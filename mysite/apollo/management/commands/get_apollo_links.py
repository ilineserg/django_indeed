import requests

from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management import BaseCommand

from apollo.models import ApolloCompanyLinks

session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)
        parser.add_argument('-e', '--end', type=int)

    def handle(self, *args, **options):
        main_parse(options['start'])


def main_parse(start, end=91):
    for i in range(start, end):
        print(f'we are on page {chr(i)}')
        r = session.get(f'https://www.apollo.io/directory/companies/{chr(i)}')
        soup = BeautifulSoup(r.text, 'lxml')
        _a = soup.find_all('a', {'class': 'cQqDMz'})
        last_page = int(_a[-1].text)
        for j in range(1, last_page):
            print(f'we are on page {j}')
            r_letter_num = session.get(
                f'https://www.apollo.io/directory/companies/{chr(i)}/{j}')
            soup_letter_num = BeautifulSoup(r_letter_num.text, 'lxml')
            _a_company = soup_letter_num.find_all('a', {'class': 'bFxflP'})
            print(type(_a_company))
            for company in _a_company:
                _data = {}
                _data.update({'title': company.text})
                _data.update({'link': f"https://www.apollo.io/companies{company['href']}"})
                ApolloCompanyLinks.objects.get_or_create(link=_data.get('link'), defaults=_data)