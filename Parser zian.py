import requests
from bs4 import BeautifulSoup
import csv

CSV = 'property.csv'
URL = 'https://nn.cian.ru/kupit-ofis/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='_93444fe79c--commercialWrapper--fYaWL')
    property_ = []

    for item in items:
        subway = item.find('div', class_='c6e8ba5398--region-metro--3A8ei')
        property_.append(
            {
                'title': item.find('a', class_='c6e8ba5398--header-link--3XZlV').get_text(),
                'price': item.find_all('li', class_='c6e8ba5398--header-subTerm-item--1pUL4')[1].get_text(),
                'district': item.find_all('a', class_='link_component-link-xUBVR4w6')[2].get_text(),
                'subway': 'nan' if subway is None else subway.get_text(strip=True)
            }
        )

    return property_


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название объявления', 'Цена', 'Район', 'Станция метро'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['district'], item['subway']])


def parser():
    base_url = 'https://nn.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=1&p={}&region=4885'
    pagination = int(input('Укажите кол-во страниц для парсинга: ').strip())
    urls = [base_url.format(x) for x in range(1, pagination + 1)]
    property_ = []
    for page, url in enumerate(urls):
        html = get_html(url)
        if html.status_code == 200:
            print(f'Парсим страницу: {page + 1}')
            property_.extend(get_content(html.text))
        else:
            print('Error')
    save_doc(property_, CSV)


parser()
