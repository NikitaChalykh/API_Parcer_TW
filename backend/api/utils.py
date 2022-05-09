import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_meta_tag(data, symbol):
    '''Функция для обработки данных из мета-тегов'''
    data = str(data)
    new_data_dict = []
    for i in range(15, len(data) + 1):
        if data[i] != symbol:
            new_data_dict.append(data[i])
        else:
            break
    return ''.join(new_data_dict)


def get_tag_for_value(data):
    '''Функция для обработки числовых данных из тегов'''
    data = str(data)
    new_data_dict = []
    for symbol in data:
        try:
            int(symbol)
            new_data_dict.append(symbol)
        except ValueError:
            continue
    return int(''.join(new_data_dict)) * 100


def get_card(vendor_code):
    '''Функция для получения данных с сайта по артикулу'''
    url = 'https://www.wildberries.ru/catalog/{}/detail.aspx'.format(
        vendor_code
    )
    response = requests.get(
        url,
        headers={'User-Agent': UserAgent().chrome}
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    vendor_code_quote = soup.find('span', id="productNmId")
    brand_quote = soup.find('meta', itemprop="brand")
    name_quote = soup.find('meta', itemprop="name")
    discont_value_quote = soup.find('span', class_="price-block__final-price")
    value_quote = soup.find(
        'del', class_="price-block__old-price j-final-saving"
    )
    return {
        'vendor_code': int(vendor_code_quote.text),
        'brand': get_meta_tag(brand_quote, '"'),
        'name': get_meta_tag(name_quote, ','),
        'discont_value': get_tag_for_value(discont_value_quote.text),
        'value': get_tag_for_value(value_quote.text)
    }


def get_supplier(vendor_code):
    data = requests.get(
        'https://wbx-content-v2.wbstatic.net/sellers/{}.json'.format(
            vendor_code
        )
    ).text
    supplier = json.loads(data)['supplierName']
    return supplier
