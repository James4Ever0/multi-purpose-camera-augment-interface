# development python version: 3.11.11

import tkinter as tk
import cv2
import json
import os

#  features:
# crop, slider
# rotate, slider
# zoom, slider
# mirror, toggle button
# store values to file when changed, load when opened

setting_file = "settings.json"
imageWindowGeometry = "800x800"
# create interface
root = tk.Tk()
root.title("Image Editor")

# create sliders
crop_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Crop")
rotate_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="Rotate")
zoom_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Zoom")
mirror_button = tk.Button(root, text="Mirror", width=10)

# add callback for mirror button
def mirror_callback():
    print("Mirror button clicked")
    # change label
    mirror_button.config(text="Unmirror" if mirror_button["text"] == "Mirror" else "Mirror")
mirror_button.config(command=mirror_callback)

crop_slider.pack()
rotate_slider.pack()
zoom_slider.pack()
mirror_button.pack()

# root.mainloop()

# create save and load buttons
save_button = tk.Button(root, text="Save", width=10)
# load_button = tk.Button(root, text="Load")

save_button.pack()
# load_button.pack()

# create function to save settings
def save_settings():
    settings = {
        "crop": crop_slider.get(),
        "rotate": rotate_slider.get(),
        "zoom": zoom_slider.get(),
        "mirror": mirror_button["text"] == "Mirror"
    }
    with open(setting_file, "w") as f:
        json.dump(settings, f)

# add callback for save button
save_button.config(command=save_settings)

# create function to load settings
def load_settings():
    with open(setting_file, "r") as f:
        settings = json.load(f)
        crop_slider.set(settings["crop"])
        rotate_slider.set(settings["rotate"])
        zoom_slider.set(settings["zoom"])
        if settings["mirror"]:
            mirror_button["text"] = "Unmirror"
        else:
            mirror_button["text"] = "Mirror"

if os.path.exists(setting_file):
    load_settings()


Window = tk.Toplevel()
Window.title("Image")
Window.geometry(imageWindowGeometry)

# add onclose function 
def on_close():
    save_settings()
    Window.destroy()
    root.destroy()
Window.protocol("WM_DELETE_WINDOW", on_close)

# create image label
image_label = tk.Label(Window)
image_label.pack()


from PIL import Image, ImageTk

# create function to update image
def update_image(input_file:str):
    # get values from sliders
    crop_value = crop_slider.get() # 0 - 100
    rotate_value = rotate_slider.get() # 0 - 360
    zoom_value = zoom_slider.get() # 0 - 100
    mirror_value = mirror_button["text"] == "Unmirror"

    print("crop_value: ", crop_value)
    print("rotate_value: ", rotate_value)
    print("zoom_value: ", zoom_value)
    print("mirror_value: ", mirror_value)
    # load image
    image = cv2.imread(input_file)

    b,g,r = cv2.split(image)
    image = cv2.merge((r,g,b))
    width, height= image.shape[:2]

    # crop image
    if width > height:
        # crop width
        margin = width-height
        shift = margin * crop_value / 100

        image = image[int(shift):int(height+shift), :, :]
    elif height > width:
        margin = height-width
        shift = margin * crop_value / 100
        image = image[:, int(shift):int(width+shift), :]
    else:
        # do nothing
        ...

    # rotate image
    M = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), rotate_value, 1.0)
    image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # zoom image
    current_image_height, current_image_width = image.shape[:2]
    # do crop then resize
    if zoom_value == 0:
        ...
    else:
        if zoom_value == 100:
            zoom_value = 99
        zoom_value = zoom_value / 100
        zoom_value = zoom_value
        half_width = current_image_width / 2
        shift = int(half_width * zoom_value)
        image = image[shift:current_image_height-shift, shift:current_image_width-shift, :]
        image = cv2.resize(image, (current_image_height, current_image_width), interpolation = cv2.INTER_AREA)

    # mirror image
    if mirror_value:
        image = cv2.flip(image, 1)
    
    # resize image to window size
    window_width, window_height = Window.winfo_width(), Window.winfo_height()
    min_wh = min(window_width, window_height)
    image = cv2.resize(image, (min_wh, min_wh))

    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=im)



    # display image
    image_label["image"] = imgtk
    image_label.image = imgtk
    image_label.pack()

# update image periodically, every 100ms
import time
import threading

def update_image_thread():
    input_file = "Samsung-Galaxy-device-settings-2.png"
    while True:
        try:
            update_image(input_file)
        except:
            import traceback
            traceback.print_exc()
            print("Error updating image")
        time.sleep(0.1)

threading.Thread(target=update_image_thread, daemon=True).start()

# main loop
root.mainloop()