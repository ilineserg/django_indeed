import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from dnb.models import IndusryDNB, CountryIndusryDNB


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
    industries = IndusryDNB.objects.all()
    scheme_link = 'https://www.dnb.com'
    _data = {}
    for i in industries:
        print(i.id, i.title, i.link)
        r = session.get(url=i.link)
        soup = BeautifulSoup(r.text, 'html.parser')
        countries = soup.find_all('div', {'class': 'col-md-6 col-xs-6 data'})
        for c in countries:
            if c:
                c.a.span.decompose()
                link = scheme_link + c.a['href']
                country = c.text.strip()
                _data.update({'title': i.title,
                              'link': link,
                              'country': country})
                CountryIndusryDNB.objects.get_or_create(link=link,
                                                        defaults=_data)



