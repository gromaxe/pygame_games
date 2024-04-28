import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Canvas
from pynput import mouse
import pyautogui
import keyboard
import threading

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.click_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.clicking = False
        self.click_type = 'left'  # Default click type

    def setup_ui(self):
        self.root.title("Python AutoClicker")

        self.set_point_button = tk.Button(self.root, text="Set Click Point and Rate", command=self.prepare_to_set_point)
        self.set_point_button.pack(pady=20)

        self.click_type_var = tk.StringVar(self.root, 'left')
        tk.Radiobutton(self.root, text="Left Click", variable=self.click_type_var, value='left').pack()
        tk.Radiobutton(self.root, text="Right Click", variable=self.click_type_var, value='right').pack()

        self.info_label = tk.Label(self.root, text="Click anywhere to set the point after minimizing.")
        self.info_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Clicking", state=tk.DISABLED, command=self.start_clicking)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="Stop Clicking", state=tk.DISABLED, command=self.stop_clicking)
        self.stop_button.pack(pady=20)

    def prepare_to_set_point(self):
        self.root.iconify()  # Minimize the window
        self.click_listener.start()  # Start listening for mouse clicks

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.click_listener.stop()  # Stop listening to further clicks
            self.click_x, self.click_y = x, y
            self.root.after(0, self.show_click_location)

    def show_click_location(self):
        overlay = Toplevel(self.root)
        overlay.attributes("-alpha", 0.5)  # Semi-transparent
        overlay.attributes("-topmost", True)  # Always on top
        overlay.overrideredirect(True)  # No window decorations
        overlay.geometry(f"50x50+{self.click_x-25}+{self.click_y-25}")  # Centered on click
        canvas = Canvas(overlay, width=50, height=50, bg='red', highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 40, 40, fill='white')
        overlay.after(1000, overlay.destroy)  # Destroy overlay after 1 second
        self.root.after(1000, self.prompt_for_click_rate)

    def prompt_for_click_rate(self):
        self.root.deiconify()  # Show the window again
        rate = simpledialog.askinteger("Input", "Enter Click Rate (clicks per second)", parent=self.root)
        if rate:
            self.click_rate = rate
            self.click_type = self.click_type_var.get()  # Get the selected click type
            self.info_label.config(text=f"Click point set at ({self.click_x}, {self.click_y}) with rate {self.click_rate} cps, type: {self.click_type}.")
            self.start_button.config(state=tk.NORMAL)

    def start_clicking(self):
        self.clicking = True
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.auto_click).start()
        keyboard.add_hotkey('esc', lambda: self.stop_clicking())

    def auto_click(self):
        while self.clicking:
            pyautogui.click(self.click_x, self.click_y, interval=1/self.click_rate, button=self.click_type)

    def stop_clicking(self):
        self.clicking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
