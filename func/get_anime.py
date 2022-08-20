from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_anime(text: str) -> str:
    """ Search for anime on jut.su """
    header = {
        'User-Agent': UserAgent().random
    }
    name = '_'.join(text.split())
    url = f'https://jut.su/{name}'
    r = get(url, headers=header)
    if str(r) == '<Response [404]>':
        return 'Проверьте ввод...'

    soup = BeautifulSoup(r.text, 'lxml')
    url = soup.find('link').get('href')
    title = soup.find('title').text
    
    # VPN check
    if soup.find('div', class_='anime_next_announce_msg_text') is not None:
        return f'*{title}*\n{url}\n_(Нужен VPN)_'
    return f'*{title}*\n{url}'
    

if __name__ == '__main__':
    pass
