import os
import sys
import cv2
from types import SimpleNamespace

import glob
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.patches import Ellipse
import math

# add paths
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\video_capture") # frame
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\pupil_detectors")
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules")
sys.path.append("C:\\work\\pupil\\pupil_src\\shared_modules\\calibration_routines")
sys.path.append("C:\\work\\pupil\\pupil_src\\tests\\yifan\\ground_truth\\pupil_detection")
#print(sys.path)

import detector_2d, detector_3d
#from calibration_routines import calibration_plugins, gaze_mapping_plugins
from calibration_routines import gaze_mappers
from calibration_routines import finish_calibration, calibrate
from gt_pupil_detection import gt_pupil_info

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


def read_monocular_calibration_data(calibration_path, ground_truth = True):

    #cal_data = [
    #    (*pair["pupil"]["norm_pos"], *pair["ref"]["norm_pos"]) for pair in matched_data
    #]
    pupil_positions = []
    ref_positions = []

    detector2d = detector_2d.Detector_2D()
    if ground_truth:
        pupil_cornea_path = calibration_path + "pupil_cornea\\"
        images = [f for f in glob.glob(pupil_cornea_path + "*.png")]
    else:
        eye_path = calibration_path + "eye\\"
        images = [f for f in glob.glob(eye_path + "*.png")]

    for i in images:
        img = cv2.imread(i)
        frame = Frame(1, img, 1)
        u_r = Roi(frame.img.shape)
        pupil_datum = detector2d.detect(frame,user_roi=u_r,visualize=False)
        pupil_norm = (pupil_datum['norm_pos'][0],pupil_datum['norm_pos'][1])
        pupil_positions.append(pupil_norm)

        f = open(calibration_path+"gaze_in_scene_camera.txt","r")
        for line in f:
            if line.startswith(os.path.splitext(i)[0]):
                ref_norm = (float(line.split(' ')[1]), float(line.split(' ')[2]))
                ref_positions.append(ref_norm)
                break

    cal_data = [(pupil_positions[i][0], pupil_positions[i][1], ref_positions[i][0], ref_positions[i][1]) for i in range(len(ref_positions))]
    return cal_data


def read_monocular_calibration_data_from_file(calibration_path, ground_truth = True):
    #cal_data = [
    #    (*pair["pupil"]["norm_pos"], *pair["ref"]["norm_pos"]) for pair in matched_data
    #]
    pupil_positions = []
    ref_positions = []

    # big mistake to not unify the formats
    if ground_truth:
        pupil_file = open(calibration_path+"pupil_cornea\\pupil_info.txt","r")
        pupils = pupil_file.readlines()
        for i in pupils:
            center = i.split(",")[1]
            x = center.split(" ")[0][1:]
            y = center.split(" ")[1].strip()[:-1]
            if y == "":
                y = center.split(" ")[2].strip()[:-1]
            pupil_info = [float(x)/320, (240-float(y))/240]
            pupil_positions.append(pupil_info)
    else:
        pupil_file = open(calibration_path+"eye\\pupil_info.txt","r")
        pupils = pupil_file.readlines()
        for i in pupils:
            x = i.split(",")[1][1:]
            y = i.split(",")[2].strip()[:-1]
            pupil_info = [float(x)/320, (240-float(y))/240]
            pupil_positions.append(pupil_info)
    
    pupil_file.close()

    gaze_file = open(calibration_path+"gaze_in_scene_camera.txt","r")
    gazes = gaze_file.readlines()
    for i in gazes:
        gaze_info = [float(i.split(" ")[1]), float(i.split(" ")[2])]
        ref_positions.append(gaze_info)
    gaze_file.close()

    cal_data = [(pupil_positions[i][0], pupil_positions[i][1], ref_positions[i][0], ref_positions[i][1]) for i in range(len(ref_positions))]
    return cal_data


