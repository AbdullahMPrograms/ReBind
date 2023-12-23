import tkinter as tk

# Function to decrease the size of the button when the mouse hovers over it
def on_enter(e):
    e.widget.config(height=2, width=14)

# Function to return the button to its original size when the mouse leaves it
def on_leave(e):
    e.widget.config(height=5, width=20)

# Create a new tkinter window
root = tk.Tk()
root.title("ReBind")

# Define the keys with their positions and sizes
keys = [
    # Format: (text, x, y, width, height, layouts)
    # The 'layouts' field is a set of strings that indicate which layouts the key belongs to.
    ("Esc", 10, 10, 50, 50, {"full", "tenkeyless"}),
    ("F1", 130, 10, 50, 50, {"full", "tenkeyless"}),
    ("F2", 190, 10, 50, 50, {"full", "tenkeyless"}),
    ("F3", 250, 10, 50, 50, {"full", "tenkeyless"}),
    ("F4", 310, 10, 50, 50, {"full", "tenkeyless"}),
    ("F5", 400, 10, 50, 50, {"full", "tenkeyless"}),
    ("F6", 460, 10, 50, 50, {"full", "tenkeyless"}),
    ("F7", 520, 10, 50, 50, {"full", "tenkeyless"}),
    ("F8", 580, 10, 50, 50, {"full", "tenkeyless"}),
    ("F9", 670, 10, 50, 50, {"full", "tenkeyless"}),
    ("F10", 730, 10, 50, 50, {"full", "tenkeyless"}),
    ("F11", 790, 10, 50, 50, {"full", "tenkeyless"}),
    ("F12", 850, 10, 50, 50, {"full", "tenkeyless"}),
    ("Print", 910, 10, 50, 50, {"full", "tenkeyless"}),
    ("Scroll Lock", 970, 10, 50, 50, {"full", "tenkeyless"}),
    ("Pause", 1030, 10, 50, 50, {"full", "tenkeyless"}),
    ("`", 10, 70, 50, 50, {"full", "tenkeyless"}),
    ("Esc", 10, 70, 50, 50, {"sixty"}),
    ("1", 70, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("2", 130, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("3", 190, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("4", 250, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("5", 310, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("6", 370, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("7", 430, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("8", 490, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("9", 550, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("0", 610, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("-", 670, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("=", 730, 70, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("Backspace", 790, 70, 110, 50, {"full", "tenkeyless", "sixty"}),
    ("Insert", 910, 70, 50, 50, {"full", "tenkeyless"}),
    ("Home", 970, 70, 50, 50, {"full", "tenkeyless"}),
    ("Page Up", 1030, 70, 50, 50, {"full", "tenkeyless"}),
    ("Tab", 10, 130, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Q", 95, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("W", 155, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("E", 215, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("R", 275, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("T", 335, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("Y", 395, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("U", 455, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("I", 515, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("O", 575, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("P", 635, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("[", 695, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("]", 755, 130, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("\\", 815, 130, 85, 50, {"full", "tenkeyless", "sixty"}),
    ("Delete", 910, 130, 50, 50, {"full", "tenkeyless"}),
    ("End", 970, 130, 50, 50, {"full", "tenkeyless"}),
    ("Page Down", 1030, 130, 50, 50, {"full", "tenkeyless"}),
    ("Caps Lock", 10, 190, 85, 50, {"full", "tenkeyless", "sixty"}),
    ("A", 105, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("S", 165, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("D", 225, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("F", 285, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("G", 345, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("H", 405, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("J", 465, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("K", 525, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("L", 585, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    (";", 645, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("'", 705, 190, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("Enter", 765, 190, 135, 50, {"full", "tenkeyless", "sixty"}),
    ("Shift", 10, 250, 125, 50, {"full", "tenkeyless", "sixty"}),
    ("Z", 145, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("X", 205, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("C", 265, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("V", 325, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("B", 385, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("N", 445, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("M", 505, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    (",", 565, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    (".", 625, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("/", 685, 250, 50, 50, {"full", "tenkeyless", "sixty"}),
    ("Shift", 745, 250, 155, 50, {"full", "tenkeyless", "sixty"}),
    ("Up", 970, 250, 50, 50, {"full", "tenkeyless"}),
    ("Ctrl", 10, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Win", 95, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Alt", 180, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Space", 265, 310, 380, 50, {"full", "tenkeyless", "sixty"}),
    ("Alt", 655, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Win", 740, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Ctrl", 825, 310, 75, 50, {"full", "tenkeyless", "sixty"}),
    ("Left", 910, 310, 50, 50, {"full", "tenkeyless"}),
    ("Down", 970, 310, 50, 50, {"full", "tenkeyless"}),
    ("Right", 1030, 310, 50, 50, {"full", "tenkeyless"}),
    # Numeric keypad for full layout
    ("Num Lock", 1090, 70, 50, 50, {"full"}),
    ("/", 1150, 70, 50, 50, {"full"}),
    ("*", 1210, 70, 50, 50, {"full"}),
    ("-", 1270, 70, 50, 50, {"full"}),
    ("7", 1090, 130, 50, 50, {"full"}),
    ("8", 1150, 130, 50, 50, {"full"}),
    ("9", 1210, 130, 50, 50, {"full"}),
    ("+", 1270, 130, 50, 110, {"full"}),
    ("4", 1090, 190, 50, 50, {"full"}),
    ("5", 1150, 190, 50, 50, {"full"}),
    ("6", 1210, 190, 50, 50, {"full"}),
    ("1", 1090, 250, 50, 50, {"full"}),
    ("2", 1150, 250, 50, 50, {"full"}),
    ("3", 1210, 250, 50, 50, {"full"}),
    ("Enter", 1270, 250, 50, 110, {"full"}),
    ("0", 1090, 310, 110, 50, {"full"}),
    (".", 1210, 310, 50, 50, {"full"})
]

# Set the layout variables
isSixty = False
isTenKeyless = True
isFullSized = False

# Determine the current layout
if isSixty:
    current_layout = "sixty"
elif isTenKeyless:
    current_layout = "tenkeyless"
elif isFullSized:
    current_layout = "full"
else:
    current_layout = None

# Create and place the buttons
for key in keys:
    text, x, y, width, height, layouts = key
    if current_layout in layouts:
        button = tk.Button(root, text=text, width=width, height=height, relief='raised', bd=4, wraplength=width*0.8)
        button.place(x=x, y=y, width=width, height=height)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# Set the size of the window
root.geometry("1330x370")

# Start the tkinter event loop
root.mainloop()