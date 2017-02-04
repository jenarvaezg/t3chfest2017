from phue import Bridge
from
import time

b = Bridge('10.0.1.3')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
#print b.get_api()

# Prints if light 1 is on or not

# Set brightness of lamp 1 to max
"""b.set_light(1, 'bri', 254)

# Set brightness of lamp 2 to 50%
b.set_light(2, 'bri', 127)

# Turn lamp 2 on
b.set_light(2,'on', True)
b.set_light(3, 'on', True)"""

# You can also control multiple lamps by sending a list as lamp_id
"""b.set_light( [1,2], 'on', True)

# Get the name of a lamp
b.get_light(1, 'name')

# You can also use light names instead of the id
b.get_light('Kitchen')
b.set_light('Kitchen', 'bri', 254)

# Also works with lists
b.set_light(['Bathroom', 'Garage'], 'on', False)

# The set_light method can also take a dictionary as the second argument to do more fancy stuff
# This will turn light 1 on with a transition time of 30 seconds
command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
b.set_light(1, command)
"""
i = 0
j = 0
hue = 0
lights = b.get_light_objects('id')
while True:
    lights[i+1].brightness = j
    lights[i+1].hue = hue
    lights[i+1].transitiontime = 10
    #b.set_light(i+1, 'bri', j, 'hue', hue, transitiontime=1)
    i = (i + 1) % 3
    j  = (j + 10) % 255
    hue = (hue + 10000) % 65280
    print i, j, hue
