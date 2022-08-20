from messages import *
from config import *
from keyboards import *
from func.get_song import get_song, get_lyrics, get_song_by_id
from func.get_weather import get_weather
from func.get_joke import get_joke
from func.crypto import encrypt, decrypt
from func.get_holiday import get_holiday
from func.get_anime import get_anime

from flask import Flask, request
import random, os, telebot


bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 's'])
def send_welcome(message):
    """ Start message """
    name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        START_MESSAGE.format(name=name),
        parse_mode="Markdown"
    )
    sticker = START_STICKERS[random.randint(0,2)]
    bot.send_animation(message.chat.id, sticker)


@bot.message_handler(commands=['help'])
def other_functions(message):
    """ Help command """
    bot.send_message(
        message.chat.id,
        HELP_MESSAGE,
        parse_mode='Markdown'
    )

#-----------------------------------------------------------------------------------------------------------
# Weather
@bot.message_handler(commands=['weather'])
def weather(message):
    """ Weather command """
    msg = bot.send_message(message.chat.id, 'Секунду...')
    try:
        result = get_weather(message.text)
        bot.edit_message_text(                             
            chat_id=message.chat.id, message_id=msg.message_id,
            text=result, reply_markup=weather_markup(),
            parse_mode="Markdown"
    )
    except Exception:                                         
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=ERROR_MESSAGE)
        

# Songs
@bot.message_handler(commands=['song'])
def song(message):
    """ Song command (requests song title). Passed to `_song` function"""
    msg = bot.send_message(message.chat.id, '🎵 Введите название песни / текст:')
    bot.register_next_step_handler(msg, _song)


def _song(message):
    global current_song
    """ Creates a Song object and sends a message with information about the song to the user """
    try:
        text = message.text
        current_song = get_song(text)
        print(current_song.other_songs)
        bot.send_message(message.chat.id, current_song.text, reply_markup=song_markup())
    except Exception:
        print(Exception)
        bot.send_message(message.chat.id, ERROR_MESSAGE)


# Cryptographer
@bot.message_handler(commands=['crypto'])
def cryptographer(message):
    """ Send start Cryptogarpher message"""
    bot.send_message(message.chat.id, 'Выбери что-нибудь 😉', reply_markup=crypto_markup())


