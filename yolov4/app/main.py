from YoloDetector import YoloDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
from datetime import datetime, timezone
import imutils
import time
import cv2

from util_db import add_to_bd

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()
# vs = VideoStream(src=0).start()
vs=cv2.VideoCapture(-1)
print("Make chahges")
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def detect_object():
    # grab global references to the video stream, output frame, and
    # lock variables
	global vs, outputFrame, lock
    # initialize the detector
	yd = YoloDetector()
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it
		(grb, frame) = vs.read()
		# frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# detect object in the image
		bboxes, time_ex = yd.detect(frame)
		# check to see if motion was found in the frame
		if bboxes is not None:
			for bbox in bboxes:
				(x,y,w,h,cls) = bbox

				dt=datetime.now(timezone.utc)
				
				add_to_bd(bbox, dt, time_ex)

				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
				text="{}".format(str(cls))
				cv2.putText(frame, text, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

		with lock:
			outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
    			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# start a thread that will perform object detection
	t = threading.Thread(target=detect_object)
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()
