#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from gpiozero import LED, PWMLED, Button

button = Button("BCM19")

led_pins = [6, 22, 12, 17, 25, 5, 13, 16, 20, 21]
led_pins = [f"BCM{i}" for i in led_pins]
# leds = [PWMLED(i) for i in led_pins]
# targets = (leds[4], leds[5])


class PWMLEDSeries:
    def __init__(self, pins):
        self._value = 0
        self._leds = [PWMLED(i) for i in pins]
        for i in self._leds:
            i.value = self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        for i in self._leds:
            i.value = self._value


def flicker(l):
    old_val = l.value
    for i in range(5):
        l.value = 0
        time.sleep(0.05)
        l.value = 1
        time.sleep(0.05)
    l.value = old_val


def win_flash(leds, delay=0.05):
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


def scroll(leds, button, speed):
    for i in leds:
        if button.is_pressed:
            if i in targets:
                win_flash(leds)
                print("win")
                return True
            else:
                return False
        i.value = 1
        time.sleep(speed)
        i.value = 0
        time.sleep(speed)

        # button.wait_for_release()


def scroller_game_driver(leds, button):
    rate = 50
    while True:
        speed = 1 / rate

        if scroll(leds, button, speed) or scroll(list(reversed(leds)), button, speed):
            rate += 5


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
            flicker(led)
        else:
            print("You lost, try again!")
            # time.sleep(0.5)


if __name__ == "__main__":
    led_series = PWMLEDSeries(led_pins)
    fade_game(led_series, button)

    # led_series.value = 1
    # time.sleep(5)
    # led_series.value = 0
    # scroller_game_driver(leds, button)

# num_brightnesses = 20
# step = 1 / num_brightnesses
# brightness = 0.0

# sub = False
# while True:
#     button.wait_for_press()
#     while button.is_pressed:
#         if sub:
#             brightness -= step
#         else:
#             brightness += step

#         if brightness >= 1:
#             brightness = 1
#             sub = True
#         if brightness <= 0:
#             brightness = 0
#             sub = False


#         time.sleep(0.05)
#         led.value = brightness
#         print(led.value)

#     button.wait_for_release()

# button.wait_for_press()
# brightness += step
# if brightness > 1:
#     brightness = 0.0

# led.value = brightness
# button.wait_for_release()

# button.wait_for_release()
# print("released")
# led.off()


"""
BUTTON_PIN = 19
LED_PIN = 16



GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)



# handle the button event
def rising(pin):
    # turn LED on
    print(pin)
    GPIO.output(LED_PIN, True)
    print("rising")

def falling(pin):
    # turn LED off
    print(pin)
    GPIO.output(LED_PIN, False)
    print("falling")

# GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=rising)
# GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=falling)

try:
    while True:
        pass
except:
    GPIO.cleanup()
"""
