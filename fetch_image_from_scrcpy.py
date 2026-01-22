# collect image periodically from scrcpy, return as cv2 image object
# run scrcpy window with title "camera-scrcpy"

# https://github.com/leng-yue/py-scrcpy-client/blob/main/scrcpy_ui/main.py#L78

import pygetwindow as gw
import cv2
import numpy as np
