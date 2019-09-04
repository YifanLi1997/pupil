import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.patches import Ellipse
import math


from helpers import generate_ellipse_data, generate_convexhull, fit_ellipse
from visulize import visulize_thresholding, visualize_orginal_images, visulize_ellipse, visualize_hull, visualize_fiited_ellipse, visualize_fitted_ellipse_on_top_of_the_original_image

filepath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\blender imgs\\"
pupil = cv2.imread(filepath+"pupil+cornea.png")
pupil_gray = cv2.cvtColor(pupil, cv2.COLOR_BGR2GRAY)

def compare_threshold(threshold, pupil_gray):
    print("")
    print("The threhold is", threshold)
    
    height = pupil.shape[0]
    width = pupil.shape[1]

    _, thresholded_image = cv2.threshold(pupil_gray, threshold, 255, cv2.THRESH_BINARY)
    ellipse_points,e_x,e_y = generate_ellipse_data(thresholded_image, height, width)
    convexhull, convexhull_points, ch_x, ch_y = generate_convexhull(ellipse_points)
    center, phi, axes = fit_ellipse(ch_x, ch_y)
    fitted_ellipse = Ellipse(center, axes[0] * 2, axes[1] * 2, math.degrees(phi))

    visualize_fitted_ellipse_on_top_of_the_original_image(fitted_ellipse, pupil_gray, xlim0=235, xlim1=300, ylim0=180, ylim1=245)
    

compare_threshold(5, pupil_gray)
compare_threshold(10, pupil_gray)
compare_threshold(15, pupil_gray)
compare_threshold(20, pupil_gray)
compare_threshold(25, pupil_gray)
compare_threshold(29, pupil_gray)
fig1 = plt.figure()
plt.imshow(pupil_gray)
plt.gca().invert_yaxis()
plt.xlim(235,300)
plt.ylim(180,245)

plt.show()