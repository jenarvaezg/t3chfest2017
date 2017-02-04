from phue import Bridge

import time
import threading
import mailgun
import telegrambot
import lights
import config

b = Bridge('10.0.1.3')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()
light_o = b.get_light_objects()
def get_reachable():
    total = 0
    for light in light_o:
        if light.reachable:
            total += 1
    return total

def monitorize(args):
    global lights
    t = threading.currentThread()
    reachable_before = get_reachable()
    print reachable_before
    while getattr(t, "do_run", True):
        if reachable_before != get_reachable():
            telegrambot.stop_view_thread()
            lights.stop_party()
            lights.alarm()
            mailgun.send_mail(config.address, "Number of HUEs changed, watch out!")
            return
    print("Monitorization visualization stopped")


if __name__ == "__main__":
    monitorize("a")
