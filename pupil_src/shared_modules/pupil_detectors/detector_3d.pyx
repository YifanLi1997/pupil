#define _ENABLE_EXTENDED_ALIGNED_STORAGE

"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2019 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""

# cython: profile=False
import math
from collections import namedtuple

import cv2
import glfw
import numpy as np
from cython.operator cimport dereference as deref
from pyglui import ui
from pyglui.cygl.utils import draw_gl_texture

from coarse_pupil cimport center_surround
from detector cimport *
from detector_utils cimport *
from methods import Roi, normalize
from gl_utils import (
    adjust_gl_view,
    clear_gl_screen,
    basic_gl_setup,
    make_coord_system_norm_based,
    make_coord_system_pixel_based,
)
from plugin import Plugin
from visualizer_3d import Eye_Visualizer


cdef class Detector_3D:

    cdef Detector2D* detector2DPtr
    cdef EyeModelFitter *detector3DPtr

    cdef dict detectProperties2D, detectProperties3D
    cdef object debugVisualizer3D
    cdef object pyResult3D
    cdef readonly object g_pool
    cdef readonly basestring uniqueness
    cdef public object menu
    cdef public object menu_icon
    cdef readonly basestring icon_chr
    cdef readonly basestring icon_font

    def __cinit__(self, g_pool = None, settings = None):
        self.detector2DPtr = new Detector2D()
        focal_length = 620.
        '''
        K for 30hz eye cam:
        [ 634.16873016    0.          343.40537637]
        [   0.          605.57862234  252.3924477 ]
        [   0.            0.            1.        ]
        '''
        #region_band_width = 5
        #region_step_epsilon = 0.5
        self.detector3DPtr = new EyeModelFitter(focal_length)

    def __init__(self, g_pool = None, settings = None ):

        #debug window
        self.debugVisualizer3D = Eye_Visualizer(g_pool ,self.detector3DPtr.getFocalLength() )
        self.g_pool = g_pool
        self.uniqueness = 'unique'
        self.icon_font = 'pupil_icons'
        self.icon_chr = chr(0xec19)
        self.detectProperties2D = settings['2D_Settings'] if settings else {}
        self.detectProperties3D = settings['3D_Settings'] if settings else {}

        if not self.detectProperties2D:
            self.detectProperties2D["coarse_detection"] = True
            self.detectProperties2D["coarse_filter_min"] = 128
            self.detectProperties2D["coarse_filter_max"] = 280
            self.detectProperties2D["intensity_range"] = 23
            self.detectProperties2D["blur_size"] = 5
            self.detectProperties2D["canny_treshold"] = 160
            self.detectProperties2D["canny_ration"] = 2
            self.detectProperties2D["canny_aperture"] = 5
            self.detectProperties2D["pupil_size_max"] = 100
            self.detectProperties2D["pupil_size_min"] = 10
            self.detectProperties2D["strong_perimeter_ratio_range_min"] = 0.8
            self.detectProperties2D["strong_perimeter_ratio_range_max"] = 1.1
            self.detectProperties2D["strong_area_ratio_range_min"] = 0.6
            self.detectProperties2D["strong_area_ratio_range_max"] = 1.1
            self.detectProperties2D["contour_size_min"] = 5
            self.detectProperties2D["ellipse_roundness_ratio"] = 0.1
            self.detectProperties2D["initial_ellipse_fit_treshhold"] = 1.8
            self.detectProperties2D["final_perimeter_ratio_range_min"] = 0.6
            self.detectProperties2D["final_perimeter_ratio_range_max"] = 1.2
            self.detectProperties2D["ellipse_true_support_min_dist"] = 2.5
            self.detectProperties2D["support_pixel_ratio_exponent"] = 2.0


        if not self.detectProperties3D:
            self.detectProperties3D["model_sensitivity"] = 0.997

    def get_settings(self):
        return {'2D_Settings': self.detectProperties2D , '3D_Settings' : self.detectProperties3D }

    def on_resolution_change(self, old_size, new_size):
        self.detectProperties2D["pupil_size_max"] *= new_size[0] / old_size[0]
        self.detectProperties2D["pupil_size_min"] *= new_size[0] / old_size[0]

    def __dealloc__(self):
      del self.detector2DPtr
      del self.detector3DPtr

    def detect(self, frame, user_roi, visualize, pause = False ):

        image_width = frame.width
        image_height = frame.height


        cdef unsigned char[:,::1] img = frame.gray
        cdef Mat cv_image = Mat(image_height, image_width, CV_8UC1, <void *> &img[0,0] )

        cdef unsigned char[:,:,:] img_color
        cdef Mat cv_image_color
        cdef Mat debug_image

        if visualize:
            img_color = frame.img
            cv_image_color = Mat(image_height, image_width, CV_8UC3, <void *> &img_color[0,0,0] )


        roi = Roi((0,0))
        roi.set( user_roi.get() )
        roi_x = roi.get()[0]
        roi_y = roi.get()[1]
        roi_width  = roi.get()[2] - roi.get()[0]
        roi_height  = roi.get()[3] - roi.get()[1]
        cdef int[:,::1] integral

        if self.detectProperties2D['coarse_detection'] and roi_width*roi_height > 320*240:
            scale = 2 # half the integral image. boost up integral
            # TODO maybe implement our own Integral so we don't have to half the image
            user_roi_image = frame.gray[user_roi.view]
            integral = cv2.integral(user_roi_image[::scale,::scale])
            coarse_filter_max = self.detectProperties2D['coarse_filter_max']
            coarse_filter_min = self.detectProperties2D['coarse_filter_min']
            bounding_box , good_ones , bad_ones = center_surround( integral, coarse_filter_min/scale , coarse_filter_max/scale )

            if visualize:
                # !! uncomment this to visualize coarse detection
                  # draw the candidates
                for v  in bad_ones:
                    p_x,p_y,w,response = v
                    x = p_x * scale + roi_x
                    y = p_y * scale + roi_y
                    width = w*scale
                    cv2.rectangle( frame.img , (x,y) , (x+width , y+width) , (0,0,255)  )

                # # draw the candidates
                for v  in good_ones:
                    p_x,p_y,w,response = v
                    x = p_x * scale + roi_x
                    y = p_y * scale + roi_y
                    width = w*scale
                    cv2.rectangle( frame.img , (x,y) , (x+width , y+width) , (255,255,0)  )
                    #responseText = '{:2f}'.format(response)
                    #cv2.putText(frame.img, responseText,(int(x+width*0.5) , int(y+width*0.5)), cv2.FONT_HERSHEY_PLAIN,0.7,(0,0,255) , 1 )

                    #center = (int(x+width*0.5) , int(y+width*0.5))
                    #cv2.circle( frame.img , center , 5 , (255,0,255) , -1  )


            x1 , y1 , x2, y2 = bounding_box
            width = x2 - x1
            height = y2 - y1
            roi_x = x1 * scale + roi_x
            roi_y = y1 * scale + roi_y
            roi_width = width*scale
            roi_height = height*scale
            roi.set((roi_x, roi_y, roi_x+roi_width, roi_y+roi_height))

        # every coordinates in the result are relative to the current ROI
        cpp2DResultPtr =  self.detector2DPtr.detect(self.detectProperties2D, cv_image, cv_image_color, debug_image, Rect_[int](roi_x,roi_y,roi_width,roi_height), visualize , False ) #we don't use debug image in 3d model

        deref(cpp2DResultPtr).timestamp = frame.timestamp #timestamp doesn't get set elsewhere and it is needt in detector3D

        ######### 3D Model Part ############
        debugDetector =  self.debugVisualizer3D.window
        cdef Detector3DResult cpp3DResult  = self.detector3DPtr.updateAndDetect( cpp2DResultPtr , self.detectProperties3D, debugDetector)

        pyResult = convertTo3DPythonResult(cpp3DResult , frame )

        if debugDetector:
            self.pyResult3D = prepareForVisualization3D(cpp3DResult)

        return pyResult


    def cleanup(self):
        self.debugVisualizer3D.close_window() # if we change detectors, be sure debug window is also closed

    @property
    def pretty_class_name(self):
        return 'Pupil Detector 3D'

    def init_ui(self):
        Plugin.add_menu(self)
        self.menu.label = self.pretty_class_name
        info = ui.Info_Text("Switch to the algorithm display mode to see a visualization of pupil detection parameters overlaid on the eye video. "\
                                +"Adjust the pupil intensity range so that the pupil is fully overlaid with blue. "\
                                +"Adjust the pupil min and pupil max ranges (red circles) so that the detected pupil size (green circle) is within the bounds.")
        self.menu.append(info)
        #self.menu.append(ui.Switch('coarse_detection',self.detectProperties2D,label='Use coarse detection'))
        self.menu.append(ui.Slider('intensity_range',self.detectProperties2D,label='Pupil intensity range',min=0,max=60,step=1))
        self.menu.append(ui.Slider('pupil_size_min',self.detectProperties2D,label='Pupil min',min=1,max=250,step=1))
        self.menu.append(ui.Slider('pupil_size_max',self.detectProperties2D,label='Pupil max',min=50,max=400,step=1))
        #self.menu.append(ui.Slider('ellipse_roundness_ratio',self.detectProperties2D,min=0.01,max=1.0,step=0.01))
        #self.menu.append(ui.Slider('initial_ellipse_fit_treshhold',self.detectProperties2D,min=0.01,max=6.0,step=0.01))
        #self.menu.append(ui.Slider('canny_treshold',self.detectProperties2D,min=1,max=1000,step=1))
        #self.menu.append(ui.Slider('canny_ration',self.detectProperties2D,min=1,max=4,step=1))
        info_3d = ui.Info_Text("Open the debug window to see a visualization of the 3D pupil detection." )
        self.menu.append(info_3d)
        self.menu.append(ui.Button('Reset 3D model', self.reset_3D_Model ))
        self.menu.append(ui.Button('Open debug window',self.toggle_window))
        self.menu.append(ui.Slider('model_sensitivity',self.detectProperties3D,label='Model sensitivity',min=0.990,max=1.0,step=0.0001))
        self.menu[-1].display_format = '%0.4f'
        # self.menu.append(ui.Slider('pupil_radius_min',self.detectProperties3D,label='Pupil min radius', min=1.0,max= 8.0,step=0.1))
        # self.menu.append(ui.Slider('pupil_radius_max',self.detectProperties3D,label='Pupil max radius', min=1.0,max=8.0,step=0.1))
        # self.menu.append(ui.Slider('max_fit_residual',self.detectProperties3D,label='3D fit max residual', min=0.00,max=0.1,step=0.0001))
        # self.menu.append(ui.Slider('max_circle_variance',self.detectProperties3D,label='3D fit max circle variance', min=0.01,max=2.0,step=0.001))
        # self.menu.append(ui.Slider('combine_evaluation_max',self.detectProperties3D,label='3D fit max combinations eval', min=500,max=50000,step=5000))
        # self.menu.append(ui.Slider('combine_depth_max',self.detectProperties3D,label='3D fit max combination depth', min=10,max=5000,step=20))
        #advanced_controls_menu = ui.Growing_Menu('Advanced Controls')
        #advanced_controls_menu.append(ui.Slider('contour_size_min',self.detectProperties2D,label='Contour min length',min=1,max=200,step=1))
        #sidebar.append(advanced_controls_menu)

    def deinit_ui(self):
        Plugin.remove_menu(self)

    def reset_3D_Model(self):
         self.detector3DPtr.reset()

    def toggle_window(self):
        if not self.debugVisualizer3D.window:
            self.debugVisualizer3D.open_window()
        else:
            self.debugVisualizer3D.close_window()

    def visualize(self):
        if self.debugVisualizer3D.window:
            self.debugVisualizer3D.update_window(self.g_pool, self.pyResult3D)

    def set_2d_detector_property(self, name, value):
        set_detector_property(self.detectProperties2D, name, value)

    def set_3d_detector_property(self, name, value):
        set_detector_property(self.detectProperties3D, name, value)

    def get_detector_properties(self):
        return {"2d": self.detectProperties2D, "3d": self.detectProperties3D}
