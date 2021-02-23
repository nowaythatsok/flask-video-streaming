#!/usr/bin/env python
import eventlet
eventlet.monkey_patch()

from importlib import import_module
import os
from flask import Flask, render_template, Response

import time
print("is_monkey_patched(time):", eventlet.patcher.is_monkey_patched(time))

from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)#, async_mode="threading")


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3', '4', '5', '6', '7']]

    while True:
        time.sleep(1)
        i = int(time.time()) % 7
        frame = imgs[i]
        print("gen yielding", i)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', threaded=True)#, debug=True)
    socketio.run(app, host='0.0.0.0')#, debug=True)