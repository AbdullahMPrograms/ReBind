import customtkinter as ctk
from PIL import Image, ImageTk
import ast

#--------------ROOT FRAME---------------
# Create a new CustomTkinter window
root = ctk.CTk()
root.title("ReBind")
#------------ROOT FRAME END-------------

#--------------DEBUG FUNCTIONS---------------
def button_event(button_name):
    print(f"{button_name} clicked")

# Create a function to print the current window size
def print_window_size():
    print(f"Current window size: {root.winfo_width()}x{root.winfo_height()}")
    print(f"Main frame size: {main_frame.winfo_width()}x{main_frame.winfo_height()}")
    print(f"Home frame size: {home_frame.winfo_width()}x{home_frame.winfo_height()}")
    print(f"Home frame width: {home_frame['width']}")
    print(f"Keys frame size: {keys_frame.winfo_width()}x{keys_frame.winfo_height()}")
    print(f"Sidebar size: {sidebar.winfo_width()}x{sidebar.winfo_height()}")
    print(f"Version frame placement: x={version_frame.winfo_x()}, y={version_frame.winfo_y()}")
    print(f"modification frame placement: x={modification_frame.winfo_width()}")
#------------DEBUG FUNCTIONS END-------------
  
#--------------MAIN FRAME---------------
# Create a main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(side='left', fill='both', expand=True)
#------------MAIN FRAME END-------------

#--------------SIDEBAR FRAME---------------
# Create a sidebar inside the main frame
sidebar = ctk.CTkFrame(main_frame, fg_color="transparent")
sidebar.pack_propagate(0)  # Don't allow the widgets inside to dictate the frame's width
sidebar.pack(side='left', fill='y')

# Create a variable to keep track of whether the sidebar is expanded or not
sidebar_expanded = False

# Create a function to toggle the sidebar
# Update the toggle_sidebar function to hide/show the labels
def toggle_sidebar():
    global sidebar_expanded
    if sidebar_expanded:
        sidebar.configure(width=70)
        menu_label.configure(text="", width=0)
        home_label.configure(text="", width=0)
        macros_label.configure(text="", width=0)
        plugin_label.configure(text="", width=0)
        save_label.configure(text="", width=0)
        settings_label.configure(text="", width=0)
        sidebar_expanded = False
    else:
        sidebar.configure(width=200)  # Change this to the expanded width you want
        menu_label.configure(text="Hide")
        home_label.configure(text="Home")
        macros_label.configure(text="Macros")
        plugin_label.configure(text="Plugins")
        save_label.configure(text="Profiles")
        settings_label.configure(text="Settings")  
        sidebar_expanded = True
#-----SIDEBAR FRAME END------

#--------------SIDEBAR BUTTONS---------------
menu_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
home_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
macros_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
save_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
plugins_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
settings_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
menu_frame.pack(side='top', fill='x')

# Create the Home button inside the home frame
menu_button = ctk.CTkButton(menu_frame, image=menu_image, text = "", width=70, height=50, fg_color = "transparent", command=toggle_sidebar)
menu_button.pack(side='left')

# Create a label for the home button
menu_label = ctk.CTkLabel(menu_frame, text="", fg_color="transparent")
menu_label.pack(side='left')

# Create a frame for the home button
home_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
home_frame.pack(side='top', fill='x')

