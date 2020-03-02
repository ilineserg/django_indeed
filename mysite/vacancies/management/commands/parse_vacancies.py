import traceback

import requests
import urllib.parse as url_parse

from django.core.management.base import BaseCommand, CommandError
from mysite.vacancies.models import Vacancy
from mysite.companies.models import Company

from ._utils import debug_log, error_log, normalize_url
from ._page import get_vacancies_on_page
from ._company import get_company_info
from . import _locations as locations
from . import _config as config


session = requests.Session()
session.headers.update(config.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)
        parser.add_argument("search", type=str, default='Sales')
        parser.add_argument("start", type=int, default=0)
        parser.add_argument("quantity", type=int, default=1000)
        parser.add_argument("location", type=str, default='by_cities')

    def handle(self, *args, **options):
        if options['location'] == 'by_cities':
            parse_by_location(search=options['search'], page=options['start'], quantity=options['quantity'])
        elif options['location'] == 'all':
            main_parse(search=options['search'], page=options['start'], quantity=options['quantity'])


def main_parse(search, page, quantity, vacancy_on_page=10, location=None):

    start_at = page * vacancy_on_page

    debug_log(f'{"#"* 21}\nParse starts at: {start_at}')

    total_company_add = 0
    total_vacancies_add = 0

    vacancies_for_add = []

    for start in range(start_at, quantity, vacancy_on_page):

        page_num = int(start / vacancy_on_page)
        debug_log(f"Parse Page: {page_num}")

        params = {
            'start': start,
            'sort': config.DEFAULT_SORT,
            'q': search
        }
        if location:
            params.update({'l': location})

        debug_log(f'Params: {params}')

        try:
            vacancies = get_vacancies_on_page(session=session, params=params)
            if vacancies is None:
                continue

            company_add = 0
            vacancies_add = 0

            for vacancy_data in vacancies:

                company_uid = vacancy_data.get('cmpid', None)
                company_link = vacancy_data.get('company_link', None)

                if company_uid:
                    company = Company.objects.filter(uid=company_uid).first()
                    if not company and company_link:
                        company_link = normalize_url(config.BASE_URL, company_link)
                        company_data = get_company_info(session, company_link)
                        if company_data:
                            company = Company(
                                uid=company_uid,
                                name=company_data.get('title'),
                                link=company_link,
                                about=company_data.get('about'),
                                headquarters=company_data.get('headquarters'),
                                employees=company_data.get('employees'),
                                industry=company_data.get('industry'),
                                website=company_data.get('website'),
                                revenue=company_data.get('revenue')
                            )
                            Company.save(company)
                            company_add += 1
                        else:
                            company = None
                else:
                    company = None

                job_key = vacancy_data.get('jk')
                if not job_key:
                    continue

                exist_vacancy = Vacancy.objects.filter(job_key=job_key).first()
                if exist_vacancy:
                    continue

                vacancy_url = vacancy_data.get('link')

                vacancy = Vacancy(
                    job_key=job_key,
                    title=vacancy_data.get('title'),
                    link=normalize_url(config.BASE_URL, vacancy_url),
                    description_text=vacancy_data.get('description', {}).get('text'),
                    description_html=vacancy_data.get('description', {}).get('html'),

                    location=vacancy_data.get('loc'),
                    location_uid=vacancy_data.get('locid'),
                    country=vacancy_data.get('country'),
                    city=vacancy_data.get('city'),
                    zip=vacancy_data.get('zip'),

                    company_name=url_parse.unquote(vacancy_data.get('srcname', '')),
                    company_uid=vacancy_data.get('cmpid'),
                    company_link=normalize_url(config.BASE_URL, company_link) if company_link else None,
                    company_id=company.id if company else None,
                    raw_data=vacancy_data
                )
                vacancies_for_add.append(vacancy)
                vacancies_add += 1

            Vacancy.objects.bulk_create(vacancies_for_add)
            total_company_add += company_add
            total_vacancies_add += vacancies_add

            debug_log(f"TC: {total_company_add}, TV: {total_vacancies_add}, C: {company_add}, V: {vacancies_add}")

        except Exception as e:
            tb = traceback.format_exc()
            error_log(f"###\nPage {page}\n{tb}")
            raise


def parse_by_location(search, page, quantity, vacancy_on_page=10):
    location_list = locations.CITIES

    for location in location_list:
        try:
            main_parse(search, page, quantity, vacancy_on_page, location=location)
        except Exception:
            continue


