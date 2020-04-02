#!/usr/bin/env python
from importlib import import_module
import os
from os import path, mkdir
import io
import errno
import time
try:
   from StringIO import StringIO
except ImportError:
    from io import StringIO
from flask import Flask, render_template, Response, request, jsonify

# Raspberry Pi camera module (requires picamera package)
from camera import Camera
from PIL import Image
clients=0
camera = Camera(training_mode=False)
mygenerator = None
gesturetype = None
readyForImage = True

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    readyForImage = True
    num_frames = 0
    while readyForImage:
        frame = camera.next_frame()
        image = Image.fromarray(frame)
        with io.BytesIO() as output:
          image.save(output, format="PNG")
          if gesturetype is not None:
            dirname = path.join("./tdata", gesturetype)
            print("dirname is", dirname)
            try:
              mkdir(dirname)
            except OSError as err:
              if err.errno != errno.EEXIST:
                raise err 

            filename = (path.join(dirname, '%05d.png') % num_frames)
            image.save(filename, "PNG")
            num_frames += 1
          #turn to jpeg....
          yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + output.getvalue() + b'\r\n')


@app.route('/done')
def done():
  global gesturetype
  print("setting gesture category to none")
  gesturetype=None
  return "success"
 
@app.route('/video_feed')
def video_feed():
    global clients, mygenerator, readyForImage
    clients += 1
    print("video feed called!!", clients)
    """Video streaming route. Put this in the src attribute of an img tag."""
    if mygenerator is not None:
      readyForImage=False
      print("closed!!")

    try:
      mygenerator = gen(camera)
    except:
      print("error generating generator!")

    return Response(mygenerator, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/record/<gesture>', methods=['GET'])
def record(gesture):
   global gesturetype
   gesturetype = gesture
   print("set gestture type to", gesturetype)
   return "success"

@app.route('/set_gesture', methods=['POST'])
def set_gesture():
   print(request.json)
   return jsonify(request.json)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
