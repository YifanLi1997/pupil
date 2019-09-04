import numpy as np
import cv2
import math
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from ellipse_fitting_from_nicky import fitEllipse, ellipse_center, ellipse_angle_of_rotation, ellipse_axis_length, ellipse_angle_of_rotation2

def generate_ellipse_data(thresholded_image, height = 480, width = 640):
    ellipse = []
    for h in range(height):
        for w in range(width):
            if thresholded_image[h][w] != 255:
                ellipse.append([h,w])
    
    x, y = zip(*ellipse)
    ellipse_points = np.array(ellipse)
    #print(ellipse_points)
    x = np.array(x)
    y = np.array(y)
    return ellipse_points,x,y


def generate_convexhull(ellipse_points):
    hull = ConvexHull(ellipse_points)
    hull_points = []
    for simplex in hull.simplices:
        hull_points.append([ellipse_points[simplex, 0][0], ellipse_points[simplex, 1][0]])
        hull_points.append([ellipse_points[simplex, 0][1], ellipse_points[simplex, 1][1]])
    y, x = zip(*hull_points)
    x = np.array(x)
    y = np.array(y)
    return hull, np.array(hull_points), x, y


def fit_ellipse(x, y):

    x_mean = x.mean()
    y_mean = y.mean()
    x = x-x_mean
    y = y-y_mean

    a = fitEllipse(x, y)
    center = ellipse_center(a)
    center[0] += x_mean
    center[1] += y_mean
    phi = ellipse_angle_of_rotation(a)
    axes = ellipse_axis_length(a)
    degree = math.degrees(phi)

    x += x_mean
    y += y_mean

    axes[0] = axes[0] * 2
    axes[1] = axes[1] * 2


    #print("xmean:", x_mean)
    #print("ymean:", y_mean)
    #print("center = ",  center)
    #print("angle of rotation = ",  degree)
    #print("axes = ", axes)
    return center, degree, axes
