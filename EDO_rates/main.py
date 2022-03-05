import requests

from bs4 import BeautifulSoup


def get_edo_rate(exp_date):

    url = f'https://www.obligacjeskarbowe.pl/oferta-obligacji/obligacje-10-letnie-edo/edo{exp_date}/'

    edo_site = requests.get(url).text
    edo_html = BeautifulSoup(edo_site, 'html.parser')

    rate = edo_html.find(class_='interest').text.split(',')
    rate = float('.'.join(rate))

    return rate

print(get_edo_rate('1231'))