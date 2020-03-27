import requests
import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from dnb.models import IndusryDNB, CountryIndusryDNB, ShortCountryDNB, CompanyDNB
import time

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
        time_start = time.clock()
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
            script = soup.find_all('script', {'type': 'application/ld+json'})

            for s in script:
                print(s)
            print(time.clock() - time_start)
            #CompanyDNB.objects.get_or_create(link=_data['link'], defaults=_data)
            _data = {}
        else:
            continue
