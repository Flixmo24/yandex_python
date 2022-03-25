from telegram.ext import Updater, MessageHandler, Filters
from pytube import YouTube

import logging
logging.basicConfig(level=logging.DEBUG, filename='logs.txt')

from yandex import sendToScreen
import config


last_url = ""
authorised_users = []

def getVideoUrl(url):

    global last_url

    if url == last_url:  # Second attempt - trying another player
        yt = YouTube(url).streams.first()
        last_url = url
        return yt.url

    last_url = url

    if "https://www.youtube" in url:
        url = url.split("&")[0]  # Removing arguments

    if "https://youtu.be" in url:
        url = "https://www.youtube.com/watch?v=" + url.split("/")[-1]

    # Page parsing and getting video_url here
    return url


def extractUrl(message, context):
    return message.text  # TODO: getting url by entities info


def message_recieved(bot, update, context):

    user_id = update.message.chat_id


    print(update.message)

    if update.message.text == config.bot_password:
        authorised_users.append(user_id)
        bot.send_message(chat_id=update.message.chat_id, text="Успешная авторизация!")
        print(f"Authorised: {user_id}")
        return

    if not user_id in authorised_users:
        bot.send_message(chat_id=update.message.chat_id, text="Доступ закрыт!")
        print("Unauthorised request blocked!")
        return

    url = extractUrl(update.message)
    video_url = getVideoUrl(url)
    result = sendToScreen(video_url)

    print(result)

    bot.send_message(chat_id=update.message.chat_id, text=result + video_url)


updater = Updater(token=config.telegram_bot_token, request_kwargs=config.proxy)



print("Начинаю сбор Видосиков =)")

updater.start_polling()

