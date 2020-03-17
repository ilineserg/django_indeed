import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup

from lusha.models import CompanyLusha


session = requests.Session()
session.headers.update(settings.HEADERS)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', type=int)
        parser.add_argument('-e', '--end', type=int)

    def handle(self, *args, **options):
        main_parse(start_page=options['start'], end_page=options['end'])


def main_parse(start_page=1, end_page=60):

    for page in range(start_page, end_page + 1):
        print(f'Page {page} in process.....')
        link = f'https://www.lusha.co/organizations/?page={page}'
        r = session.get(url=link)
        soup = BeautifulSoup(r.text, 'html.parser')
        company_list = soup.find('div', {'class': 'company-list'})
        companies = company_list.find_all('a')
        for company in companies:
            company_dict = {}
            c_details_dict = {}
            c_social = {}
            emails = {}

            c_link = company['href']
            company_dict.update({'link': c_link})

            r_c = session.get(url=c_link)
            soup = BeautifulSoup(r_c.text, 'html.parser')

            company_info = soup.find('div', {'class': 'company-info'})
            company_dict.update({'description_html': str(company_info)})

            if company_info:
                text_block = company_info.find('div', {'class': 'text-block'})
                company_dict.update({'title': text_block.find('h1').text})
                company_dict.update({'description_text': text_block.find('p').text})

                class_link = text_block.find('div', {'class': 'link'})
                company_dict.update({'link_outer': class_link.find('a')['href']})

                company_details = text_block.find('dl', {'class': 'company-details'})
                if company_details:
                    d_key, d_value = None, None
                    for detail in company_details:
                        if detail.name == 'dt':
                            d_key = detail.text
                        if detail.name == 'dd':
                            d_value = detail.text
                        if d_key and d_value:
                            c_details_dict.update({d_key: d_value})
                            d_key, d_value = None, None

                company_dict.update({'company_details': json.dumps(c_details_dict)})

                company_social = text_block.find('ul',
                                                  {'class': 'company-social-networks'})
                if company_social:
                    for social in company_social:
                        _data = social.find('a')
                        if _data != -1:
                            c_social.update({_data['class'][0]: _data['href']})

                company_dict.update({'company_social_networks': json.dumps(c_social)})

                email_formats_div = soup.find('div', {'class': 'formats-table'})
                trs = email_formats_div.find_all('tr')
                for tr in trs:
                    td = tr.find_all('td')
                    emails.update({td[0].text:[td[1].text, td[2].text]})
                company_dict.update({'email_address_formats': json.dumps(emails)})
            CompanyLusha.objects.get_or_create(link=company_dict['link'],
                                                   defaults=company_dict)







