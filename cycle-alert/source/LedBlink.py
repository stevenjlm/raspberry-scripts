import RPi.GPIO as gpio
import time

DOWN_T = 10 # sec
DOWN_R = 100 # ratio

OUT_PIN = 18

class LedInterface:
    def __init__(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(OUT_PIN, gpio.OUT)

    def pulse_down(self, duration):
        iterations = duration / DOWN_T
        for it in range(int(iterations)):
            gpio.output(OUT_PIN, True)
            time.sleep(DOWN_T / DOWN_R)
            gpio.output(OUT_PIN, False)
            time.sleep(DOWN_T - DOWN_T / DOWN_R)
        return

    def led_on(self, duration):
        gpio.output(OUT_PIN, True)
        time.sleep(duration)
        gpio.output(OUT_PIN, False)
        return
