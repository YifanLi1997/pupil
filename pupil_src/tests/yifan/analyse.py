import sys
import os
import glob
from matplotlib import pyplot as plt
import matplotlib
import math
import numpy as np

datasets = {"control group":"control","exp1":"exp1","exp2":"exp2","exp3":"exp3","exp4":"exp4","exp5":"exp5"}

def difference_between_lists(list1, list2):
    differences = []
    for i in range(len(list1)):
        difference = math.hypot(list1[i][0] - list2[i][0], list1[i][1] - list2[i][1])
        differences.append(difference)
    return differences


def difference_between_lists_with_labels(list1, list2, list3):
    differences = []
    for i in range(len(list1)):
        if list3[i]:
            difference = math.hypot(list1[i][0] - list2[i][0], list1[i][1] - list2[i][1])
            differences.append(difference)
        else:
            differences.append(0)
    return differences


def cal_attributes(group_name):
    
    dictpath = "C:\\Users\\localadmin\\Downloads\\my_attempt\\images\\"+group_name

    Gs = []
    gt_gaze_file = open(dictpath+"\\gaze_in_scene_camera.txt","r")
    gt_gazes = gt_gaze_file.readlines()
    for i in gt_gazes:
        x = float(i.split(" ")[1])
        y = float(i.split(" ")[2])
        Gs.append([x,y])
    gt_gaze_file.close()
    #print("gt gaze finished")

    GPs = []
    GGs = []
    PPs = []
    PGs = []

    gaze_file = open(dictpath+"\\gaze_info.txt","r")
    gazes = gaze_file.readlines()
    for i in gazes:
        PG_x = float(i.split(",")[1][1:])
        PG_y = float(i.split(",")[2].strip()[:-1])
        PP_x = float(i.split(",")[3][1:])
        PP_y = float(i.split(",")[4].strip()[:-1])
        GG_x = float(i.split(",")[5][1:])
        GG_y = float(i.split(",")[6].strip()[:-1])
        GP_x = float(i.split(",")[7][1:])
        GP_y = float(i.split(",")[8].strip()[:-1])
        PGs.append([PG_x, PG_y])
        PPs.append([PP_x, PP_y])
        GGs.append([GG_x, GG_y])
        GPs.append([GP_x, GP_y])
    gaze_file.close()
    #print("gaze finished")

    assert len(Gs) == len(GPs), "the number of gt gazes != the number of calculated gazes"

    GPCs = []
    gt_pupil_file = open(dictpath+"\\pupil_cornea\\pupil_info.txt","r")
    gt_pupils = gt_pupil_file.readlines()
    for i in gt_pupils:
        center = i.split(",")[1]
        try:
            #x = float(center.split(" ")[0][1:])
            #y = float(center.split(" ")[1].strip()[:-1].strip())
            #tmp = 2
            #while y == "":
            #    y = float(center.split(" ")[tmp].strip()[:-1].strip())
            #    tmp += 1
            x = float(center[1:13].strip())
            y = float(center[13:-1].strip())
        except ValueError:
            print("the error line is ", i.split(",")[0])
        GPCs.append([x,y])
    gt_pupil_file.close()
    #print("gt pupil finished")

    PPCs = []
    pupil_file = open(dictpath+"\\eye\\pupil_info.txt","r")
    pupils = pupil_file.readlines()
    for i in pupils:
        x = float(i.split(",")[1][1:])
        y = float(i.split(",")[2].strip()[:-1])
        PPCs.append([x,y])
    pupil_file.close()
    #print("pupil finished")

    assert len(GPCs) == len(PPCs), "the number of gt pupils != the number of calculated pupils"

    GP_Gs = difference_between_lists(GPs, Gs)
    GG_Gs = difference_between_lists(GGs, Gs)
    GP_GGs = difference_between_lists(GPs, GGs)
    GPC_PPCs = difference_between_lists(GPCs, PPCs)

    detected_or_not = []
    for i in range(len(GPC_PPCs)):
        if GPC_PPCs[i] < 3:
            detected_or_not.append(1)
        else:
            detected_or_not.append(0)

    detection_rate = detected_or_not.count(1) / len(GPC_PPCs)
    #print("detection rate: ", detection_rate)

    PP_Gs = difference_between_lists_with_labels(PPs, Gs, detected_or_not)
    PP_GPs = difference_between_lists_with_labels(PPs, GPs, detected_or_not)
    PG_GGs = difference_between_lists_with_labels(PGs, GGs, detected_or_not)

    detect_GPC_PPCs = []
    for i in range(len(GPC_PPCs)):
        if detected_or_not[i]:
            detect_GPC_PPCs.append(GPC_PPCs[i])
            #print(GPC_PPCs[i])
        else:
            detect_GPC_PPCs.append(0)
            #print(i*4)
    

    display_helper = []
    for i in detect_GPC_PPCs:
        if i == 0:
            display_helper.append('r')
        else:
            display_helper.append('b')


    attributes = [GP_Gs, GG_Gs, GP_GGs, PP_Gs, PP_GPs, PG_GGs, detect_GPC_PPCs, detection_rate, display_helper]


    return attributes


