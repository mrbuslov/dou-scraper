import json
import re
import requests
import time
import requests
from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper(browser={
    'browser': 'chrome',
    'platform': 'linux',
    'mobile': False
})
    
# Step 1 - Collect all companies htmls
url = "https://jobs.dou.ua/companies/xhr-load/?"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://jobs.dou.ua",
    "Pragma": "no-cache",
    "Referer": "https://jobs.dou.ua/companies/",
    "User-Agent": "<your User-Agent here>",
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {
    "csrftoken": "<your csrftoken here",
    "_ga": "<your _ga here",
    "_gcl_au": "<your _gcl_au here",
    "__gsas": "<your __gsas here",
    "_ga_N62L6SV4PV": "<your _ga_N62L6SV4PV here",
}
    

data = {
    "csrfmiddlewaretoken": "<your csrfmiddlewaretoken here",
    "count": 0
}

dou_htmls = []
dou_companies_links = []
for i in range(100000000):
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        print(f"Request {i+1}: Status {response.status_code}")
        try:
            if response.json()['last'] == True:
                break
            dou_htmls.append(response.text)
        except Exception as e:
            print("Failed to parse JSON:", e)
        time.sleep(1)
        data['count'] += 20
    except Exception as e:
        print("Request failed:", e)
        break
with open('htmls.json', 'w') as f:
    json.dump(dou_htmls, f)


# Step 2 - extract DOU companies links from htmls
for html in dou_htmls:
    pattern = r'https://jobs\.dou\.ua/companies/[^/\s]+/'
    dou_companies_links.extend(set(re.findall(pattern, html)))

print(dou_companies_links)

with open('companies_links.json', 'w') as f:
    json.dump(dou_companies_links, f)

# Step 3 - extract all jobs links from each company html
all_hrefs = []

for i, url in enumerate(dou_companies_links):
    print(f'{i + 1}/{len(dou_companies_links)}')
    response = scraper.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        site_div = soup.find('div', class_='site')
        name_el = soup.find('h1', class_='g-h2')
        bio_el = soup.find('div', class_='bi-geo-alt-fill')
        href = None

        if site_div:
            a_tag = site_div.find('a')
            if a_tag and a_tag.has_attr('href'):
                href = a_tag['href']
        all_hrefs.append({
            "href": href,
            "name": name_el.text.strip() if name_el else None,
            "bio": bio_el.text.strip() if bio_el else None
        })
    else:
        print(f"Ошибка при запросе {url}: {response.status_code}")

print(all_hrefs)
with open('jobs_links.json', 'w') as f:
    json.dump(all_hrefs, f, ensure_ascii=False, indent=2)
