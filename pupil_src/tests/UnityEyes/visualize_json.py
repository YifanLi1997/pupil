import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib
import json

eye = cv2.imread("1.jpg")

with open("1.json", "r") as f:
    json_file = json.load(f)

interior_margin_2d = json_file["interior_margin_2d"]
caruncle_2d = json_file["caruncle_2d"]
iris_2d = json_file["iris_2d"]
eye_details = json_file["eye_details"]
lighting_details = json_file["lighting_details"]
eye_region_details = json_file["eye_region_details"]
head_pose = json_file["head_pose"]

def visualize(points):
    vis = []
    for i in range(len(points)):
        vis.append([float(points[i][1:9]),480.0000-float(points[i][10:19])])

    x,y = zip(*vis)
    plt.imshow(eye)
    plt.scatter(x,y)

visualize(interior_margin_2d)
visualize(caruncle_2d)
visualize(iris_2d)

plt.xlim(150,500)
plt.ylim(100,450)
plt.gca().invert_yaxis()
plt.show()