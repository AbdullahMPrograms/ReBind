import customtkinter as ctk
from PIL import Image, ImageTk
import ast

# might need to make the keysframe the total outside size of the keys then place that frame in another frame and center it, rn the spacing is so dumb

# Create a new CustomTkinter window
root = ctk.CTk()
root.title("ReBind")

menu_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
home_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
macros_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
save_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
plugins_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
settings_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

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

max_x = 0
max_y = 0

def button_event(button_name):
    print(f"{button_name} clicked")

# Create a function to print the current window size
def print_window_size():
    print(f"Current window size: {root.winfo_width()}x{root.winfo_height()}")
    print(f"Main frame size: {main_frame.winfo_width()}x{main_frame.winfo_height()}")
    print(f"Home frame size: {home_frame.winfo_width()}x{home_frame.winfo_height()}")
    print(f"Keys frame size: {keys_frame.winfo_width()}x{keys_frame.winfo_height()}")
    print(f"Sidebar size: {sidebar.winfo_width()}x{sidebar.winfo_height()}")
    print(f"Version frame placement: x={version_frame.winfo_x()}, y={version_frame.winfo_y()}")
    
# Define a StringVar to track the state of the switch
switch_state = ctk.StringVar(value="off")

# Define the mode_switch function before creating the CTkSwitch
def mode_switch():
    modification_frame.update_idletasks()
    if switch_state.get() == "on":
        modification_frame.configure(bg_color="transparent")  # Replace "color1" with the color you want
    if switch_state.get() == "off":
        modification_frame.configure(fg_color="transparent")  # Replace "color2" with the color you want
    print("switch toggled, current value:", switch_state.get())
    
# Create a variable to keep track of whether the sidebar is expanded or not
sidebar_expanded = False

# Create a function to toggle the sidebar
# maybe make keys_frame x = -50 so that keys frame wont move (dumb solution ik)
def toggle_sidebar():
    global sidebar_expanded
    if sidebar_expanded:
        sidebar.configure(width=70)
        home_button.configure(compound="none")  # Hide the text
        sidebar_expanded = False
    else:
        sidebar.configure(width=200)  # Change this to the expanded width you want
        home_button.configure(compound="left")  # Show the text to the left of the image
        sidebar_expanded = True

# ROOT Frame
# Create a main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(side='left', fill='both', expand=True)

# Create a sidebar inside the main frame
sidebar = ctk.CTkFrame(main_frame, fg_color="transparent")
sidebar.pack(side='left', fill='y')

# SIDEBAR BUTTONS
# Create a hamburger menu inside the sidebar
hamburger_menu = ctk.CTkButton(sidebar, image=menu_image, text = "", width=70, height=50, fg_color = "transparent", command=toggle_sidebar)
hamburger_menu.place(x=0, y=0)

# Create the Home, Macros, Save, and Settings buttons
home_button = ctk.CTkButton(sidebar, image=home_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Home'))
home_button.place(x=0, y=50)

macros_button = ctk.CTkButton(sidebar, image=macros_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Macros'))
macros_button.place(x=0, y=100)

plugin_button = ctk.CTkButton(sidebar, image=plugins_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Plugins'))
plugin_button.place(x=0, y=150)

#Profiles
save_button = ctk.CTkButton(sidebar, image=save_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Profiles'))
save_button.place(x=0, y=200)

# Create a Print Size button and place it above the Settings button
print_size_button = ctk.CTkButton(sidebar, text="Size", width=70, height=50, fg_color = "transparent", command=print_window_size)
print_size_button.place(x=0, y=410)  # Adjust the y coordinate

# HOME FRAME
# Create a home frame inside the main frame with a specific height
home_frame = ctk.CTkFrame(main_frame)
home_frame.pack(side='top', fill='both', expand=True)

# Create a frame at the top of the home_frame to hold the switch and label
modification_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
modification_frame.pack(side='top', fill='x')

# Create a spacer Label with a height of 40 pixels
spacer = ctk.CTkLabel(modification_frame, height=20, text = "")
spacer.pack()

# Create a label underneath the switch and pack it to the right of the modification_frame
switch_label = ctk.CTkLabel(modification_frame, text="Advanced")
switch_label.pack(side='right', padx=20)

# Now create the CTkSwitch
switch = ctk.CTkSwitch(modification_frame, text="", variable=switch_state, onvalue="on", offvalue="off", command=mode_switch)
switch.pack(side='right', padx=20)

# Create a frame for the keys inside the home_frame
keys_frame = ctk.CTkFrame(home_frame, bg_color="transparent")
keys_frame.pack(side='top', fill='both', expand=True)

# VERSION FRAME
# Create a version frame inside the main frame with a specific height
version_frame = ctk.CTkFrame(main_frame, height=20, fg_color="transparent")
version_frame.pack(side='bottom', fill='x')

# Create a label with a text message on the far right of the version frame
version_label = ctk.CTkLabel(version_frame, text="v0.0.1     ", anchor='e')
version_label.pack(side='right')

# Read the keys from the 'Keys.ini' file
with open('Python/Layouts/Keys.ini', 'r') as file:
    keys = ast.literal_eval(file.read())

# Create and place the buttons
for key in keys:
    text, x, y, width, height, layouts = key
    if current_layout in layouts:
        # If the current layout is 'sixty', adjust the y-coordinate
        if current_layout == 'sixty':
            y -= 60
        button = ctk.CTkButton(keys_frame, text=text, width=width, height=height, command=lambda text=text: button_event(text))
        button._text_label.configure(wraplength=width*0.8)  # Configure word wrap
        #button.place(x=x+50, y=y+70)  # Add 50 pixels of space on the left and on top
        button.place(x=x, y=y)
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)

# Adjust the size of the keys_frame to fit the keys
keys_frame.configure(width=max_x + 10, height=max_y + 10)

# Adjust the size of the home_frame to fit the keys_frame
home_frame.configure(width=sidebar['width'] + home_frame['width'], height=max_y + 130)

# Adjust the size of the main_frame to fit the home_frame
main_frame.configure(width=sidebar['width'] + home_frame['width'], height=max_y + 170)

# HAS TO BE HERE CAUSE OF THE MAIN FRAME HEIGHT THING
# Create a Settings button and place it at the bottom of the window
settings_button = ctk.CTkButton(sidebar, image=settings_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Settings'))
sidebar.configure(width=70, height=main_frame['height'])
# Place the settings button at the bottom of the window
if current_layout == 'sixty':
    settings_button.place(x=0, y=sidebar['height'] - 50)  # Adjust the y coordinate
else:
    settings_button.place(x=0, y=sidebar['height'] - 50)  # Adjust the y coordinate

print_size_button.place(x=0, y=250)  # Adjust the y coordinate

# Adjust the size of the window to fit the main_frame
root.geometry(f"{max_x + sidebar['width'] + 100}x{sidebar['height']}")

# Center the keys_frame within the home_frame
keys_frame.place(relx=0.5, rely=0.5, anchor='center')

# Lock the window size
root.resizable(False, False)

# Start the CustomTkinter event loop
root.mainloop()