#!/usr/bin/env python
from importlib import import_module
import os
import io
try:
   from StringIO import StringIO
except ImportError:
    from io import StringIO
from flask import Flask, render_template, Response, request, jsonify

# Raspberry Pi camera module (requires picamera package)
from camera import Camera
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.next_frame()
        image = Image.fromarray(frame)
        with io.BytesIO() as output:
          image.save(output, format="PNG")
          #turn to jpeg....
          yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + output.getvalue() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera(training_mode=False)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_gesture', methods=['POST'])
def set_gesture():
   print(request.json)
   return jsonify(request.json)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
