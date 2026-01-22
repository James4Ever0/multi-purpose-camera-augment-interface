# collect image periodically from scrcpy, return as cv2 image object
# run scrcpy window with title "camera-scrcpy"

# https://github.com/leng-yue/py-scrcpy-client/blob/main/scrcpy_ui/main.py#L78

# [1] pip install git+https://github.com/leng-yue/py-scrcpy-client.git@ad57b15934c71cb24555bbb3f5050b1d6c908de5
# commit hash: ad57b15934c71cb24555bbb3f5050b1d6c908de5

import cv2
import scrcpy  # [1]

from adbutils import adb

def on_init():
    print("Scrcpy client initialized")

def select_first_device_and_apply_frame_callback(on_frame):
    """blocking, run it in thread or as main thread"""

    device_list = adb.device_list()
    print("Avaliable devices:", device_list)
    if len(device_list) == 0:
        raise RuntimeError("No device connected")

    # use first device
    device = device_list[0]
    client = scrcpy.Client(
        device=device,
        bitrate=1000000000,
        encoder_name=None,
        max_fps=60,
    )


    client.add_listener(scrcpy.EVENT_INIT, on_init)
    client.add_listener(scrcpy.EVENT_FRAME, on_frame)

    client.start()

import numpy as np
def test_on_frame(frame):
    if type(frame) == np.ndarray:
        print("New frame received")
        # print('Frame:', frame) # numpy array
        print("Frame type:", type(frame)) # <class 'numpy.ndarray'>
        print("Frame shape:", frame.shape) # (height, width, 3), (2560, 1144, 3)

def test():
    select_first_device_and_apply_frame_callback(test_on_frame)

if __name__ == "__main__":
    test()