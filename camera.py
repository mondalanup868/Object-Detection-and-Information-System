import tkinter as tk
import cv2
from PIL import Image, ImageTk
import datetime

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def camera(frame):
    # Replace this with the correct IP camera URL provided by your app
    stream_url = "http://10.9.165.118:8080/video"

    # Start capturing the video feed from the mobile camera using the IP camera URL
    cap = cv2.VideoCapture(stream_url)

    # Create a label to display the camera feed inside the frame
    label_video = tk.Label(frame)
    label_video.pack(expand=True, fill="both")  # Adjust to fill the frame

    # Variable to store the current frame and control whether the video feed should update
    current_frame = None
    video_running = True

    def update_frame():
        nonlocal current_frame, video_running
        if video_running:
            # Capture frame-by-frame
            ret, frame_cv = cap.read()
            if ret:
                current_frame = frame_cv  # Store the current frame for capturing
                
                # Get the current size of the frame (to fit the camera feed within the blue frame)
                frame_width = frame.winfo_width()
                frame_height = frame.winfo_height() - 50  # Reserve space for the Capture button

                # Ensure frame dimensions are positive
                if frame_width > 0 and frame_height > 0:
                    # Resize the frame to fit the current dimensions of the blue frame
                    frame_cv = cv2.resize(frame_cv, (frame_width, frame_height))

                    # Convert the image from OpenCV (BGR) to PIL format (RGB)
                    frame_cv = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_cv)
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Update the label with the new frame
                    label_video.imgtk = imgtk
                    label_video.configure(image=imgtk)

            else:
                print("Failed to capture frame from the camera.")

        # Call the update_frame function every 10ms
        frame.after(10, update_frame)

    # Function to capture the current frame, stop the video feed, and detect faces
    def capture_image():
        nonlocal video_running, current_frame
        if current_frame is not None:
            # Stop the video feed (freeze the frame)
            video_running = False

            # Save the current frame as an image (timestamped filename)
            filename = f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            # Detect faces in the current frame
            detect_and_draw_faces(current_frame)

            # Save the image with face detection
            cv2.imwrite(filename, current_frame)
            print(f"Image captured, faces detected, and saved as {filename}")

    # Function to detect faces and draw green boxes around them
    def detect_and_draw_faces(frame_cv):
        # Convert the frame to grayscale (required for Haar cascades)
        gray_frame = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2GRAY)

        # Detect faces using the cascade classifier
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw a green rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_cv, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green box with 2-pixel width

        # Resize the image to fit within the dynamically sized frame
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height() - 50  # Reserve space for the Capture button
        
        # Ensure dimensions are valid for resizing
        if frame_width > 0 and frame_height > 0:
            frame_cv_resized = cv2.resize(frame_cv, (frame_width, frame_height))

            # Convert the image from OpenCV (BGR) to PIL format (RGB) for displaying
            frame_cv_rgb = cv2.cvtColor(frame_cv_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_cv_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)

    # Add the shutter button for capturing the image at the bottom of the blue frame
    shutter_button = tk.Button(frame, text="Capture & Detect", command=capture_image, bg="red", fg="white")
    shutter_button.pack(pady=10, side=tk.BOTTOM)

    # Start the video update loop
    update_frame()

# Sample code to integrate the camera function with Tkinter
root = tk.Tk()
root.title("Camera Feed with Face Detection")
root.geometry("600x500")

# Create a grid layout where the blue and green frames can resize
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create a left frame (blue) for the camera
frame_left = tk.Frame(root, bg='skyblue', width=300, height=300)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a right frame (green) for additional content (optional)
frame_right = tk.Frame(root, bg='green', width=300, height=300)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create a bottom frame for the "Get Info" button
frame_bottom = tk.Frame(root, bg="lightgray", height=50)
frame_bottom.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Add a button to the bottom frame
button_info = tk.Button(frame_bottom, text="Get Info", bg='green', fg='white')
button_info.pack(expand=True)

# Start the camera in the blue frame
camera(frame_left)

root.mainloop()
