import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib

def visulize_thresholding(data, threshold, fig, fig_x, fig_y, fig_order, xlim0=0, xlim1=320, ylim0=0, ylim1=240):

    _, threshed_datapoints = cv2.threshold(data, threshold, 255, cv2.THRESH_BINARY)
    print("threshed_datapoints: ", threshed_datapoints)
    
    ax = fig.add_subplot(fig_x, fig_y, fig_order)
    title = "threshold = " + str(threshold)
    ax.set_title(title)
    plt.xlim(xlim0,xlim1)
    plt.ylim(ylim0,ylim1)
    plt.gca().invert_yaxis()
    plt.imshow(threshed_datapoints)


def visualize_orginal_images(eye, pupil, eye_gray, pupil_gray):

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,4,1)
    ax1.set_title("original eye")
    plt.imshow(eye)

    ax2 = fig1.add_subplot(1,4,2)
    ax2.set_title("original pupil")
    plt.imshow(pupil)

    ax3 = fig1.add_subplot(1,4,3)
    ax3.set_title("grayscale eye")
    plt.imshow(eye_gray)

    ax4 = fig1.add_subplot(1,4,4)
    ax4.set_title("grayscale pupil")
    plt.imshow(pupil_gray)

    fig1.tight_layout()


def visulize_ellipse(ellipse, xlim0=0, xlim1=320, ylim0=0, ylim1=240):

    y,x = zip(*ellipse)
    y = list(y)
    x = list(x)

    #for i in range(len(y)):
    #    tmp = 240 - y[i]
    #    y[i] = tmp

    fig0 = plt.figure()
    plt.scatter(x,y) 
    plt.xlim(xlim0,xlim1)
    plt.ylim(ylim0,ylim1)
    plt.gca().invert_yaxis()


def visualize_hull(ellipse_points,hull):
    plt.plot(ellipse_points[:,0], ellipse_points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(ellipse_points[simplex, 0], ellipse_points[simplex, 1], 'k-')


def visualize_fiited_ellipse(fitted_ellipse):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_artist(fitted_ellipse)
    fitted_ellipse.set_alpha(0.5)
    ax.scatter(fitted_ellipse.center[0],fitted_ellipse.center[1], color = 'red', s=100)
    plt.xlim([0,320])
    plt.ylim([0,240])


def visualize_fitted_ellipse_on_top_of_the_original_image(fitted_ellipse, pupil_gray, xlim0=0, xlim1=320, ylim0=0, ylim1=240):
    fig1 = plt.figure()
    ax = fig1.add_subplot(1,1,1)
    plt.imshow(pupil_gray, cmap = "gray")
    ax.add_artist(fitted_ellipse)
    fitted_ellipse.set_alpha(0.2)
    fitted_ellipse.set_color("yellow")
    ax.scatter(fitted_ellipse.center[0],fitted_ellipse.center[1], color = 'red', s=20)
    plt.xlim(xlim0,xlim1)
    plt.ylim(ylim1,ylim0)
