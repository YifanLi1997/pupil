import sys
import os
import glob
from matplotlib import pyplot as plt
import matplotlib

from gt_pupil_detection import gt_pupil_info


datasets = "exp5" # control, exp1, exp2, exp3, exp4, exp5
calibration = False

if calibration:
    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+datasets+"\\calibration\\pupil_cornea\\"
else: 
    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+datasets+"\\pupil_cornea\\"
pupil_cornea_images = [f for f in glob.glob(dictpath + "*.png")]

f = open(dictpath+"pupil_info.txt","w")

for i in pupil_cornea_images:
    center, degree, axes = gt_pupil_info(i, False)
    image_name = i.split("\\")[-1]
    frame_number = image_name.split(".")[0]
    info = str(frame_number) + "," + str(center) + "," + str(degree) + "," + str(axes) + "\n"
    f.write(info)

f.close()
plt.show()