#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 17:45:48 2018

@author: Da-sil_t
"""

import cv2
from pprint import pprint

def fist_pos(info):
	cascade = cv2.CascadeClassifier("rsc/fist.xml")
	if cascade.empty():
		print("error cascade")
		exit(-1)

	while (True):
		frame = info.frame
		hand = cascade.detectMultiScale(frame, 1.3, 6)

		if (len(hand) == 1):
			for (x, y, w, h) in hand:
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			return (hand)
