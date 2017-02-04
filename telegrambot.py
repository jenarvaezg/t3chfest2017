import os
import lights
import threading
import twitter_model
import config
import time

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


twitter_thread = None
bot = None
current_view_thread = None
twitter_lock = threading.Lock()


def updateLanguage(new_language):
    twitter_lock.acquire()
    f = open("language.txt", "w")
    f.write(new_language)
    f.close()
    twitter_lock.release()
    print "language is now " + new_language

def updateSentiment(new_sentiment):
    twitter_lock.acquire()
    f = open("sentiment.txt", "w")
    print "new sentiment is"  + str(new_sentiment)
    f.write(str(new_sentiment))
    f.close()
    twitter_lock.release()

def getLanguage():
    twitter_lock.acquire()
    f = open("language.txt", "r")
    lang = f.read()
    f.close()
    twitter_lock.release()
    return lang


def getSentiment():
    twitter_lock.acquire()
    f = open("sentiment.txt", "r")
    sent = float(f.read())
    f.close()
    twitter_lock.release()
    return sent



def party(params):
    stop_view_thread()
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
    stop_view_thread()
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

def stop_view_thread():
    global current_view_thread
    if current_view_thread == None:
        return
    current_view_thread.do_run = False
    current_view_thread.join()
    current_view_thread = None

def follow(params):
    try:
        if params == []:
            return "You should tell me users and/or hashtags, separated by spaces"
        hashtags = []
        users = []
        for field in params:
            if field.startswith("@"):
                users.append(field[1:])
            elif field.startswith("#"):
                hashtags.append(field[1:])
    except e:
        print e
    if len(users) == 0 and len(hashtags) == 0:
        return "You should tell me users and/or hashtags, separated by spaces"
    threading.Thread(target=twitter_model.track, args=(users, hashtags)).start()
    return "Started tracking, no way back!"

def viewUpdatedLanguage(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print "setting flag " + getLanguage()
        lights.set_flag(getLanguage())
        print "flag set"
        time.sleep(5)
    print("Language visualization stopped")

def viewUpdatedSentiment(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print "setting sentiment " + str(getSentiment())
        sentiment = getSentiment()
        print sentiment
        print type(sentiment)
        sentiment = int(sentiment)
        if sentiment == 0:
            lights.set_flag("white")
        elif sentiment > 0:
            lights.set_flag("green")
        else:
            lights.set_flag("red")
        print "flag set"
        time.sleep(5)
    print("Sentiment visualization stopped")

def view(params):
    global current_view_thread
    if params == []:
        return "You should tell me if you want to see language or sentiment"
    if params[0] == "language":
        stop_view_thread()
        current_view_thread = threading.Thread(target=viewUpdatedLanguage, args=("task",))
        current_view_thread.start()
        return "Displaying language"
    if params[0] == "sentiment":
        stop_view_thread()
        current_view_thread = threading.Thread(target=viewUpdatedSentiment, args=("task",))
        current_view_thread.start()
        return "Displaying sentiment"
    return "You should tell me if you want to see language or sentiment"

def tweetStuff(params):
    if params == []:
        return "You should tell me what to tweet"
    to_tweet = " ".join(params)
    twitter_model.post_update(to_tweet)
    return "Tweet sent"

def handler(bot, update):
    print getLanguage()
    global tgbot
    tgbot = bot
    msg = update.message
    tokenized_text = msg.text.split(" ")
    print tokenized_text
    to_return = ""
    if tokenized_text[0] == "/track":
        to_return = follow(tokenized_text[1:])
    elif tokenized_text[0]  == "/flag":
        to_return = flag(tokenized_text[1:])
    elif tokenized_text[0] == "/tweet":
        to_return = tweetStuff(tokenized_text[1:])
    elif tokenized_text[0] == "/party":
        to_return = party(tokenized_text[1:])
    elif tokenized_text[0] == "/on":
        to_return = turn_on(tokenized_text[1:])
    elif tokenized_text[0] == "/off":
        to_return = turn_off(tokenized_text[1:])
    elif tokenized_text[0] == "/view":
        to_return = view(tokenized_text[1:])
    else:
        to_return = "Invalid command"
    update.message.reply_text(to_return)


def start():
    updater = Updater(os.getenv("TELEGRAM_API"))

    dp = updater.dispatcher


    msg_handler = MessageHandler(Filters.command, handler)
    dp.add_handler(msg_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()



if __name__ == "__main__":
    start()
