# USAGE
import numpy as np
import time
import cv2
import os

class YoloDetector():
	def __init__(self, confidence=0.5, threshold=0.3, yolo_path='cfg'):
		self.confidence=confidence
		self.threshold=threshold
		self.labelsPath=os.path.sep.join([yolo_path, "coco.names"])
		self.weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
		self.configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])

		self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
		self.ln = self.net.getLayerNames()

		# self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
		self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

	def detect(self, image):
		# load our YOLO object detector trained on COCO dataset (80 classes)
		# and determine only the *output* layer names that we need from YOLO
		LABELS=open(self.labelsPath).read().strip().split("\n")

		(W,H)=image.shape[:2]
		# construct a blob from the input frame and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes
		# and associated probabilities
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
		self.net.setInput(blob)
		start = time.time()
		layerOutputs = self.net.forward(self.ln)
		end = time.time()

		time_ex=end-start
		# initialize our lists of detected bounding boxes, confidences,
		# and class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability)
				# of the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.confidence:
					# scale the bounding box coordinates back relative to
					# the size of the image, keeping in mind that YOLO
					# actually returns the center (x, y)-coordinates of
					# the bounding box followed by the boxes' width and
					# height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top
					# and and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates,
					# confidences, and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping
		# bounding boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

		detectList=[]
		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
				detectList.append((x,y,w,h,classIDs[i]))

		return detectList, time_ex