def visualize_one_dataset(attributes, display_helper):
    x = np.linspace(0, 396, 100)
    x_sim = np.linspace(0, 396, 50)
    fig = plt.figure()
    title = "detection rate: " + str(attributes[-2])
    fig.suptitle(title)
    for i in range(7):
        ax = fig.add_subplot(2,4,i+1)
        if attributes == exp5:
            plt.scatter(x_sim,attributes[i],c = display_helper)
        else:
            plt.scatter(x,attributes[i],c = display_helper)
        ax.set_ylim(ymin = 0)
    return None


def visulize_datasets_comparison(order_of_the_attribute):
    x = np.linspace(0, 396, 100)
    x_sim = np.linspace(0, 396, 50)
    fig = plt.figure()
    if order_of_the_attribute == 0:
        title = "error in gaze mapping and calibration (GP-G)"
    elif order_of_the_attribute == 1:
        title = "error in gaze mapping (GG-G)"
    elif order_of_the_attribute == 2:
        title = "error in calibration (GG-GP)"
    elif order_of_the_attribute == 3:
        title = "error in the entire process (PP-G)"
    elif order_of_the_attribute == 4:
        title = "error in pupil detection that is amplified by calibration (PP-GP)"
    elif order_of_the_attribute == 5:
        title = "error in pupil detection that is amplified by gaze mapping (PG-GG)"
    elif order_of_the_attribute == 6:
        title = "error in pupil detection (GPC-PPC)"
    fig.suptitle(title)

    ax1 = fig.add_subplot(2,3,1)
    plt.scatter(x, control[order_of_the_attribute], c = control[-1])
    ax1.set_ylim(ymin = 0)
    ax1.set_title('Control group')

    ax2 = fig.add_subplot(2,3,2)
    plt.scatter(x, exp1[order_of_the_attribute], c = exp1[-1])
    ax2.set_ylim(ymin = 0)
    ax2.set_title('Exp. 1')

    ax3 = fig.add_subplot(2,3,3)
    plt.scatter(x, exp2[order_of_the_attribute], c = exp2[-1])
    ax3.set_ylim(ymin = 0)
    ax3.set_title('Exp. 2')

    ax4 = fig.add_subplot(2,3,4)
    plt.scatter(x, exp3[order_of_the_attribute], c = exp3[-1])
    ax4.set_ylim(ymin = 0)
    ax4.set_title('Exp. 3')

    ax5 = fig.add_subplot(2,3,5)
    plt.scatter(x, exp4[order_of_the_attribute], c = exp4[-1])
    ax5.set_ylim(ymin = 0)
    ax5.set_title('Exp. 4')

    ax6 = fig.add_subplot(2,3,6)
    plt.scatter(x_sim, exp5[order_of_the_attribute], c = exp5[-1])
    ax6.set_ylim(ymin = 0)
    ax6.set_title('Exp. 5')

    return None

control = cal_attributes(datasets["control group"])
exp1 = cal_attributes(datasets["exp1"])
exp2 = cal_attributes(datasets["exp2"])
exp3 = cal_attributes(datasets["exp3"])
exp4 = cal_attributes(datasets["exp4"])
exp5 = cal_attributes(datasets["exp5"])


visualize_one_dataset(control, control[-1])
#visualize_one_dataset(exp1, exp1[-1])
#visualize_one_dataset(exp2, exp2[-1])
#visualize_one_dataset(exp3, exp3[-1])
#visualize_one_dataset(exp4, exp4[-1])
#visualize_one_dataset(exp5, exp5[-1])

#for i in range(7):
#    visulize_datasets_comparison(i)
plt.show()