#!/usr/bin/python3


import os
import lights
import threading
import twitter_model
import config

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


twitter_thread = None

def party(params):
    if params == []:
        lights.partyLikeIts1999()
        return "Party started"
    lights.stop_party()
    return "Party stopped"

def turn_on(params):
    if params == []:
        lights.turn_on(-1)
        return "Turned on all lights"
    try:
        lights.turn_on(int(params[0]))
    except e:
        print e
        return "Error turning on", params[0]
    return "Turned on", params[0]


def turn_off(params):
    if params == []:
        lights.turn_off(-1)
        return "Turned off all lights"
    try:
        lights.turn_off(int(params[0]))
    except e:
        print e
        return "Error turning off", params[0]
    return "Turned off", params[0]

def flag(params):
    try:
        if params == []:
            print "go default"
            lights.set_flag()
            return "Set default flag"
        lights.set_flag(params[0]) #to-do
        return "Set flag to ", params[0]
    except e:
        print e
        return "Error setting flag"

def handler(bot, update):
    msg = update.message
    tokenized_text = msg.text.split(" ")
    print tokenized_text
    to_return = ""
    if tokenized_text[0] == "/follow":
        to_return = follow(tokenized_text[1:])
    elif tokenized_text[0]  == "/flag":
        to_return = flag(tokenized_text[1:])
    elif tokenized_text[0] == "/send":
        to_return = sendStuff(tokenized_text[1:])
    elif tokenized_text[0] == "/party":
        to_return = party(tokenized_text[1:])
    elif tokenized_text[0] == "/on":
        to_return = turn_on(tokenized_text[1:])
    elif tokenized_text[0] == "/off":
        to_return = turn_off(tokenized_text[1:])
    else:
        to_return = "Invalid command"
    update.message.reply_text(to_return)


def start():
    print "STARTING"
    global twitter_thread
    twitter_thread = threading.Thread(target=twitter_model.track, args=(config.users, config.hashtags))
    twitter_thread.start()
    updater = Updater(os.getenv("TELEGRAM_API"))

    dp = updater.dispatcher


    msg_handler = MessageHandler(Filters.command, handler)
    dp.add_handler(msg_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    start()
