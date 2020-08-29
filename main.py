import re

from bs4 import BeautifulSoup
import requests

from Package import Package

URL = 'https://irancell.ir/en/o/1001/online-purchase-of-internet-packages'


def scrape(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    elems = soup.find_all('div',
                          attrs={'class': 'col-md-6 col-xl-4 js-product'})
    packs = []
    for e in elems:
        try:
            price = int(re.sub('[^0-9]', '', e.attrs['data-payable']))
            p = Package(volume=get_volume(e), duration=get_duration_in_hours(e), price=price)
            p.is_local = 'Local' in e.find(attrs={'class': 'js-name-product'}).text
            p.description = e.find(attrs={'class': 'package-card__subtitle'}).text
            p.is_time_limited = not not p.description
            packs.append(p)
        except BaseException as err:
            print(e, err)

    packs.sort(key=lambda el: el.price_per_gig())
    for p in packs:
        print(p)


def get_volume(elem):
    vol = elem.attrs['data-volume']
    if vol:
        if vol != 'unlimited':
            return int(vol)
        else:
            if elem.attrs['data-duration'] == '30days':
                return 150 * 1024
            elif elem.attrs['data-duration'] == '7days':
                return 50 * 1024
            elif elem.attrs['data-duration'] == 'daily':
                return 25 * 1024
            elif elem.attrs['data-duration'] == 'hourly':
                return get_duration_in_hours(elem) * 20 * 1024
            else:
                raise Exception('--- duration invalid!')
    else:
        name = elem.find(attrs={'class': 'js-name-product'}).text
        vol = re.findall(r'\d+MB|\d+GB', name)[0]
        if vol.endswith('GB'):
            return int(re.sub('[^0-9]', '', vol)) * 1024
        else:
            return int(re.sub('[^0-9]', '', vol))


def get_duration_in_hours(elem):
    k = elem.attrs['data-duration']
    if k != 'hourly':
        if k != 'daily':
            return int(re.sub('[^0-9]', '', k)) * 24
        else:
            return 24
    else:
        name = elem.find(attrs={'class': 'js-name-product'}).text
        if elem.attrs['data-volume'] == 'unlimited':
            return int(re.sub('[^0-9]', '', name))
        else:
            return int(re.findall(r'\b\d+\b', name)[0])


if __name__ == '__main__':
    scrape(URL)
