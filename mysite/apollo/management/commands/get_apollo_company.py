import requests
import json
import time
import pprint

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from apollo.models import ApolloCompanyLinks, ApolloCompany, ApolloEmployees, ApolloTechUsed


session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)

    def handle(self, *args, **options):
        main_parse()


def main_parse():
    _data = {}
    _technologies = {}
    _employees = []
    _employee = {}
    technologies = None
    employees = None


    count_links = ApolloCompanyLinks.objects.count()
    limit = 1001
    offset = 0
    while offset < count_links:
        selection = ApolloCompanyLinks.objects.all()[offset:offset + limit]

        for s in selection:
            r = session.get('https://www.apollo.io/companies/companies/Askredit-IFN-SA/5a9e4ef4a6da98d9467382d9')
            soup = BeautifulSoup(r.text, 'html.parser')

            script = soup.find('script', {'id': '__NEXT_DATA__'})
            data = json.loads(script.text)
            try:
                _data.update({'company_id': data['query']['companyId']})
                _data.update({'title': s.title})
                _data.update({'link': s.link})
                _data.update({'website': data['props']['pageProps']['data']['website_url']})
                _data.update({'number_of_employees': data['props']['pageProps']['data']['employee_count']})
                _data.update({'phone': data['props']['pageProps']['data']['phone_number']})
                _data.update({'address': data['props']['pageProps']['data']['location']})
                _data.update({'tags': data['props']['pageProps']['data']['keywords']})
                _data.update({'description': data['props']['pageProps']['data']['description']})

                technologies = data['props']['pageProps']['data']['technologies']

                if technologies:
                    print(technologies)
                    #list(map(lambda x: x.update({'company': ApolloCompany.objects.filter(company_id=_data['company_id']).first()}), technologies))
                    list(map(lambda x: x.update({'company': '!!!'}), technologies))
                    #ApolloTechUsed.objects.bulk_create(technologies)

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

                print(_employees)
            except Exception:
                break
            break

        break

    offset += limit

    """
    for i in range(start, end):


        if company.country:
            r = session.get(company.link)
            soup = BeautifulSoup(r.text, 'html.parser')
            _data.update({'country': company.country})
            _title = soup.find('h1', {'class': 'title'})
            _data.update({'title': _title.text if _title else None})

            _data.update({'link': company.link})

            _address = soup.find('div', {'class': 'address'})
            _data.update({'address': _address.text.strip() if _address else None})
            _data.update({'address_html': str(_address) if _address else None})

            _phone = soup.find('div', {'class': 'phone'})
            _data.update({'phone': _phone.text if _phone else None})

            _website = soup.find('div', {'class': 'web'})
            if _website:
                _website = _website.find('a')['href']
                _data.update({'website': _website})

            _company_type = soup.find('span', {'class': 'type'})
            _data.update({'company_type': _company_type.text if _company_type else None})

            _company_role = soup.find('span', {'class': 'role'})
            _data.update({'company_role': _company_role.text if _company_role else None})

            _description_text = soup.find('span', {'class': 'company_summary'})
            if _description_text:
                _description_text.a.decompose()
                _data.update({'description_text': _description_text.text})

            _employees = soup.find('li', {'class': 'emp'})
            if not _employees:
                _employees = soup.find('li', {'class': 'empCon'})
                if _employees:
                    _employees = _employees.find('span', {'class': 'value'}).text
            else:
                if _employees:
                    _employees = _employees.find('span', {'class': 'value'}).text

            _data.update({'employees': _employees})

            _incorporated = soup.find('li', {'class': 'founded'})
            print(_incorporated)
            if _incorporated:
                _incorporated = _incorporated.find('span', {'class': 'value'}).text
                print(_incorporated)
                _data.update({'incorporated': _incorporated})

            _corporate_family_connections = soup.find('div', {'class': 'count'})
            _data.update({'corporate_family_connections': _corporate_family_connections.text.strip() if _corporate_family_connections else None})
            CompanyDNB.objects.get_or_create(link=_data['link'], defaults=_data)
            _data = {}
        else:
            continue"""
