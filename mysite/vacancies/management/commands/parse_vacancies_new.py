import traceback

import requests
import urllib.parse as url_parse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from companies.models import Company
from country_sites.models import IndeedCountrySites
from locations.models import Locations
from vacancies.management.commands._company import get_company_info
from vacancies.management.commands._page import get_vacancies_on_page
from vacancies.management.commands._utils import debug_log, normalize_url, \
    error_log
from vacancies.models import Vacancy

session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = """Parse indeed.com
    --search - 
    """

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str)
        parser.add_argument('--search', type=str)
        parser.add_argument('-s', '--start', type=int)
        parser.add_argument('-q', '--quantity', type=int)
        parser.add_argument('--by_location', action='store_true')
        parser.add_argument('--location_lvl', type=str)

    def handle(self, *args, **options):
        print(options)
        if options['by_location']:
            parse_by_location(search=options['search'],
                              page=options['start'],
                              quantity=options['quantity'],
                              country=options['country'],
                              location_lvl=options['location_lvl'])
        else:
            main_parse(search=options['search'],
                       page=options['start'],
                       quantity=options['quantity'],
                       country=options['country'])


def main_parse(search, page, quantity, vacancy_on_page=10, location=None, country=None):
    country_site = IndeedCountrySites.objects.get(code_iso=country)
    start_at = page * vacancy_on_page

    debug_log(f'{"#"* 21}\nParse starts at: {start_at}')

    total_company_add = 0
    total_vacancies_add = 0

    for start in range(start_at, quantity, vacancy_on_page):

        page_num = int(start / vacancy_on_page)
        debug_log(f"Parse Page: {page_num}")

        params = {
            'start': start,
            'sort': settings.DEFAULT_SORT
        }
        if search:
            params.update({'q': search})
        if location:
            params.update({'l': location})

        debug_log(f'Params: {params}')

        try:
            vacancies = get_vacancies_on_page(country=country, session=session, params=params)
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
                        _counry = IndeedCountrySites.objects.get(
                            code_iso=country)
                        company_link = normalize_url(_counry.site, company_link)
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
                                revenue=company_data.get('revenue'),
                                country_site=country_site
                            )

                            company.save()

                            company_add += 1
                        else:
                            company = None
                else:
                    company = None

                job_key = vacancy_data.get('jk')
                if not job_key:
                    continue

                exist_vacancy = Vacancy.objects.filter(job_key=job_key).first()
                print(exist_vacancy)

                if exist_vacancy:
                    continue

                vacancy_url = vacancy_data.get('link')

                vacancy = Vacancy(
                    job_key=job_key,
                    title=vacancy_data.get('title'),
                    link=normalize_url(country_site.site, vacancy_url),
                    description_text=vacancy_data.get('description', {}).get('text'),
                    description_html=vacancy_data.get('description', {}).get('html'),

                    location=vacancy_data.get('loc'),
                    location_uid=vacancy_data.get('locid'),
                    country=vacancy_data.get('country'),
                    city=vacancy_data.get('city'),
                    zip=vacancy_data.get('zip'),

                    company_name=url_parse.unquote(vacancy_data.get('srcname', '')),
                    company_uid=vacancy_data.get('cmpid'),
                    company_link=normalize_url(country_site.site, company_link) if company_link else None,
                    company_id=company.id if company else None,
                    raw_data=vacancy_data,
                    country_site=country_site
                )
                _data = {'title': vacancy.title,
                         'link': vacancy.link,
                         'description_text': vacancy.description_text,
                         'description_html': vacancy.description_html,
                         'location': vacancy.location,
                         'location_uid': vacancy.location_uid,
                         'country': vacancy.company,
                         'city': vacancy.city,
                         'zip': vacancy.zip,
                         'company_name': vacancy.company_name,
                         'company_uid': vacancy.company_uid,
                         'company_link': vacancy.company_link,
                         'company_id': company.id if company else None,
                         'raw_data': vacancy.raw_data,
                         'country_site': country_site}
                Vacancy.objects.get_or_create(job_key=job_key, defaults=_data)
                vacancies_add += 1

            total_company_add += company_add
            total_vacancies_add += vacancies_add
            debug_log(f"TC: {total_company_add}, TV: {total_vacancies_add}, C: {company_add}, V: {vacancies_add}")

        except Exception as e:
            tb = traceback.format_exc()
            error_log(f"###\nPage {page}\n{tb}")
            raise


def parse_by_location(search, page, quantity, country, location_lvl, vacancy_on_page=10):
    _country = IndeedCountrySites.objects.get(code_iso=country)
    location_list = Locations.objects.values_list('city', 'code_state').filter(country=_country)
    location_list = list(map(lambda x: ', '.join(x), location_list))

    for location in location_list:
        try:
            main_parse(search, page, quantity, vacancy_on_page, country=country, location=location)
        except Exception:
            continue