# Create the Home button inside the home frame
home_button = ctk.CTkButton(home_frame, image=home_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Home'))
home_button.pack(side='left')

# Create a label for the home button
home_label = ctk.CTkLabel(home_frame, text="", fg_color="transparent")
home_label.pack(side='left')

# Create a frame for the macros button
macros_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
macros_frame.pack(side='top', fill='x')

# Create the Macros button inside the macros frame
macros_button = ctk.CTkButton(macros_frame, image=macros_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Macros'))
macros_button.pack(side='left')

# Create a label for the macros button
macros_label = ctk.CTkLabel(macros_frame, text="", fg_color="transparent")
macros_label.pack(side='left')

# Create a frame for the plugin button
plugin_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
plugin_frame.pack(side='top', fill='x')

# Create the Plugin button inside the plugin frame
plugin_button = ctk.CTkButton(plugin_frame, image=plugins_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Plugins'))
plugin_button.pack(side='left')

# Create a label for the plugin button
plugin_label = ctk.CTkLabel(plugin_frame, text="", fg_color="transparent")
plugin_label.pack(side='left')

# Create a frame for the save button
save_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
save_frame.pack(side='top', fill='x')

# Create the Save button inside the save frame
save_button = ctk.CTkButton(save_frame, image=save_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Profiles'))
save_button.pack(side='left')

# Create a label for the save button
save_label = ctk.CTkLabel(save_frame, text="", fg_color="transparent")
save_label.pack(side='left')

# Create a frame for the settings button
settings_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
settings_frame.pack(side='bottom', fill='x')

# Create the Settings button inside the settings frame
settings_button = ctk.CTkButton(settings_frame, image=settings_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: button_event('Settings'))
settings_button.pack(side='left')

# Create a label for the settings button
settings_label = ctk.CTkLabel(settings_frame, text="1", bg_color="transparent")
settings_label.pack(side='left')
#-----SIDEBAR BUTTONS END------

#--------------HOME FRAME---------------
# Create a home frame inside the main frame with a specific height
home_frame = ctk.CTkFrame(main_frame)
home_frame.pack(side='top', fill='both', expand=True)
#-----HOME FRAME END------

#--------------MODIFICATION FRAME---------------
# Create a frame at the top of the parent_frame to hold the labels and dropdown menus
modification_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
modification_frame.pack(side='top', expand=False)  # Pack to the left of the parent_frame

# Create labels and dropdown menus in the modification frame
program_label = ctk.CTkLabel(modification_frame, text="Program Name:")
program_label.pack(side='left', padx=(0, 10))  # Reduce padding to 10 pixels
program_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
program_dropdown.pack(side='left', pady=5)  # Add 50 pixels of padding to the left

modifier_label = ctk.CTkLabel(modification_frame, text="Modifier Key:")
modifier_label.pack(side='left', padx=(50, 10))  # Reduce padding to 10 pixels
modifier_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
modifier_dropdown.pack(side='left', pady=5)  # Add 50 pixels of padding to the right

layer_label = ctk.CTkLabel(modification_frame, text="Layer:")
layer_label.pack(side='left', padx=(50, 10))  # Reduce padding to 10 pixels
layer_segbutton = ctk.CTkSegmentedButton(modification_frame, values=["0","1", "2", "3"])
layer_segbutton.set("0")
layer_segbutton.pack(side='left', pady=5) 
#------------MODIFICATION FRAME END-------------

#--------------KEYS FRAME---------------
max_x = 0
max_y = 0

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

# Create a frame for the keys inside the home_frame
keys_frame = ctk.CTkFrame(home_frame, bg_color="transparent")
keys_frame.pack(side='top', fill='both', expand=True)

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
        button.place(x=x, y=y)
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)
#------------KEYS FRAME END-------------

#--------------VERSION FRAME---------------
# Create a version frame inside the main frame with a specific height
version_frame = ctk.CTkFrame(main_frame, height=20, fg_color="transparent")
version_frame.pack(side='bottom', fill='x')

# Create a label with a text message on the far right of the version frame
version_label = ctk.CTkLabel(version_frame, text="v0.0.1", padx = (15), anchor='e')
version_label.pack(side='right')
#------------VERSION FRAME END-------------

#------------FINAL FRAME PLACEMENTS-------------
# Adjust the size of the keys_frame to fit the keys
keys_frame.configure(width=max_x + 10, height=max_y + 10)

# Adjust the size of the home_frame to fit the keys_frame
home_frame.configure(width=sidebar['width'] + home_frame['width'], height=max_y + 170)

# Adjust the size of the main_frame to fit the home_frame
main_frame.configure(width=sidebar['width'] + home_frame['width'], height=max_y + 210)

sidebar.configure(width=70, height=main_frame['height'])

root.geometry(f"{max_x + sidebar['width'] + 100}x{sidebar['height']}")

# Center the keys_frame within the home_frame
keys_frame.place(relx=0.5, rely=0.5, anchor='center')
#------------FINAL FRAME PLACEMENTS END-------------

# Lock the window size
root.resizable(False, False)

# Start the CustomTkinter event loop
root.mainloop()