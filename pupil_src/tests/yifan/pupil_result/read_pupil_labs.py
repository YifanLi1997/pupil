import numpy as np
from matplotlib import pyplot as plt
import matplotlib

fig = plt.figure()

frame_img = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\frame_img.npy")
ax1 = fig.add_subplot(1,3,1)
plt.imshow(frame_img)
ax1.set_title("frame_img")
print(frame_img.shape)

frame_bgr = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\frame_bgr.npy")
ax2 = fig.add_subplot(1,3,2)
plt.imshow(frame_bgr)
ax2.set_title("frame_bgr")

frame_gray = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\frame_gray.npy")
ax3 = fig.add_subplot(1,3,3)
plt.imshow(frame_gray)
ax3.set_title("frame_gray")

#result = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\result.npy", allow_pickle=True)#3D
result = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\result.npy", allow_pickle=True)#2D
print("result: ",result)

fig.tight_layout()
#plt.show()

#frame = np.load("C:\\work\\pupil\\pupil_src\\tests\\yifan\\frame.npy", allow_pickle=True)
#print("==============================")
#print("frame: ", frame)