def _encr(message):
    """ Message encryption """
    if message.text == '/back':
        cryptographer(message)
        return None
    markup = crypto_markup()
    result = encrypt(message.text)
    bot.send_message(message.chat.id, f'>>> Ваше сообщение (_Нажми_):\n\n`{result}`', parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Что-нибудь ещё? 😉', reply_markup=markup)


def _decr(message):
    """ Message decryption """
    if message.text == '/back':
            cryptographer(message)
            return None
    try:
        result = decrypt(message.text)
        bot.send_message(message.chat.id, f'>>> Вам написали:\n{result}')
        bot.send_message(message.chat.id, 'Что-нибудь ещё? 😉', reply_markup=crypto_markup())
    except ValueError:
        bot.send_message(message.chat.id, ERROR_MESSAGE)


# Anime search
@bot.message_handler(commands=['anime'])
def anime(message):
    """ Requests anime title"""
    msg = bot.send_message(message.chat.id, 'Введите название аниме:')
    bot.register_next_step_handler(msg, _get_anime_link)


def _get_anime_link(message):
    """ Get anime data by title"""
    text = message.text
    result = get_anime(text)
    bot.send_message(message.chat.id, result, parse_mode='Markdown')


# Анекдот
@bot.message_handler(commands=['joke'])
def joke(message):
    """ Get random joke """
    msg = bot.send_message(message.chat.id, 'Секунду...') 
    result = get_joke()
    bot.edit_message_text(result, msg.chat.id, msg.message_id)

# Holiday
@bot.message_handler(commands=['holiday'])
def holiday(message):
    """ Get today's holiday """
    msg = bot.send_message(message.chat.id, 'Секунду...')
    result = get_holiday()
    bot.edit_message_text(result, message.chat.id, msg.message_id)

# Yes/No
@bot.message_handler(commands=['?', 'coin'])
def coin_flip(message):
    result = ('Yes', 'No')[random.randint(0,1)]
    bot.reply_to(message, result)

# Twerk
@bot.message_handler(commands=['twerk'])
def twerk(message):
    sticker = TWERK_STICKERS[0] if random.random() < 0.10 else TWERK_STICKERS[1]
    bot.send_animation(message.chat.id, sticker)

# Calculator
@bot.message_handler(regexp=r'\d+\s*[/*+-]\s*\d+')
def math(message):
    try:
        bot.reply_to(message, eval(message.text))
    except SyntaxError:
        pass

# Links
@bot.message_handler(commands=['github', 'git'])
def git_link(message):
    bot.send_message(message.chat.id, 'https://github.com/IWDNO/Crypto_bot.git')

#-----------------------------------------------------------------------------------------------------------
# Feedback
@bot.message_handler(commands=['feedback'])
def get_feedback(message):
    name = message.from_user.first_name
    username = message.from_user.username
    msg = bot.send_message(message.chat.id, 'Напишите Ваш отзыв:\n\n_Отмена -> /back_', parse_mode='Markdown')
    bot.register_next_step_handler(msg, _send_feedback, name, username)
    
def _send_feedback(message, name, username):
    # Выход
    if message.text == '/back':
        bot.send_message(message.chat.id, 'Что дальше?')
        return None
    # Отправка
    comment = message.text
    bot.send_message(chat_id=744684673, text=f'Отзыв от {name} (@{username}):\n{comment}')
    bot.send_message(message.chat.id, 'Ваш отзыв отправлен :)')

#-----------------------------------------------------------------------------------------------------------
# Обработчик текста
@bot.message_handler(content_types='text')
def main(message):
    if message.text.lower() in ['привет', 'хай', 'ку', 'hi', 'hello']:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIcbGLKxNeMYAdcVbWFbC5R2M7cOAoBAAIFAAPANk8T-WpfmoJrTXUpBA')
    if message.text.lower() == 'да':
        bot.reply_to(message, 'Пизда')
    if message.text.lower() in ['пока', 'спокойной ночи']:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIcYmLKw8BxFuVVPxT7vl1hDThmzBfuAAILAAOuNp0y11yfBnx4SLkpBA')

#-----------------------------------------------------------------------------------------------------------
# inline keyboard обработчик
@bot.callback_query_handler(func=lambda call: True)
def weather_callback(call):
    global current_song
    
    """ Cryptogarpher """
    if call.data == 'encrypt':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text='Введите сообщение для шифровки:\n\n _назад -> /back_',
            reply_markup=None, parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, _encr)

    if call.data == 'decrypt':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text='Введите сообщение для Расшифровки:\n\n _назад -> /back_', 
            reply_markup=None, parse_mode='Markdown' 
        )
        bot.register_next_step_handler(msg, _decr)     


    """ Weather """
    if call.data == 'Other_city':
        msg = bot.send_message(call.message.chat.id, 'Введите город: ')
        bot.register_next_step_handler(msg, weather)


    """ Song lyrics """
    if call.data == 'show_lyrics':
        result = get_lyrics(current_song.song_id)
        bot.send_message(call.message.chat.id, result, reply_markup=find_song_markup())

    if call.data == 'another_song':
        song(call.message)
        
    if call.data == 'other_results':
        """ message with other results in inline keyboard"""
        songs = current_song.other_songs
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text='Другие результаты: ',
            reply_markup=other_songs_markup(songs), parse_mode='Markdown'
        )
    
    if call.data == 'show_links':
        result = current_song.links
        bot.send_message(call.message.chat.id, result, reply_markup=find_song_markup(), parse_mode='Markdown')

    if call.data.startswith('song'):
        # call.data: 'song/{id}'
        song_id = call.data.split('/')[1]
        
        current_song = get_song_by_id(song_id, current_song.other_songs)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=current_song.text, 
            reply_markup=song_markup(), parse_mode='Markdown' 
        )


@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
