#!/usr/bin/env python3

import time

from gpiozero import LED, PWMLED, Button
from helper import PWMLEDSeries


def win_flash(led, delay=0.05):
    """Flash the LEDs in to indicate the player won."""
    old_value = led.value
    for _ in range(5):
        led.value = 0
        time.sleep(delay)
        led.value = 1
        time.sleep(delay)

    # Restore old values
    led.value = old_value


def fade_game(led, button, delay=0.05):
    num_steps = 20
    step = 1 / num_steps

    while True:
        sub = False
        brightness = 0
        led.value = 0

        button.wait_for_press()

        while button.is_pressed:
            if sub:
                brightness -= step
            else:
                brightness += step

            if brightness >= 1:
                brightness = 1
                sub = True
            elif brightness <= 0:
                brightness = 0
                sub = False

            time.sleep(delay)
            led.value = brightness

        button.wait_for_release()
        if round(led.value, 2) == 0:
            print("You win!")
            win_flash(led)
        else:
            print("Try again!")


led_pins = [6, 22, 12, 17, 25, 5, 13, 16, 20, 21]
led_pins = [f"BCM{i}" for i in led_pins]
led_series = PWMLEDSeries(led_pins)
button = Button("BCM19")

fade_game(led_series, button)
