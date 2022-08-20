from requests import get
from bs4 import BeautifulSoup


def get_holiday() -> str:
    """ Get today's holiday from `www.calend.ru` """
    r = get('https://www.calend.ru/')
    soup = BeautifulSoup(r.text, 'lxml')
    holiday_block = soup.find_all('div', class_='wrapIn')
    result = holiday_block[0].find('a').text

    date_block = soup.find_all('span', class_='title date')
    date = date_block[0].find('a').text

    return f'{date}:\n{result}'