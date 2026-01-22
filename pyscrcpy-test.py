# Install: pip install pyscrcpy
# need py3.7 instead?
# better install from github, the latest version is not on pypi
# https://github.com/yixinNB/pyscrcpy

import pyscrcpy
import cv2
import numpy as np
import threading

class ScrcpyCapture:
    def __init__(self, device_id=None, max_width=1280):
        self.client = pyscrcpy.Client(device=device_id, max_width=max_width)
        self.frame = None
        self.lock = threading.Lock()
        
        # Set frame callback
        self.client.add_listener(pyscrcpy.EVENT_FRAME, self._on_frame)
        
    def _on_frame(self, frame):
        """Callback when new frame is available"""
        with self.lock:
            # Convert to numpy array
            self.frame = np.array(frame)
    
    def start(self):
        """Start scrcpy client"""
        self.client.start()
    
    def get_frame(self):
        """Get latest frame"""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def stop(self):
        """Stop client"""
        self.client.stop()

# Usage
capture = ScrcpyCapture()
capture.start()

# Get frames periodically
while True:
    frame = capture.get_frame()
    if frame is not None:
        cv2.imshow("Scrcpy", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture.stop()
cv2.destroyAllWindows()

# try myscrcpy?
# https://github.com/me2sy/MYScrcpy/blob/main/src/myscrcpy/core/connection.py