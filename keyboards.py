from telebot import types


def weather_markup():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Другой город', callback_data='Other_city')
    markup.add(button)
    return markup
    
    
def crypto_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Шифровка', callback_data='encrypt')
    button2 = types.InlineKeyboardButton('Расшифровка', callback_data='decrypt')
    markup.add(button1, button2)
    return markup


def anime_markup():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Аниме, вышедшие недавно', callback_data='recent_anime')
    markup.add(button)
    return markup

#--------------------------------------------------------------------------------------------------#

def song_markup():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Показать текст', callback_data='show_lyrics')
    button2 = types.InlineKeyboardButton('⬅️ Найти другую песню', callback_data='another_song')
    button3 = types.InlineKeyboardButton('Другие результаты', callback_data='other_results')
    button4 = types.InlineKeyboardButton('Получить ссылки', callback_data='show_links')
    markup.row(button1, button4)
    markup.row(button3)
    markup.row(button2)
    return markup


def other_songs_markup(songs):
    # songs: [ [song name, artist, id], [...] ]
    markup = types.InlineKeyboardMarkup()
    for i in range(len(songs)):
        song_name = songs[i][0]
        artist = songs[i][1]
        id = songs[i][2]
        button = types.InlineKeyboardButton(f'{song_name} - {artist}', callback_data=f'song/{id}') # returns id for `get_song_by_id()`
        markup.add(button)
    button2 = types.InlineKeyboardButton('⬅️ Найти другую песню', callback_data='another_song')
    markup.add(button2)
    return markup


def find_song_markup():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Найти другую песню', callback_data='another_song')
    markup.add(button)
    return markup