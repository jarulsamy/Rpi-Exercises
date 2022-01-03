#!/usr/bin/env python3


import time

from gpiozero import LED, PWMLED, Button
from helper import PWMLEDSeries


def win_flash(leds, delay=0.05):
    """Flash the LEDs in to indicate the player won."""
    old_values = [led.value for led in leds]
    for _ in range(5):
        for i in leds:
            i.value = 0
        time.sleep(delay)
        for i in leds:
            i.value = 1
        time.sleep(delay)

    # Restore old values
    for i, val in zip(leds, old_values):
        i.value = val


rate = 50
current_led = None


def button_callback(button):
    global current_led, target, rate, leds
    if current_led in targets:
        print("Win!")
        print(current_led)
        rate += 5
        win_flash(leds)
    else:
        print("You missed!")
        print(current_led)


def scroll(leds, button, targets, speed):
    global current_led
    for i in leds:
        current_led = i
        button.when_pressed = button_callback
        i.value = 1
        time.sleep(speed)
        i.value = 0
        time.sleep(speed)


def scroller_game(leds, button, targets):
    while True:
        speed = 1 / rate

        scroll(leds, button, targets, speed)
        scroll(list(reversed(leds)), button, targets, speed)


led_pins = [6, 22, 12, 17, 25, 5, 13, 16, 20, 21]
led_pins = [f"BCM{i}" for i in led_pins]
leds = [PWMLED(i) for i in led_pins]
targets = (leds[4], leds[5])
button = Button("BCM19")

scroller_game(leds, button, targets)
