from messages import *
from config import *
from keyboards import *
from func.get_song import get_song, get_lyrics, get_song_by_id
from func.get_weather import get_weather
from func.get_joke import get_joke
from func.crypto import encrypt, decrypt
from func.get_holiday import get_holiday
from func.get_anime import get_anime, new_anime

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
    msg = bot.send_message(message.chat.id, WAIT_MESSAGE)
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
    msg = bot.send_message(message.chat.id, SONG_SEARCH_MESSAGE)
    bot.register_next_step_handler(msg, _song)


def _song(message):
    global current_song
    """ Creates a Song object and sends a message with information about the song to the user """
    try:
        msg = bot.send_message(message.chat.id, WAIT_MESSAGE)
        text = message.text
        current_song = get_song(text)
        print(current_song.other_songs)
        bot.edit_message_text(current_song.text, msg.chat.id, msg.message_id, reply_markup=song_markup())
    except Exception:
        print(Exception)
        bot.edit_message_text(ERROR_MESSAGE, msg.chat.id, msg.message_id)


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
    result = encrypt(message.text)
    bot.send_message(message.chat.id, f'>>> Ваше сообщение (_Нажми_):\n\n`{result}`', parse_mode='Markdown')
    bot.send_message(message.chat.id, NEXT_ACTION_MESSAGE, reply_markup=crypto_markup())


def _decr(message):
    """ Message decryption """
    if message.text == '/back':
            cryptographer(message)
            return None
    try:
        result = decrypt(message.text)
        bot.send_message(message.chat.id, f'>>> Вам написали:\n{result}')
        bot.send_message(message.chat.id, NEXT_ACTION_MESSAGE, reply_markup=crypto_markup())
    except ValueError:
        bot.send_message(message.chat.id, ERROR_MESSAGE)


# Anime search
@bot.message_handler(commands=['anime'])
def anime(message):
    """ Requests anime title"""
    msg = bot.send_message(message.chat.id, ANIME_SEARCH_MESSAGE, reply_markup=recent_anime_markup())
    bot.register_next_step_handler(msg, _get_anime_link)


def _get_anime_link(message):
    """ Get anime data by title"""
    text = message.text
    msg = bot.send_message(message.chat.id, WAIT_MESSAGE)
    result = get_anime(text)
    bot.edit_message_text(result, msg.chat.id, msg.message_id, parse_mode='Markdown')


# Анекдот
@bot.message_handler(commands=['joke'])
def joke(message):
    """ Get random joke """
    msg = bot.send_message(message.chat.id, WAIT_MESSAGE) 
    result = get_joke()
    bot.edit_message_text(result, msg.chat.id, msg.message_id)

# Holiday
@bot.message_handler(commands=['holiday'])
def holiday(message):
    """ Get today's holiday """
    msg = bot.send_message(message.chat.id, WAIT_MESSAGE)
    result = get_holiday()
    bot.edit_message_text(result, message.chat.id, msg.message_id)

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
    bot.send_message(message.chat.id, GIT_LINK)

#-----------------------------------------------------------------------------------------------------------
# Feedback
@bot.message_handler(commands=['feedback'])
def get_feedback(message):
    msg = bot.send_message(message.chat.id, SEND_FEEDBACK_MESSAGE, parse_mode='Markdown')
    bot.register_next_step_handler(msg, _send_feedback)
    
def _send_feedback(message):
    if message.text == '/back':
        bot.send_message(message.chat.id, NEXT_ACTION_MESSAGE)
        return None
    name = message.from_user.first_name
    username = message.from_user.username
    comment = message.text
    bot.send_message(chat_id=744684673, text=f'Отзыв от {name} (@{username}):\n{comment}')
    bot.send_message(message.chat.id, FEEDBACK_SUCCESS_MESSAGE)

#-----------------------------------------------------------------------------------------------------------
# Обработчик текста
@bot.message_handler(content_types='text')
def main(message):
    if message.text.lower() in HELLO_MESSAGES_TO_REPLY:
        bot.send_sticker(message.chat.id, HELLO_STICKER)
    if message.text.lower() in BYE_MESSAGES_TO_REPLY:
        bot.send_sticker(message.chat.id, BYE_STICKER)
    if message.text.lower() == 'да':
        bot.reply_to(message, 'Пизда')

#-----------------------------------------------------------------------------------------------------------
# inline keyboard обработчик
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global current_song
    
    """ Cryptogarpher """
    if call.data == 'encrypt':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=ENCRYPT_MESSAGE,
            reply_markup=None, parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, _encr)
        
    if call.data == 'decrypt':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=DECRYPT_MESSAGE, 
            reply_markup=None, parse_mode='Markdown' 
        )
        bot.register_next_step_handler(msg, _decr)     


    """ Anime """
    if call.data  == 'recent_anime':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.edit_message_text(new_anime(), call.message.chat.id, call.message.message_id, reply_markup=find_anime_markup())
        
    if call.data == 'find_anime':
        anime(call.message)


    """ Weather """
    if call.data == 'Other_city':
        msg = bot.edit_message_text(WEATHER_CHOOSE_CITY_MESSAGE, call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, weather)


    """ Songs """
    if call.data == 'show_lyrics':
        result = get_lyrics(current_song.song_id)
        bot.send_message(call.message.chat.id, result, reply_markup=find_song_markup())

    if call.data == 'another_song':
        song(call.message)
        
    if call.data == 'other_results':
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


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "!", 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    