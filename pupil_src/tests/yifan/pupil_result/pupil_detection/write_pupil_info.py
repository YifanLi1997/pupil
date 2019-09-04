import sys
import os
import glob
from matplotlib import pyplot as plt
import matplotlib

from pupil_detection import pupil_detection_result_2d

datasets = "exp5" # control, exp1, exp2, exp3, exp4, exp5
calibration = False

if calibration:
    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+datasets+"\\calibration\\eye\\"
else: 
    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+datasets+"\\eye\\"
eye_images = [f for f in glob.glob(dictpath + "*.png")]

f = open(dictpath+"pupil_info.txt","w")

for i in eye_images:
    center, degree, axes = pupil_detection_result_2d(i, False)
    image_name = i.split("\\")[-1]
    frame_number = image_name.split(".")[0]
    info = str(frame_number) + "," + str(center) + "," + str(degree) + "," + str(axes) + "\n"
    f.write(info)

f.close()
plt.show()