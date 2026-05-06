# sensors/ultrasonic.py

try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

import time
from config import TRIG, ECHO


# Setup only if running on Raspberry Pi
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


def get_distance():
    # 💻 PC MODE (fake data)
    if GPIO is None:
        return 100  # fake constant distance

    # 🟢 Raspberry Pi real logic
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        stop = time.time()

    duration = stop - start
    distance = duration * 17150

    return round(distance, 2)