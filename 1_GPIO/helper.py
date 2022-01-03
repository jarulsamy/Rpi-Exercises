#!/usr/bin/env python3


from gpiozero import PWMLED, Button


class PWMLEDSeries:
    """Treat several LEDs as a single gpiozero.PWMLED object."""

    def __init__(self, pins):
        """Initialize all the LEDs from the corresponding pin numbers."""
        self._value = 0
        self._leds = [PWMLED(i) for i in pins]
        for i in self._leds:
            i.value = self.value

    @property
    def value(self):
        """Return the current LED brightness value."""
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        for i in self._leds:
            i.value = self._value
