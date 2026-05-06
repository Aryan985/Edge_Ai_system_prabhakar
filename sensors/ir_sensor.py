# sensors/ir_sensor.py

try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

from config import IR_PIN

if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN)


def detect_ir():
    if GPIO is None:
        return False  # fake

    return GPIO.input(IR_PIN) == 0