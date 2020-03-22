import requests
import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from dnb.models import IndusryDNB, CountryIndusryDNB, ShortCountryDNB, CompanyDNB


session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)
        parser.add_argument('-e', '--end', type=int)

    def handle(self, *args, **options):
        main_parse(start=options['start'], end=options['end'])


def main_parse(start, end):
    items_count = 0
    scheme_link = 'https://www.dnb.com'
    _data = {}
    for i in range(start, end):
        try:
            company = ShortCountryDNB.objects.get(id=i)
        except Exception:
            continue
        print(company.id)
        print(company.country)
        print(company.link)
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
            continue