def gaze_mapping_result_2d(img_path, calibration="dummy", calibration_path = "", calibration_ground_truth = True):

    ##### prepare data #####
    img = cv2.imread(img_path)
    frame = Frame(1, img, 1)
    u_r = Roi(frame.img.shape)

    detector2d = detector_2d.Detector_2D()
    pupil_datum = detector2d.detect(frame,user_roi=u_r,visualize=False)
    pupil_datum['id'] = 0
    #print(pupil_datum)

    pool = SimpleNamespace()
    pool.active_gaze_mapping_plugin = None
    ##### prepare data #####

    ##### map gaze #####
    if calibration=="dummy":
        pool.active_gaze_mapping_plugin = gaze_mappers.Dummy_Gaze_Mapper(pool)
    elif calibration=="monocular":
        cal_pt_cloud = read_monocular_calibration_data_from_file(calibration_path, calibration_ground_truth)
        #cal_pt_cloud = read_monocular_calibration_data(calibration_path, calibration_ground_truth)
        _, _, params = calibrate.calibrate_2d_polynomial(cal_pt_cloud)
        #print(params)
        pool.active_gaze_mapping_plugin = gaze_mappers.Monocular_Gaze_Mapper(pool, params)

    gaze_data = pool.active_gaze_mapping_plugin.on_pupil_datum(pupil_datum)
    #print(gaze_data)
    ##### map gaze #####
    return gaze_data[0]['norm_pos']
    

def gaze_mapping_with_gt_pupil_2d(img_path, calibration="dummy", calibration_path = "", calibration_ground_truth = True):

    ##### prepare data #####
    img = cv2.imread(img_path)
    frame = Frame(1, img, 1)
    u_r = Roi(frame.img.shape)

    detector2d = detector_2d.Detector_2D()
    pupil_datum = detector2d.detect(frame,user_roi=u_r,visualize=False)

    center, degree, axes = gt_pupil_info(img_path)
    pupil_datum['confidence'] = 1.0
    pupil_datum['diameter'] = max(axes)
    pupil_datum['ellipse']['center'] = center
    pupil_datum['ellipse']['angle'] = degree
    pupil_datum['ellipse']['axes'] = axes
    pupil_datum['norm_pos'] = [center[0]/320, (240-center[1])/240]
    pupil_datum['id'] = 0

    #print(pupil_datum)

    pool = SimpleNamespace()
    pool.active_gaze_mapping_plugin = None
    ##### prepare data #####

    ##### map gaze #####
    if calibration=="dummy":
        pool.active_gaze_mapping_plugin = gaze_mappers.Dummy_Gaze_Mapper(pool)
    elif calibration=="monocular":
        cal_pt_cloud = read_monocular_calibration_data_from_file(calibration_path, calibration_ground_truth)
        #cal_pt_cloud = read_monocular_calibration_data(calibration_path, calibration_ground_truth)
        _, _, params = calibrate.calibrate_2d_polynomial(cal_pt_cloud)
        #print(params)
        pool.active_gaze_mapping_plugin = gaze_mappers.Monocular_Gaze_Mapper(pool, params)

    gaze_data = pool.active_gaze_mapping_plugin.on_pupil_datum(pupil_datum)
    #print(gaze_data)
    ##### map gaze #####
    return gaze_data[0]['norm_pos']


def gaze_mapping_result_3d(img_path):
    img = cv2.imread(img_path)
    frame = Frame(1, img, 1)
    #print(frame)

    detector3d = detector_3d.Detector_3D()
    #print(detector3d)

    Pool = namedtuple('Pool', 'user_dir');
    pool = Pool('/')
    #print(pool)

    u_r = Roi(frame.img.shape)
    #print(u_r)

    detector3d.visualize()
    result = detector3d.detect(frame,user_roi=u_r,visualize=False)
    center_x = result['ellipse']['center'][0]
    center_y = result['ellipse']['center'][1]
    center = [center_x, center_y]
    axes_0 = result['ellipse']['axes'][0]
    axes_1 = result['ellipse']['axes'][1]
    axes = [axes_0, axes_1]
    degree = result['ellipse']['angle']
    print(result)

    fitted_ellipse = Ellipse(center, axes[0], axes[1], degree)

    #frame_img = frame.img
    #fig = plt.figure()
    #ax = fig.add_subplot(1,1,1)
    #ax.add_artist(fitted_ellipse)
    #plt.imshow(frame_img)
    #plt.scatter(center_x, center_y, color = 'red', s=10)

    return None


#calibration_path = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\calibration\\"
### 31 0.20654381811618805 0.6869257688522339
#print(gaze_mapping_result_2d("C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\eye\\0000.png")) #(0.5109901905059815, 0.6302992184956868)
#print(gaze_mapping_result_2d("C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\eye\\0000.png", "monocular", calibration_path, calibration_ground_truth = True)) # (0.20542196146164837, 0.686623505720501)
#print(gaze_mapping_result_2d("C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\eye\\0000.png", "monocular", calibration_path, calibration_ground_truth = False)) # (0.21225852665858191, 0.6983125944450461)


plt.show()

