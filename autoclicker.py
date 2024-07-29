import tkinter as tk
import pyautogui
import threading
import time
from pynput import mouse

class MouseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Coordinates Tracker")
        self.label = tk.Label(root, text="Move your mouse to see the coordinates", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.positions = []
        self.recording_enabled = True
        
        self.run_button = tk.Button(root, text="Run", command=self.run_clicks)
        self.run_button.pack(pady=10)
        
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_positions)
        self.clear_button.pack(pady=10)
        
        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(pady=10)

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.wait_label = tk.Label(root, text="Wait time after clicks (seconds):")
        self.wait_label.pack(pady=10)
        self.wait_entry = tk.Entry(root)
        self.wait_entry.pack(pady=10)
        self.wait_entry.insert(0, "5")  # Default wait time is 5 seconds

        self.loop_label = tk.Label(root, text="Number of loops:")
        self.loop_label.pack(pady=10)
        self.loop_entry = tk.Entry(root)
        self.loop_entry.pack(pady=10)
        self.loop_entry.insert(0, "1")  # Default number of loops is 1

        # Update coordinates every 100 milliseconds
        self.update_coordinates()

        # Start listening to mouse clicks globally
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def update_coordinates(self):
        # Get the mouse coordinates
        x, y = pyautogui.position()
        # Update the label with the coordinates
        self.label.config(text=f"Mouse Coordinates: ({x}, {y})")
        # Call this method again after 100 milliseconds
        self.root.after(100, self.update_coordinates)

    def is_click_inside_window(self, x, y):
        # Get the window's position and size
        window_x = self.root.winfo_rootx()
        window_y = self.root.winfo_rooty()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Check if the click is inside the window
        if window_x <= x <= window_x + window_width and window_y <= y <= window_y + window_height:
            return True
        return False

    def on_click(self, x, y, button, pressed):
        if pressed and self.recording_enabled:
            if not self.is_click_inside_window(x, y):
                # Add the coordinates to the list of positions
                self.positions.append((x, y))
                self.listbox.insert(tk.END, f"({x}, {y})")
                self.label.config(text=f"Recorded Positions: {self.positions}")

    def run_clicks(self):
        # Disable the Run button to prevent multiple clicks
        self.run_button.config(state=tk.DISABLED)
        self.recording_enabled = False  # Disable recording during auto-clicking

        # Get the wait time and number of loops from the entry fields
        try:
            wait_time = float(self.wait_entry.get())
        except ValueError:
            wait_time = 5  # Default wait time if input is invalid

        try:
            num_loops = int(self.loop_entry.get())
        except ValueError:
            num_loops = 1  # Default number of loops if input is invalid

        # Function to perform clicks and loop
        def perform_clicks():
            for _ in range(num_loops):
                time.sleep(3)  # Wait for 3 seconds before starting
                for pos in self.positions:
                    pyautogui.moveTo(pos[0], pos[1], duration=1)  # Move to the position slowly
                    pyautogui.click()
                time.sleep(wait_time)  # Wait for the specified time after all clicks
            self.run_button.config(state=tk.NORMAL)  # Re-enable the Run button after clicking
            self.recording_enabled = True  # Re-enable recording after auto-clicking

        # Run the click operation in a separate thread to avoid freezing the GUI
        threading.Thread(target=perform_clicks).start()

    def clear_positions(self):
        # Clear the recorded positions
        self.positions = []
        self.listbox.delete(0, tk.END)
        self.label.config(text="Move your mouse to see the coordinates")

    def delete_selected(self):
        # Get the selected index
        selected_index = self.listbox.curselection()
        if selected_index:
            # Remove the selected position from the list
            self.positions.pop(selected_index[0])
            # Remove the selected item from the listbox
            self.listbox.delete(selected_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseTracker(root)
    root.mainloop()