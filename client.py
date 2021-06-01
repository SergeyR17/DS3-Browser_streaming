#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from receiver import Receiver

min_area = 15
channel = False
app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():
    """Video streaming home page."""

    if request.method == "POST":
        global min_area
        min_area = int(request.form['min_area'])
        print('MINAREA:', min_area)
        print('MINAREA type:', type(min_area))
        
        global channel
        channel = int(request.form['channels'])
        print('DIF chan:', channel)
        return render_template('index.html', min_area=min_area)
    
    
    #render_template('index.html', min_area=min_area)
    return render_template('index.html')


def gen(receiver,min_area, channel):
    """Video streaming generator function."""
    while True:
        
        frame = receiver.get_frame(min_area, channel)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed' )
def video_feed():

    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Receiver(), min_area, channel),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)