import requests

from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management import BaseCommand

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
    r = session.get('https://www.apollo.io/companies/Abaco-Consulting/54a11c6e69702d8ed4afa100?chart=count')

    soup = BeautifulSoup(r.text, 'lxml')
    html = soup.find('html')
    print(html)
    with open('out.html', 'w') as out_f:
        out_f.write(str(html))

