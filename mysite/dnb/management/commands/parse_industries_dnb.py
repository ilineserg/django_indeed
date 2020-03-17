import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from dnb.models import IndusryDNB


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
    link = 'https://www.dnb.com/business-directory.html'
    scheme_link = 'https://www.dnb.com'
    r = session.get(url=link)
    soup = BeautifulSoup(r.text, 'html.parser')
    step = 0

    industry_links = soup.find_all('div', {'class': 'link'})
    for i_link in industry_links:
        step += 1
        print(step)
        title = i_link.text.strip()
        industry_link = scheme_link + i_link.find('a')['href']
        IndusryDNB.objects.update_or_create(title=title, link=industry_link,
                                            defaults={'title': title,
                                                      'link': industry_link})
