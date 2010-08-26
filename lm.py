#!/usr/bin/env python

import sys, os

from PIL import Image
import cv

class FaceFinder(object):
    CASCADE = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    HAAR_SCALE = 1.2
    MIN_NEIGHBORS = 2
    MIN_SIZE = (20, 20)
    OVERLAY_PATH = 'logo.png'
    OVERLAY_SCALE = 1.7
    SCALE = 2

    def detect(self, img):
        gray = cv.CreateImage((img.width, img.height), 8, 1)
        small_img = cv.CreateImage(
                (
                    cv.Round(img.width / self.SCALE),
                    cv.Round(img.height / self.SCALE)
                ), 8, 1)
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        return cv.HaarDetectObjects(small_img, self.CASCADE, cv.CreateMemStorage(0),
                self.HAAR_SCALE, self.MIN_NEIGHBORS, 0, self.MIN_SIZE)

    def process(self, in_path, out_path):
        img = cv.LoadImage(in_path, 1)
        faces = self.detect(img)
        if faces:
            img_in = Image.open(in_path)
            img_overlay = Image.open(self.OVERLAY_PATH)
            for (x, y, w, h), n in faces:
                new_x = int(x * self.SCALE)
                new_y = int(y * self.SCALE)
                new_w = int(w * self.OVERLAY_SCALE * self.SCALE)
                new_h = int(h * self.OVERLAY_SCALE * self.SCALE)
                offset_w = int((new_w - w * self.SCALE) / 2)
                offset_h = int((new_h - h * self.SCALE) / 2)
                img_overlay_current = img_overlay.resize((new_w, new_h), Image.ANTIALIAS)
                img_in.paste(img_overlay_current, (new_x - offset_w, new_y - offset_h), img_overlay_current)
            img_in.save(out_path, 'JPEG')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Syntax: %s <in_file.jpg> <out_file.jpg>' % sys.argv[0]
        exit(1)
    ff = FaceFinder()
    ff.process(sys.argv[1], sys.argv[2])

