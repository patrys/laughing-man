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
    PIL_MODES = {
        "RGBA" : (cv.IPL_DEPTH_8U, 4),
        "RGB" : (cv.IPL_DEPTH_8U, 3),
        "L"   : (cv.IPL_DEPTH_8U, 1),
        "F"   : (cv.IPL_DEPTH_32F, 1),
    }

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

    def process_image(self, in_image):
        mode = self.PIL_MODES[in_image.mode]
        in_cv_image = cv.CreateImageHeader(in_image.size, *mode)
        cv.SetData(in_cv_image, in_image.tostring())
        faces = self.detect(in_cv_image)
        if faces:
            img_overlay = Image.open(self.OVERLAY_PATH)
            for (x, y, w, h), n in faces:
                new_x = int(x * self.SCALE)
                new_y = int(y * self.SCALE)
                new_w = int(w * self.OVERLAY_SCALE * self.SCALE)
                new_h = int(h * self.OVERLAY_SCALE * self.SCALE)
                offset_w = int((new_w - w * self.SCALE) / 2)
                offset_h = int((new_h - h * self.SCALE) / 2)
                img_overlay_current = img_overlay.resize((new_w, new_h), Image.ANTIALIAS)
                in_image.paste(img_overlay_current, (new_x - offset_w, new_y - offset_h), img_overlay_current)
        return in_image

    def process(self, in_path, out_path):
        img_in = Image.open(in_path)
        self.process_image(img_in)
        img_in.save(out_path, 'JPEG')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Syntax: %s <in_file.jpg> <out_file.jpg>' % sys.argv[0]
        exit(1)
    ff = FaceFinder()
    ff.process(sys.argv[1], sys.argv[2])

