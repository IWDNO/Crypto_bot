from requests import get
from random import randint
from bs4 import BeautifulSoup



def get_joke() -> str:
    """ Get random joke from `mir-knig.com` """
    page = randint(1,32)
    r = get(f'https://mir-knig.com/joke/cat/2?p_={page}')
    soup = BeautifulSoup(r.text, 'lxml')
    divs = soup.find_all("div", {'class':'col-s-12'})[4:-7]
    index = randint(0, len(divs)-1)
    joke_body = divs[index]

    # Проверка на рекламный баннер
    result = _parse_joke(joke_body)
    if  result != '':
        return f'Анекдот:\n\n{result}'
    else:
        result = _parse_joke(divs[index-1]) # previous joke
        return f'Анекдот:\n\n{result}'
    

def _parse_joke(body: BeautifulSoup) -> str:
    parts = body.find_all('p')
    result = '\n'.join(x.text for x in parts)
    return result


if __name__ == '__main__':
    print(get_joke())
