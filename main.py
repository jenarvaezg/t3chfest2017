import lights
import twitter_model
import telegrambot
import threading


def main():
    print "start telegram"
    telegram_thread = threading.Thread(target=telegrambot.start)
    telegram_thread.start()
    print "OK"


    telegram_thread.join()


if __name__ == "__main__":
    main()
