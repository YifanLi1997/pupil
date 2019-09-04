import sys
import os
import cv2

from matplotlib import pyplot as plt
import matplotlib
from matplotlib.patches import Ellipse
import math

# add paths
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\video_capture") # frame
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\pupil_detectors")
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\pupil_detectors\\singleeyefitter")
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules")
#print(sys.path)

import detector_2d, detector_3d
from methods import Roi
from collections import namedtuple


class Frame(object):
    """docstring of Frame"""

    def __init__(self, timestamp, img, index):
        self.timestamp = timestamp
        self._img = img
        self.bgr = img
        self.height, self.width, _ = img.shape
        self._gray = None
        self.index = index
        # indicate that the frame does not have a native yuv or jpeg buffer
        self.yuv_buffer = None
        self.jpeg_buffer = None

    @property
    def img(self):
        return self._img

    @property
    def gray(self):
        if self._gray is None:
            self._gray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        return self._gray

    def copy(self):
        return Frame(self.timestamp, self._img.copy(), self.index)


def pupil_detection_result_2d(img_path, visualization = False):
    img = cv2.imread(img_path)
    frame = Frame(1, img, 1)
    #print(frame)

    detector2d = detector_2d.Detector_2D()
    #print(detector2d)

    u_r = Roi(frame.img.shape)
    #print(u_r)

    result = detector2d.detect(frame,user_roi=u_r,visualize=False)
    center_x = result['ellipse']['center'][0]
    center_y = result['ellipse']['center'][1]
    center = [center_x, center_y]
    axes_0 = result['ellipse']['axes'][0]
    axes_1 = result['ellipse']['axes'][1]
    axes = [axes_0, axes_1]
    degree = result['ellipse']['angle']
    #print(result['ellipse'])
    #print(result['norm_pos'])
    #print('')

    if visualization:
        fitted_ellipse = Ellipse(center, axes[0], axes[1], degree)

        frame_img = frame.img
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.add_artist(fitted_ellipse)
        plt.imshow(frame_img)
        plt.scatter(center_x, center_y, color = 'red', s=10)

    return center, degree, axes


def pupil_detection_result_3d(img_path):
    img = cv2.imread(img_path)
    frame = Frame(1, img, 1)
    #print(frame)

    Pool = namedtuple('Pool', 'user_dir');
    pool = Pool('/')
    #print(pool)

    detector3d = detector_3d.Detector_3D()
    #print(detector3d)

    u_r = Roi(frame.img.shape)
    #print(u_r)

    print(detector3d)
    result = detector3d.detect(frame,user_roi=u_r,visualize=False)
    center_x = result['ellipse']['center'][0]
    center_y = result['ellipse']['center'][1]
    center = [center_x, center_y]
    axes_0 = result['ellipse']['axes'][0]
    axes_1 = result['ellipse']['axes'][1]
    axes = [axes_0, axes_1]
    degree = result['ellipse']['angle']

    #fitted_ellipse = Ellipse(center, axes[0], axes[1], degree)

    #frame_img = frame.img
    #fig = plt.figure()
    #ax = fig.add_subplot(1,1,1)
    #ax.add_artist(fitted_ellipse)
    #plt.imshow(frame_img)
    #plt.scatter(center_x, center_y, color = 'red', s=10)

    return center, degree, axes

pupil_detection_result_2d("C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\eye\\0100.png", visualization=True)
plt.show()

def archive():
    ######################## for motion blur ###############################
    #model_3_single = "C:\\Users\\localadmin\\Downloads\\my_attempt\\Blender model3\\single image\\"
    #model_3_video = "C:\\Users\\localadmin\\Downloads\\my_attempt\\Blender model3\\video image\\"
    #model_4_single = "C:\\Users\\localadmin\\Downloads\\my_attempt\\Blender model4\\single image\\"
    #model_4_video = "C:\\Users\\localadmin\\Downloads\\my_attempt\\Blender model4\\video image\\"

    #pupil_result_2d(model_4_single+"0000.png",1)
    #pupil_result_2d(model_4_single+"0001.png",2)
    #pupil_result_2d(model_4_single+"0002.png",3)
    #pupil_result_2d(model_4_single+"0003.png",4)
    #pupil_result_2d(model_4_single+"0004.png",5)
    #pupil_result_2d(model_4_single+"0005.png",6)
    #pupil_result_2d(model_4_single+"0006.png",7)
    #pupil_result_2d(model_4_single+"0007.png",8)
    #pupil_result_2d(model_4_single+"0008.png",9)
    return None