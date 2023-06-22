from pynput import keyboard
from pynput.keyboard import Key, Controller
from random import randint
import time

kb = Controller()

combos = [ {keyboard.Key.num_lock} ]

current = set()

def execute():
    for _ in range(randint(3, 6)):
        kb.press(chr(randint(ord('a'),ord('z'))))

def on_press(key):
    if any([key in combo for combo in combos]):
        current.add(key)
        
        if any(all(k in current for k in combo) for combo in combos):
            execute()

def on_release(key):
    if any([key in combo for combo in combos]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    time.sleep(5)