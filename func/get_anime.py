from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


header = {
        'User-Agent': UserAgent().random
    }


def get_anime(text: str) -> str:
    """ Search for anime on jut.su """
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
    

def new_anime() -> str:
    """ Finds anime that came out today on jut.su """
    url = 'https://jut.su/'
    r = get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div', class_='media_b clear new_all_other_last_eps').find_all('div', class_='media_content')
    anime_list = []
    for item in results:
        name = item.find('div', class_='b-g-title').text
        episode = item.find('span', class_='ml_padding').text
        url = item.find('a', class_='media_link l_e_m_l').get('href')
        anime_list.append(
            [
                name,
                episode,
                url
            ]
        )
    return _parse_anime_list(anime_list)
    
    
def _parse_anime_list(anime_list: list[list]) -> str:
    result = []
    for anime in anime_list:
        result.append(f'{anime[0]} - {anime[1]}\n{anime[2]}')
    parsed_result = '\n\n'.join(result)
    return parsed_result


if __name__ == '__main__':
    print(new_anime())
