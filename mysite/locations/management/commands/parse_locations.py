from bs4 import BeautifulSoup
import requests
import urllib.parse as url_parse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from locations.models import Locations
from country_sites.models import IndeedCountrySites


session = requests.Session()
session.headers.update(settings.HEADERS)


def parse(code_iso):
    city = {}
    code_state = None
    country_site = IndeedCountrySites.objects.get(code_iso=code_iso)

    r = session.get(url=country_site.states_link)

    soup = BeautifulSoup(r.text, 'html.parser')
    states_table = soup.find('table', {'id': 'states'})
    states_a = states_table.find_all('a')
    for s_a in states_a:
        state_link = country_site.site + s_a['href']
        r = session.get(url=state_link)

        soup = BeautifulSoup(r.text, 'html.parser')
        cities_table = soup.find('table', {'id': 'cities'})
        if cities_table:
            cities_a = cities_table.find_all('a')
            for c_a in cities_a:
                if code_state is None:
                    code_state = c_a['href'].split('-')[-1].strip()
                city.update({'code_state': code_state})
                city.update({'city': c_a.text.replace('Jobs in ', '').strip()})
                city.update({'state': s_a.text})
                city.update({'country': country_site})
                print(city['state'], city['city'])
                Locations.objects.get_or_create(state=city['state'], city=city['city'], defaults=city)
                city = {}
            code_state = None


def us_parse(code_iso):
    city = {}
    code_state = None
    country_site = IndeedCountrySites.objects.get(code_iso=code_iso)

    r = session.get(url=country_site.states_link)

    soup = BeautifulSoup(r.text, 'html.parser')
    states_table = soup.find('table', {'id': 'states'})
    states_a = states_table.find_all('a')
    for s_a in states_a:
        state_link = country_site.site + s_a['href']
        if url_parse.parse_qs(state_link):
            r = session.get(url=state_link)

            soup = BeautifulSoup(r.text, 'html.parser')
            cities_table = soup.find('table', {'id': 'cities'})
            if cities_table:
                cities_p = cities_table.find_all('p', {'class': 'city'})
                for c_p in cities_p:
                    a = c_p.find('a')
                    if code_state is None:
                        code_state = a['href'].split('-')[-2].strip()
                    amount = c_p.find('span', {'class': 'amount'})
                    if amount:
                        amount = amount.text.replace('(', '').replace(')', '')
                        if int(amount) > 999:
                            city.update({'level': 1})
                        else:
                            city.update({'level': 2})
                    city.update({'code_state': code_state})
                    city.update({'city': a.text.strip()})
                    city.update({'state': s_a.text})
                    city.update({'country': country_site})
                    print(city['state'], city['city'])
                    Locations.objects.get_or_create(state=city['state'], city=city['city'], defaults=city)
                    city = {}
                code_state = None


class Command(BaseCommand):
    help = 'Parse locations. -c, --country_iso_code is a Alpha-2 code of ' \
           'ISO 3166-1'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--country_iso_code', type=str)

    def handle(self, *args, **options):
        if options['country_iso_code'] == "US":
            us_parse(code_iso="US")
        elif options['country_iso_code'] == "CA":
            parse(code_iso="CA")
        elif options['country_iso_code'] == "AU":
            parse(code_iso="AU")



