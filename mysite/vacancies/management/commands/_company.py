import urllib.parse as url_parse

from bs4 import BeautifulSoup
import json

SCRIPT_BEGIN = 'window._initialData'


def get_company_info(session, url):
    company = {
       'title': None,
       'link': url,
       'about': None,
       'headquarters': None,
       'employees': None,
       'industry': None,
       'revenue': None,
       'website': None
    }

    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    company['title'] = soup.find('h1', attrs={'class': 'cmp-SnapshotPage-heading'}).text.strip()
    scripts = soup.find_all('script')
    json_code = None

    for s in scripts:
        if s.text.startswith(SCRIPT_BEGIN):
            json_code = json.loads(s.text[len(SCRIPT_BEGIN) + 1:].rstrip(';'))

    if json_code:
        about_story = json_code.get('aboutStory')
        if about_story:
            about_description = about_story.get('aboutDescription', {})
            less_text = about_description.get('lessText', '')
            more_text = about_description.get('moreText', '')
            about_text = less_text + more_text

            if about_text:
                company.update({'about': about_text})

            about_metadata = about_story.get('aboutMetadata', {})

            company_links = about_metadata.get('companyLinks', [])
            company_links_text = "\n".join([" - ".join([link['text'], url_parse.unquote(link['href'])])
                                            for link in company_links])
            if company_links:
                company.update({'website': company_links_text})

            headquarters = about_metadata.get('headquartersLocation', '')
            headquarters = headquarters.replace('\r', ' ').replace('\n', ' ')
            if headquarters:
                company.update({'headquarters': headquarters})

            employees = about_metadata.get('employeeRange')
            if employees:
                company.update({'employees': employees})

            industry_links = about_metadata.get('industryLinks', [])
            industry_links_text = "\n".join([" - ".join([link['text'], url_parse.unquote(link['href'])])
                                             for link in industry_links])
            if industry_links:
                company.update({'industry': industry_links_text})

            revenue = about_metadata.get('revenue', None)
            if revenue:
                company.update({'revenue': revenue})

            return company
    return None