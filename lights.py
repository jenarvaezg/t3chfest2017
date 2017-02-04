from phue import Bridge

import time
import threading

b = Bridge('10.0.1.3')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()
lights = b.get_light_objects('id')
#first right then left then middle
flag_colors_dict = {"es": [0, 0, 13750], 'pt': [0, 25500, 0], 'fr': [0, 46920, 30000],
    'white': [30000, 30000, 30000], 'green': [25500, 25500, 25500], 'red': [0, 0, 0],
    'en': [0, 30000, 46920]
}

partyThread = ""


def get_status():
    status = {"on" : 0, 'reachable': 0, 'lights': []}
    for light in lights:
        if lights[light].on:
            status['on'] = status['on'] + 1
        if lights[light].reachable:
            status['reachable'] = status['reachable'] + 1
        l = {}
        l['hue'] = lights[light].hue
        l['brightness'] = lights[light].brightness
        l['id'] = light
        l['on'] = lights[light].on
        l['reachable'] = lights[light].reachable
        status['lights'].append(l)
    return status


def run_party(arg):
    t = threading.currentThread()
    i = 0
    j = 0
    hue = 0
    lights = b.get_light_objects('id')
    while getattr(t, "do_run", True):
        lights[i+1].brightness = j
        lights[i+1].hue = hue
        lights[i+1].transitiontime = 10
        i = (i + 1) % 3
        j  = (j + 10) % 255
        hue = (hue + 10000) % 65280
        print i, j, hue
    print("Party stopped")


def stop_party():
    global partyThread
    if partyThread == "":
        return
    partyThread.do_run = False
    partyThread.join()
    partyThread = ""


def partyLikeIts1999():
    global partyThread
    turn_on(-1)
    if partyThread != "":
        return
    partyThread = threading.Thread(target=run_party, args=("task",))
    partyThread.start()



def turn_on(light_id):
    stop_party()
    if light_id == -1:
        for light in lights:
            lights[light].on = True
            lights[light].brightness = 255
    else:
        lights[light_id].on = True

def turn_off(light_id):
    stop_party()
    if light_id == -1:
        for light in lights:
            lights[light].on = False
    else:
        lights[light_id].on = False

def set_flag(country_code="es"):
    stop_party()
    turn_on(-1)
    flag_colors = flag_colors_dict.get(country_code, None)
    if flag_colors is None:
        return
    light_id = 1
    for color in flag_colors:
        lights[light_id].hue = color
        light_id += 1

def alarm():
    turn_on(-1)
    for light in lights:
        lights[light].hue = 0
        lights[light].brightness = 255
    time.sleep(1)
    for light in lights:
        lights[light].brightness = 0
    time.sleep(1)
    for light in lights:
        lights[light].brightness = 255
    time.sleep(1)
    for light in lights:
        lights[light].brightness = 0
    time.sleep(1)
    for light in lights:
        lights[light].brightness = 255

def init():
    for light in lights:
        lights[light].brightness = 255
        lights[light].hue = 30000

init()

if __name__ == "__main__":
    """partyLikeIts1999()
    print "going to sleep"
    time.sleep(5)
    print "woke up"
    stop_party()
    print "bye"""
    alarm()
