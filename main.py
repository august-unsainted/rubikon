from middle.middle import *
import random

port = random.randint(1024, 65535)

eel.init('front')
eel.start('login.html', size=(950, 550), port=port)
