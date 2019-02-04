#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:38:02 2018

@author: Da-sil_t
"""

import cv2
import numpy as np
import time
from threading import Thread
import tsvision
from fist import fist_pos

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

class information:
    hand = 0
    end = False
    frame = None
    calibrage_max = 100
    f_calibrage = True
    calibrage_haut = ()
    calibrage_bas = ()

class camera(Thread):
    def __init__ (self, info) :
        Thread.__init__(self)
        self._hand_percent = 0
        self.info = info

    def detect_hand(self, frame):
        # TS
        image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, scores = tsvision.detect_hand(image_np)
        hand = tsvision.get_box_points(scores, boxes, image_np)
        return (hand)

    def calibrate(self):
        if (len(self.info.calibrage_haut) == 0):
            self.info.calibrage_haut = fist_pos(self.info)
            if (len(self.info.calibrage_haut) == 1):
                time.sleep(3)
            elif (len(self.info.calibrage_bas) == 0):
                self.info.calibrage_bas = fist_pos(self.info)
                if (len(self.info.calibrage_bas) == 1):
                    self.info.f_calibrage = False
                    self.info.calibrage_min = self.info.calibrage_bas[0][1] - self.info.calibrage_haut[0][1]
                    self.info.calibrage_max = self.info.calibrage_haut[0][1]

    def run(self):
        video = cv2.VideoCapture(0)

        cascade = cv2.CascadeClassifier("rsc/hand.xml")
        tracker = cv2.TrackerKCF_create()
        ok = False

        if cascade.empty():
            print("error cascade")
            exit(-1)
        while (self.info != True):
            if cv2.waitKey(20) == 27:
                cv2.destroyWindow("frame")
                break

            ret, frame = video.read()

            if ret is False:
                print("error video")
                exit(-1)
            self.info.frame = frame

            # update hand value to feed game
            self.info.hand = 10

            cv2.imshow('frame',frame)
