import requests


class Song(): # Костыль, который не работает с несколькими пользователями одновременно
    def __init__(self, text, song_id, links, other_songs) -> None:
        self.text = text
        self.song_id = song_id
        self.links = links
        self.other_songs = other_songs # list: [ [song name, artist, id], [...] ]

"""
    get_song создаёт экземпляр класса, в котором присутствуют "другие результаты".
    get_song_by_id пересоздаёт его, не изменяя "другие результаты" и используется только
в InlineKeyboard при взаимодействии со списком других рузультатов (из-за этого можно просмтривать 
песни из списка по очереди и возвращаться к тем же результатам обратно).
    get_song пересоздаёт объект с новым списком "других результатов" и используется только
при поиске новой песни при помощи текстовых сообщений.

get_lyrics имеет хард лимит API запросов (100 в месяц), поэтому запускается отдельно по кнопке. 
"""

def get_song(text: str) -> Song:
    """ Get top search result song (data to display, id, links) and other results """
    url = "https://genius.p.rapidapi.com/search"
    querystring = {"q":f"{text}"}
    headers = {
        "X-RapidAPI-Key": "23ae694b94mshde60663923854bcp123394jsn8a655805e626",
        "X-RapidAPI-Host": "genius.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    # other results (2-10) (max 10)
    hits = [data['response']['hits'][i]['result'] for i in range(1,10)]
    other_songs = []
    for track in hits:
        title = track['title']
        artist_name = track['artist_names']
        id = track['id']
        title, artist_name = _format_ru_text(title, artist_name)
        other_songs.append([title, artist_name, id])

    # top result song
    song_info = data['response']['hits'][0]['result']
    artist_name = song_info['artist_names']
    title = song_info['title_with_featured']
    date = song_info['release_date_for_display']
    id = song_info['id']
    url = song_info['url']
    title, artist_name = _format_ru_text(title, artist_name)
    social_links = _get_song_links(id)
    
    top_result_data = f'{artist_name} - {title}\n{date}\n\nСсылка на текст: {url}'
    return Song(top_result_data, id, social_links, other_songs)


def get_song_by_id(id: int, songs: list) -> Song:
    """ Get song by id (for inline keyboard with other search results) """
    url = f"https://genius.p.rapidapi.com/songs/{id}"
    headers = {
        "X-RapidAPI-Key": "23ae694b94mshde60663923854bcp123394jsn8a655805e626",
        "X-RapidAPI-Host": "genius.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    song_info = data['response']['song']

    artist_name = song_info['artist_names']
    title = song_info['title_with_featured']
    date = song_info['release_date_for_display']
    song_id = song_info['id']
    url = song_info['url']
    title, artist_name = _format_ru_text(title, artist_name)
    social_links = _get_song_links(song_id)

    top_result_data = f'{artist_name} - {title}\n{date}\n\nСсылка на текст: {url}'
    return Song(top_result_data, song_id, social_links, songs)


def get_lyrics(id: int) -> str:
    """ Get song lyrics (hard limit API 100/month) """
    try:
        url = f"https://genius-song-lyrics1.p.rapidapi.com/songs/{id}/lyrics"
        headers = {
            "X-RapidAPI-Key": "23ae694b94mshde60663923854bcp123394jsn8a655805e626",
            "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers)
        lyrics = response.json()['response']['lyrics']['lyrics']['body']['plain']
        return lyrics
    except:
        return 'Произоша ошибка... Используйте ссылку выше ⬆️'


def _get_song_links(id: int) -> str:
    """ Get links to streaming services """
    url = f"https://genius.p.rapidapi.com/songs/{id}"
    headers = {
        "X-RapidAPI-Key": "23ae694b94mshde60663923854bcp123394jsn8a655805e626",
        "X-RapidAPI-Host": "genius.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    name = response.json()['response']['song']['full_title']
    data = response.json()['response']['song']['media']
    result = []
    for song in data:
        url = song['url']
        provider = song['provider']
        result.append(f'Сервис: _{provider}_\n{url}\n')
    return f'*{name}*\n\n' + '\n'.join(result) 


def _format_ru_text(title: str, artist: str) -> list[str]:
    """ Cutting off the English translation of Russian names """
    try:
        title = title[:title.index('(')]
    except: 
        pass
    try:
        artist = artist[:artist.index('(')] + artist[artist.index(')')+2:]
    except:
        pass
    return [title, artist]


if __name__ == '__main__':
    print(_get_song_links(5049949))