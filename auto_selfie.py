


import cv2
import numpy as np
import time
import tkinter as tk
from PIL import Image, ImageTk

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

class AutoSelfieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Selfie Camera")

        self.cap = None
        self.running = False
        self.start_time = None
        self.count = 0

        # Video display label
        self.label = tk.Label(root)
        self.label.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=10, pady=10)

        self.stop_btn = tk.Button(btn_frame, text="Pause Camera", command=self.stop_camera)
        self.stop_btn.grid(row=0, column=1, padx=10, pady=10)

        self.exit_btn = tk.Button(btn_frame, text="Exit", command=self.exit_app)
        self.exit_btn.grid(row=0, column=2, padx=10, pady=10)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.update_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def exit_app(self):
        self.stop_camera()
        self.root.destroy()

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()

            if ret:
                # Display image (with rectangle)
                img = frame.copy()

                # Clean image (no rectangle)
                clean_img = frame.copy()

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    # Draw rectangle ONLY on display
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    if self.start_time is None:
                        self.start_time = time.time()

                    elapsed = time.time() - self.start_time

                    if elapsed >= 5:
                        self.count += 1
                        filename = f"selfie_{self.count}.jpg"

                        # Save clean image (no rectangle)
                        cv2.imwrite(filename, clean_img)

                        print("Saved:", filename)

                        time.sleep(1)
                        self.start_time = None

                # Convert image to Tkinter format
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                imgtk = ImageTk.PhotoImage(image=img_pil)

                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)

            self.root.after(10, self.update_frame)

# Run app
root = tk.Tk()
app = AutoSelfieApp(root)
root.mainloop()
