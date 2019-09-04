import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.patches import Ellipse
import math

from helpers import generate_ellipse_data, generate_convexhull, fit_ellipse
from visulize import visulize_thresholding, visualize_orginal_images, visulize_ellipse, visualize_hull, visualize_fiited_ellipse, visualize_fitted_ellipse_on_top_of_the_original_image


def gt_pupil_info(filepath, visualization = False):
    # read pictures
    pupil = cv2.imread(filepath)
    pupil_gray = cv2.cvtColor(pupil, cv2.COLOR_BGR2GRAY)

    height = pupil.shape[0]
    width = pupil.shape[1]

    _, thresholded_image = cv2.threshold(pupil_gray, 20, 255, cv2.THRESH_BINARY)
    ellipse_points,e_x,e_y = generate_ellipse_data(thresholded_image, height, width)
    convexhull, convexhull_points, ch_x, ch_y = generate_convexhull(ellipse_points)

    center, degree, axes = fit_ellipse(ch_x, ch_y)

    if visualization:
        fitted_ellipse = Ellipse(center, axes[0], axes[1], degree)

        visualize_fitted_ellipse_on_top_of_the_original_image(fitted_ellipse, pupil_gray)

        #visualize_fiited_ellipse(fitted_ellipse)
        #fig1 = plt.figure()
        #plt.imshow(pupil_gray)
        #plt.gca().invert_yaxis()

        #visualize_hull(ellipse_points,convexhull)

        #visulize_ellipse(ellipse_points,240,300,180,250)
        #visulize_ellipse(ellipse_points)

        #visualize_orginal_images(eye, pupil, eye_gray, pupil_gray)

        #fig2 = plt.figure()
        #visulize_thresholding(pupil_gray, 30, fig2, 1,2,1) # visulize_thresholding(data, threshold, fig, fig_x, fig_y, fig_order, xlim0=0, xlim1=640, ylim0=0, ylim1=480)
        #fig2.tight_layout()

        plt.show()

    return center, degree, axes


gt_pupil_info("C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\control\\pupil_cornea\\0100.png", visualization=True)
plt.show()