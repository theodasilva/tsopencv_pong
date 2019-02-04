#!/usr/bin/env python3

import numpy as np
import sys
import tensorflow as tf
import os
from threading import Thread
from datetime import datetime
import cv2
import label_map_util
from collections import defaultdict
from pprint import pprint
import tsvision as tsvision

detection_graph = tf.Graph()
sys.path.append("..")
MODEL_NAME = 'hand_inference_graph'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join(MODEL_NAME, 'hand_label_map.pbtxt')
NUM_CLASSES = 1
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
	label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_inference_graph():

	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')
		sess = tf.Session(graph=detection_graph)
	return detection_graph, sess

detection_graph, sess = tsvision.load_inference_graph()

def get_box_points(scores, boxes, image_np):
	for i in range(1):
		if (scores[i] > 0.25):
			height = np.size(image_np, 0)
			width = np.size(image_np, 1)
			(left, right, top, bottom) = (boxes[i][1] * width, boxes[i][3] * width,
										  boxes[i][0] * height, boxes[i][2] * height)
			return np.array([(int(left), int(top), int(right), int(bottom))], dtype=np.int32)
	return ()

def detect_hand(image_np):
	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
	detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
	detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
	detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
	num_detections = detection_graph.get_tensor_by_name('num_detections:0')
	image_np_expanded = np.expand_dims(image_np, axis=0)
	(boxes, scores, classes, num) = sess.run(
		[detection_boxes, detection_scores,
			detection_classes, num_detections],
		feed_dict={image_tensor: image_np_expanded})
	return np.squeeze(boxes), np.squeeze(scores)
