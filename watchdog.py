from phue import Bridge

import time
import threading

b = Bridge('10.0.1.3')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()
lights = b.get_light_objects('id')
