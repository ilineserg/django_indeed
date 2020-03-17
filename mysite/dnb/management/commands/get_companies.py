import requests
import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from dnb.models import IndusryDNB, CountryIndusryDNB, ShortCountryDNB


session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)
        parser.add_argument('-e', '--end', type=int)

    def handle(self, *args, **options):
        main_parse()


def main_parse():
    items_count = 0
    scheme_link = 'https://www.dnb.com'
    r = session.get('https://www.dnb.com/business-directory/industry-analysis.agriculture-forestry-sector.html')
    print(r)
    industries_by_countries = CountryIndusryDNB.objects.all()
    _data = {}
    for ibc in industries_by_countries:
        if ibc.id < 505:
            continue
        print(ibc.id, ibc.link, ibc.country)
        link_wo_page = ibc.link.split('?')[0]
        if ibc.country == 'Australia':
            for i in range(1, 21):
                time.sleep(1)
                print(f'{items_count} add')
                print(f'page={i}')
                link = link_wo_page + f'?page={i}'
                r = session.get(url=link)
                print(r)
                soup = BeautifulSoup(r.text, 'html.parser')
                company_results = soup.find('div', {'id': 'companyResults'})
                if company_results:
                    print('yes')
                    items = company_results.find_all('a')
                    for i in items:
                        try:
                            link = scheme_link + i['href']
                            _data.update({'title': i.text.strip(),
                                          'link': link,
                                          'country': ibc.country})
                            ShortCountryDNB.objects.get_or_create(
                                link=_data['link'],
                                defaults=_data)
                            if _data:
                                items_count += 1
                            _data = {}
                        except Exception:
                            _data = {}
                            continue

                else:
                    with open('out.txt', 'w') as out:
                        out.write(f'{link}')
        else:
            continue