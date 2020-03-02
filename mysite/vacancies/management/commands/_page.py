import json
import re
from bs4 import BeautifulSoup
from django.conf import settings

from vacancies.management.commands._utils import normalize_url, debug_log, colorize, Colors

JOBS_URL = normalize_url(settings.INDEED_BASE_URL, settings.JOBS_PATH)
JOBS_DESC_URL = normalize_url(settings.INDEED_BASE_URL, settings.JOBS_DESC_PATH)


def get_vacancies_on_page(session, params):
    r = session.get(url=JOBS_URL, params=params)
    try:
        r.raise_for_status()
    except Exception as e:
        message = f"{colorize('Error', Colors.RED)}\nRequest status: {r.code}\n"
        debug_log(message)
        return None

    soup = BeautifulSoup(r.text, 'lxml')
    scripts_els = soup.find_all('script')

    script = None

    for script_el in scripts_els:
        _text = script_el.text
        if _text.find("var jobmap") != -1:
            script = _text

    if not script:
        message = f"{colorize('Not Found Vacancies on Page', Colors.RED)}\n"
        debug_log(message)
        return None

    pattern = re.compile(r"jobmap\[\d+\]{1}(.+[};])")
    _data = re.findall(pattern, script)

    kv_pattern = re.compile(r"(\w+):{1}\s?'(.*?)'")

    _data = list(map(lambda x: x.strip().lstrip('=').rstrip(';').strip(), _data))
    data = []
    for row in _data:
        _d = re.findall(kv_pattern, row)
        data.append({k: v for k, v in _d})

    job_keys = list(map(lambda x: x.get('jk', ''), data))

    r_desc = session.get(JOBS_DESC_URL, params={'jks': ",".join(job_keys)})
    r_desc_json = r_desc.json()

    descriptions = {k: {'text': BeautifulSoup(v, 'lxml').text, 'html': v} for k, v in r_desc_json.items()}

    for item in data:
        jk = item.get('jk', '')
        item.update({'description': descriptions.get(jk, {'text': '', 'html': ''})})
        if jk:
            data_el = soup.find('div', attrs={'id': f"p_{jk}"})
            company_link = data_el.find('a', attrs={'data-tn-element': 'companyName'})
            if company_link:
                item.update({"company_link": company_link.attrs['href']})

            link = data_el.find('a', attrs={'id': f'jl_{jk}'})
            if link:
                item.update({"link": link.attrs['href']})

    return data