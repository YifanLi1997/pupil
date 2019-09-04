import os

number = "0056"
print(int(number))


pupil_positions = [(1,1),(2,2),3,4]
ref_positions = [(1,1),(2,2),3,4]

cal_data = [(pupil_positions[i], ref_positions[i]) for i in range(len(ref_positions))]
#print(type(cal_data[1][1]))

#pupil_cornea_images = os.listdir("C:\\work\\pupil\\pupil_src\\tests\\yifan\\pupil_result\\gaze_mapping\\calibration\\pupil_cornea\\")
#print(os.path.splitext(pupil_cornea_images[0])[0])

#detectProperties2D = {}
#detectProperties2D["coarse_detection"] = True
#detectProperties2D["coarse_filter_min"] = 128
#detectProperties2D["coarse_filter_max"] = 280
#detectProperties2D["intensity_range"] = 23
#detectProperties2D["blur_size"] = 5
#detectProperties2D["canny_treshold"] = 160
#detectProperties2D["canny_ration"] = 2
#detectProperties2D["canny_aperture"] = 5
#detectProperties2D["pupil_size_max"] = 100
#detectProperties2D["pupil_size_min"] = 10
#detectProperties2D["strong_perimeter_ratio_range_min"] = 0.8
#detectProperties2D["strong_perimeter_ratio_range_max"] = 1.1
#detectProperties2D["strong_area_ratio_range_min"] = 0.6
#detectProperties2D["strong_area_ratio_range_max"] = 1.1
#detectProperties2D["contour_size_min"] = 5
#detectProperties2D["ellipse_roundness_ratio"] = 0.1
#detectProperties2D["initial_ellipse_fit_treshhold"] = 1.8
#detectProperties2D["final_perimeter_ratio_range_min"] = 0.6
#detectProperties2D["final_perimeter_ratio_range_max"] = 1.2
#detectProperties2D["ellipse_true_support_min_dist"] = 2.5
#detectProperties2D["support_pixel_ratio_exponent"] = 2.0

#detectProperties3D = {}
#detectProperties3D["model_sensitivity"] = 0.997

#settings = {}
#settings["2D_Settings"] = detectProperties2D
#settings["3D_Settings"] = detectProperties3D
#print(settings)