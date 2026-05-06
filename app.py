# app.py

from flask import Flask, render_template, Response, jsonify
import cv2

from ai.detect import detect_objects
from sensors.ultrasonic import get_distance
from sensors.ir_sensor import detect_ir
from fusion.logic import check_hazard
from config import *

try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

# LED setup
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
app = Flask(__name__)

camera = cv2.VideoCapture(CAMERA_INDEX)

status_data = {
    "danger": False,
    "distance": 0
}

def generate_frames():
    global status_data

    while True:
        success, frame = camera.read()
        if not success:
            break

        # AI detection
        frame, ai_detected = detect_objects(frame)

        # Sensor data
        distance = get_distance()
        ir = detect_ir()

        # Decision
        danger = check_hazard(ai_detected, distance, ir)

        status_data["danger"] = danger
        status_data["distance"] = distance

        # LED control
        if GPIO:
            if danger:
                GPIO.output(RED_LED, True)
                GPIO.output(GREEN_LED, False)
            else:
                GPIO.output(RED_LED, False)
                GPIO.output(GREEN_LED, True)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def status():
    return jsonify(status_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)