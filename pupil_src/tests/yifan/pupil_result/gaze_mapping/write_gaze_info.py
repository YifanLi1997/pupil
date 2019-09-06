import sys
import os
import glob
from matplotlib import pyplot as plt
import matplotlib

from gaze_mapping import read_monocular_calibration_data, gaze_mapping_result_2d, gaze_mapping_with_gt_pupil_2d

#datasets = {"control","exp1","exp2","exp3","exp4"} # control, exp1, exp2, exp3, exp4, exp5
datasets = {"exp5"}

for dataset in datasets:

    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+dataset+"\\"
    calibration_path = dictpath + "calibration\\"
    eye_images_path = dictpath + "eye\\"
    pupil_cornea_images_path = dictpath + "pupil_cornea\\"

    eye_images = [f for f in glob.glob(eye_images_path + "*.png")]
    pupil_cornea_images = [f for f in glob.glob(pupil_cornea_images_path + "*.png")]

    f = open(dictpath+"gaze_info.txt","w")

    for i in range(len(eye_images)):
        image_name = eye_images[i].split("\\")[-1]
        frame_number = image_name.split(".")[0]

        #eye_dummy_cal = gaze_mapping_result_2d(eye_images[i])
        PG = gaze_mapping_result_2d(eye_images[i], "monocular", calibration_path)
        PP = gaze_mapping_result_2d(eye_images[i], "monocular", calibration_path, False)

        #pupil_dummy_cal = gaze_mapping_with_gt_pupil_2d(pupil_cornea_images[i])
        GG = gaze_mapping_with_gt_pupil_2d(pupil_cornea_images[i], "monocular", calibration_path)
        GP = gaze_mapping_with_gt_pupil_2d(pupil_cornea_images[i], "monocular", calibration_path, False)

        #info = str(frame_number) + "," + str(eye_dummy_cal) + "," + str(eye_gt_monocular_cal) + "," + str(eye_monocular_cal) + "," + str(pupil_dummy_cal) + "," + str(pupil_gt_monocular_cal) + "," + str(pupil_monocular_cal) + "\n"
        info = str(frame_number) + "," + str(PG) + "," + str(PP) + "," + str(GG) + "," + str(GP) + "\n"
        #info = str(frame_number) + "," + str(PP*) + "," + str(PP) + "," + str(P*P*) + "," + str(P*P) + "\n"
        f.write(info)

    f.close()

plt.show()