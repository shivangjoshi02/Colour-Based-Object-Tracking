import imutils
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

class ColorCalibrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Calibration")

        self.create_sliders()
        self.create_buttons()

        self.cam = cv2.VideoCapture(0)
        self.update()

    def create_sliders(self):
        # Variables for slider values
        self.hue_lower_var = tk.IntVar(value=0)
        self.hue_upper_var = tk.IntVar(value=13)
        self.sat_lower_var = tk.IntVar(value=100)
        self.sat_upper_var = tk.IntVar(value=255)
        self.val_lower_var = tk.IntVar(value=50)
        self.val_upper_var = tk.IntVar(value=255)

        # Frame for sliders
        sliders_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        sliders_frame.grid(row=0, column=0)

        # Create a style to configure the slider colors
        slider_style = ttk.Style(self.root)
        slider_style.configure("Black.Horizontal.TScale", troughcolor="black", sliderbackground="white",
                               sliderhighlightcolor="white", sliderwidth=15)

        # Create sliders
        ttk.Label(sliders_frame, text="Hue Lower:").grid(row=0, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=179, variable=self.hue_lower_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=0, column=1)

        ttk.Label(sliders_frame, text="Hue Upper:").grid(row=1, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=179, variable=self.hue_upper_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=1, column=1)

        ttk.Label(sliders_frame, text="Saturation Lower:").grid(row=2, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=255, variable=self.sat_lower_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=2, column=1)

        ttk.Label(sliders_frame, text="Saturation Upper:").grid(row=3, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=255, variable=self.sat_upper_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=3, column=1)

        ttk.Label(sliders_frame, text="Value Lower:").grid(row=4, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=255, variable=self.val_lower_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=4, column=1)

        ttk.Label(sliders_frame, text="Value Upper:").grid(row=5, column=0, pady=5)
        ttk.Scale(sliders_frame, from_=0, to=255, variable=self.val_upper_var, orient=tk.HORIZONTAL, length=200,
                  style="Black.Horizontal.TScale").grid(row=5, column=1)

    def create_buttons(self):
        # Frame for buttons
        buttons_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        buttons_frame.grid(row=0, column=1)

        # Create a style to configure the button colors
        button_style = ttk.Style(self.root)
        button_style.configure('ColorButton.TButton', width=10)

        # Create buttons for color presets
        preset_names = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Magenta", "Black", "White"]
        preset_commands = [lambda name=name.lower(): self.set_preset_color(name) for name in preset_names]

        for i, name in enumerate(preset_names):
            button_color = name.lower()

            # Create a Canvas to draw the background color
            canvas = tk.Canvas(buttons_frame, width=16, height=16)
            canvas.create_rectangle(0, 0, 16, 16, fill=button_color)
            canvas.grid(row=i, column=0, pady=5, padx=5)

            # Create the button on top of the Canvas
            ttk.Button(buttons_frame, text=name, command=preset_commands[i], style='ColorButton.TButton',
                       compound=tk.CENTER).grid(row=i, column=1, pady=5)

    def set_preset_color(self, preset_name):
        # Preset color values
        presets = {
            "red": (0, 13, 100, 255, 50, 255),
            "green": (40, 80, 100, 255, 50, 255),
            "blue": (100, 120, 100, 255, 75, 255),
            "yellow": (25, 35, 100, 255, 100, 255),
            "purple": (120, 140, 100, 255, 50, 255),
            "orange": (15, 35, 100, 255, 100, 255),
            "cyan": (85, 100, 100, 125, 255, 255),
            "magenta": (140, 160, 100, 179, 255, 255),
            "black": (85, 100, 100, 125, 255, 255),
            "white": (140, 160, 100, 179, 255, 255),
            # Add more presets as needed
        }
        if preset_name in presets:
            h_low, h_up, s_low, s_up, v_low, v_up = presets[preset_name]
            self.hue_lower_var.set(h_low)
            self.hue_upper_var.set(h_up)
            self.sat_lower_var.set(s_low)
            self.sat_upper_var.set(s_up)
            self.val_lower_var.set(v_low)
            self.val_upper_var.set(v_up)

    def update(self):
        _, frame = self.cam.read()
        frame = imutils.resize(frame, width=600)
        blur = cv2.GaussianBlur(frame, (11, 11), 0)

        h_lower = self.hue_lower_var.get()
        h_upper = self.hue_upper_var.get()
        s_lower = self.sat_lower_var.get()
        s_upper = self.sat_upper_var.get()
        v_lower = self.val_lower_var.get()
        v_upper = self.val_upper_var.get()

        orgLower = (h_lower, s_lower, v_lower)
        orgUpper = (h_upper, s_upper, v_upper)

        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, orgLower, orgUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        color_calibration = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Color Calibration", color_calibration)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                if radius > 250:
                    print("stop")
                else:
                    if center[0] < 150:
                        print("Left")
                    elif center[0] > 450:
                        print("Right")
                    elif center[0] < 250:
                        print("Front")
                    else:
                        print("Stop")

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            self.cam.release()
            cv2.destroyAllWindows()
            self.root.destroy()
        else:
            self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorCalibrationApp(root)
    root.mainloop()
