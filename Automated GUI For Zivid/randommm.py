import tkinter as tk
from tkinter import messagebox
import multiprocessing

def background_task():
    global result

    """Background task to be run in a separate process."""
    # This is just a placeholder function for demonstration purposes.
    # Replace it with your actual background processing logic.
    result = "Result of background processing"
    return result

def start_background_process():
    """Start a background process."""
    # Create a multiprocessing.Process object
    process = multiprocessing.Process(target=background_task)
    print(process.start())
    # Optionally, you can wait for the process to finish:
    # process.join()

def on_button_click():
    """Handle button click event."""
    # Start the background process
    start_background_process()
    # Display a message box to indicate the process has started
    messagebox.showinfo("Info", f"{result}")

result = None
# Create the main application window
root = tk.Tk()
root.title("Multiprocessing with GUI")

# Create a button to start the background process
button = tk.Button(root, text="Start Background Process", command=on_button_click)
button.pack(pady=20)

# Run the GUI event loop
root.mainloop()
