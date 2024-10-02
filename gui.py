import tkinter as tk
from camera import camera
# Create the main window
root = tk.Tk()
root.title("Responsive Layout")
root.geometry("600x400")  # Initial size of the window

# Configure the grid to allow resizing
root.grid_rowconfigure(0, weight=1)  # Top row (for left and right frames)
root.grid_rowconfigure(1, weight=0)  # Bottom row (for button frame)
root.grid_columnconfigure(0, weight=1)  # Left column
root.grid_columnconfigure(1, weight=1)  # Right column

# Create a frame for the left (blue) section
frame_left = tk.Frame(root, bg='skyblue')
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

camera(frame_left)

# Create a frame for the right (green) section
frame_right = tk.Frame(root, bg='green')
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create a frame for the bottom button
frame_bottom = tk.Frame(root)
frame_bottom.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Add a button to the bottom frame
button = tk.Button(frame_bottom, text="Get Info", bg='green', fg='black')
button.pack(expand=True)

# Allow resizing of the frames
frame_left.grid_propagate(False)
frame_right.grid_propagate(False)
frame_bottom.grid_propagate(False)

# Start the Tkinter event loop
root.mainloop()
