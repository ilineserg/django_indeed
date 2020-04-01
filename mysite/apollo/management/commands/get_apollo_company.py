import requests
import json
import time
import pprint

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from apollo.models import ApolloCompanyLinks, ApolloCompany, ApolloEmployees, ApolloTechUsed, ApolloTags


session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Apollo parser'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)

    def handle(self, *args, **options):
        main_parse(options['start'])


def main_parse(start):
    _data = {}
    _technologies = {}
    _employees = []
    _employee = {}

    count_links = ApolloCompanyLinks.objects.count()
    limit = 1000
    offset = start
    while offset < count_links:
        selection = ApolloCompanyLinks.objects.all().order_by('id')[offset:offset + limit]

        for s in selection:
            _employees = []
            r = session.get(s.link)
            print(s.id)
            soup = BeautifulSoup(r.text, 'html.parser')

            script = soup.find('script', {'id': '__NEXT_DATA__'})
            data = json.loads(script.text)
            try:
                _data.update({'company_id_apollo': data['query']['companyId']})
            except Exception:
                continue
            _data.update({'title': s.title})
            _data.update({'link': s.link})
            _data.update({'website': data['props']['pageProps']['data']['website_url']})
            _data.update({'number_of_employees': data['props']['pageProps']['data']['employee_count']})
            _data.update({'phone': data['props']['pageProps']['data']['phone_number']})
            _data.update({'address': data['props']['pageProps']['data']['location']})

            _data.update({'description': data['props']['pageProps']['data']['description']})
            _data.update({'social_links': data['props']['pageProps']['data']['social_links']})
            technologies = data['props']['pageProps']['data']['technologies']
            company, created = ApolloCompany.objects.get_or_create(company_id_apollo=_data['company_id_apollo'], defaults=_data)

            tags = data['props']['pageProps']['data']['keywords']
            tags_objects = []
            if tags:
                for t in tags:
                    tags_objects.append(ApolloTags.objects.get_or_create(title=t)[0])
            company.tags.set(tags_objects)

            if technologies:
                list(map(lambda x: x.update({'company': ApolloCompany.objects.get(company_id_apollo=_data['company_id_apollo'])}), technologies))
                t_list = [ApolloTechUsed(**t) for t in technologies]
                ApolloTechUsed.objects.bulk_create(t_list)

            employees = data['props']['pageProps']['data']['people']

            if employees:
                for e in employees:
                    if e:
                        _employee.update({'first_name': e['first_name']})
                        _employee.update({'last_name': e['last_name']})
                        for e_h in e['employment_history']:
                            if e_h['current'] is True:
                                _employee.update({'position': e_h['title']})

                        _employees.append(_employee)
                        _employee = {}
                list(map(lambda x: x.update({'company': ApolloCompany.objects.get(company_id_apollo=_data['company_id_apollo'])}), _employees))
                e_list = [ApolloEmployees(**_e) for _e in _employees]
                ApolloEmployees.objects.bulk_create(e_list)

            _data = {}
        offset += limit