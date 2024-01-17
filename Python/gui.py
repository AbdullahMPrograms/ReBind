import customtkinter as ctk
from PIL import Image, ImageTk
import ast
import os
import configparser

class MyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ReBind")
        self.root.minsize(1250, 570) #Tenkeyless size, works well with 60%
        self.themes = self.get_available_themes()
        self.set_theme(self.themes[0])  # Set the first available theme
        self.layouts = self.get_available_layouts()
        self.set_layout(self.layouts[3])  # Set the first available layout
        self.sidebar_expanded = False
        self.main_frame = self.create_main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.home_frame = self.create_home_frame()
        self.macro_frame = self.create_macro_frame()
        self.plugin_frame = self.create_plugin_frame()
        self.profile_frame = self.create_profile_frame()
        self.settings_frame = self.create_settings_frame()
        self.modification_frame = self.create_modification_frame()
        self.keys_frame = self.create_keys_frame()
        self.current_buttons = []
        self.version_frame = self.create_version_frame()
        self.create_sidebar_buttons()
        self.general_settings_frame = self.create_general_settings_frame()
        self.draw_frame('home')

    def get_available_themes(self):
        themes = []
        theme_files = os.listdir("Python/Themes")
        for file in theme_files:
            if file.endswith('.ini'):
                themes.append(file[:-4])  # Remove the .ini extension
        print('Detected themes:', themes)
        return themes

    def set_theme(self, theme):
        print("Setting theme:", theme)
        config = configparser.ConfigParser()
        config.read(f'Python/Themes/{theme}.ini')
        colours = config['colours']
        self.bg_colour = colours['background']
        self.main_colour = colours['main']
        self.button_hover_colour = colours['button_hover']
        self.button_press_colour = colours['button_press']
        self.button_selected_colour = colours['button_selected']
        self.segmented_button_hover_colour = colours['segmented_button_hover']
        self.keys_frame_colour = colours['keys_frame']
        self.key_button_colour = colours['key_button']

    def get_available_layouts(self):
        layouts = []
        layout_files = os.listdir("Python/Layouts")
        for file in layout_files:
            if file.endswith('.ini'):
                layouts.append(file[:-4])  # Remove the .ini extension
        print('Detected layouts:', layouts)
        return layouts

    def set_layout(self, layout):
        print("Setting layout:", layout)
        self.keys = self.get_layout_keys(layout)

    def get_layout_keys(self, layout):
        with open(f'Python/Layouts/{layout}.ini', 'r') as file:
            keys = ast.literal_eval(file.read())
        return keys

    def get_remap_keys(self):
        with open(f'Python/remap_keys.ini', 'r') as file:
            remap_keys = ast.literal_eval(file.read())
        return remap_keys

    def draw_replace_key(self, button_name):
        self.replace_key_window = ctk.CTkToplevel(self.root)
        self.replace_key_window.geometry('400x460')
        self.key_to_be_replaced = button_name

        modifier = self.modifier_dropdown.get()

        title = f"Replace Key: "
        if modifier:
            title += f"{modifier} + "
        title += button_name

        program = self.program_dropdown.get()
        if program:
            title += f" for {program}"
        self.replace_key_window.title(title)

        self.replace_key_window.grab_set()
        self.replace_key_window.attributes('-topmost', True)

        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        window_width = 400
        window_height = 460
        pos_x = root_x + (root_width - window_width) // 2
        pos_y = root_y + (root_height - window_height) // 2

        self.replace_key_window.geometry(f"+{pos_x}+{pos_y}")

        search_frame = ctk.CTkFrame(self.replace_key_window)
        search_frame.pack(side='top', fill='x', padx=40, pady=(40,0))

        search_var = ctk.StringVar()
        search_bar = ctk.CTkEntry(search_frame, textvariable=search_var, height=35)
        search_bar.pack(fill='x')

        keys_frame = ctk.CTkScrollableFrame(self.replace_key_window, fg_color="transparent")
        keys_frame.pack(side='top', fill='both', expand=True, padx=40, pady=20)

        self.current_buttons = []
        self.key_buttons = []

        buttons_frame = ctk.CTkFrame(self.replace_key_window, fg_color="transparent")
        buttons_frame.pack(side='top', fill='x', padx=80, pady=(10,15))
        self.save_button = ctk.CTkButton(buttons_frame, width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Save", command=self.save_replaced_key)
        self.save_button.configure(state='disabled')
        self.save_button.pack(side='left')
        reset_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Reset", command=self.reset_replaced_key)
        reset_button.pack_forget()  # Hide the Reset button initially
        cancel_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Cancel", command=self.replace_key_window.destroy)
        cancel_button.pack(side='right')

        for key, original_key in self.get_remap_keys():
            key_button = ctk.CTkButton(keys_frame, text=key, height=45, fg_color="transparent", hover_color=self.button_hover_colour, border_width=2, text_color=("gray10", "#DCE4EE"))
            key_button.configure(command=lambda key_button=key_button, text=key: self.update_search_bar(key_button, text, search_bar))
            key_button.pack(side='top', fill='x', padx=0, pady=5)
            self.key_buttons.append(key_button)

            # Check if the clicked key's original value and key value are different
            if key == self.key_to_be_replaced and key != original_key:
                print(f"Original key: {key} does not match Remapped key: {original_key}")
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)  # Show the Reset button in the center
        
        def update_buttons(*args):
            search_term = search_var.get().lower()

            # If the search term ends with '+', show all buttons
            if search_term.strip().endswith('+'):
                for key_button in self.key_buttons:
                    key_button.pack(side='top', fill='x', padx=0, pady=5)
            else:
                for key_button in self.key_buttons:
                    key_button.pack_forget()

                for key_button in self.current_buttons:
                    key_button.pack(side='top', fill='x', padx=0, pady=5)

                search_terms = search_term.split('+')
                for term in search_terms:
                    term = term.strip()
                    for key_button in self.key_buttons:
                        key_text = key_button.cget("text").lower()
                        if term == key_text and key_button not in self.current_buttons:
                            key_button.pack(side='top', fill='x', padx=0, pady=5)

                    for key_button in self.key_buttons:
                        key_text = key_button.cget("text").lower()
                        if term in key_text and key_button not in self.current_buttons and term != key_text:
                            key_button.pack(side='top', fill='x', padx=0, pady=5)

        search_var.trace("w", update_buttons)         

                
    def update_search_bar(self, key_button, text, search_bar):
        current_text = search_bar.get()
        self.select_button(key_button, text)

        # If this button is not selected
        if key_button not in self.current_buttons:
            # Remove the text of the button from the search bar
            parts = current_text.split(' + ')
            parts.remove(text)
            new_text = ' + '.join(parts)
        else:
            # Replace the current text in the search bar with the button text
            if '+' in current_text:
                base_text, _ = current_text.rsplit('+', 1)
                new_text = base_text + '+ ' + text
            else:
                new_text = text

        # Update the search bar
        search_bar.delete(0, 'end')
        search_bar.insert(0, new_text.strip())

    def save_replaced_key(self):
        # Get the selected options
        program = self.program_dropdown.get()
        focus = self.focus_dropdown.get()
        modifier = self.modifier_dropdown.get()
        layer = self.layer_var.get()

        # Start building the print statement
        replaced_key = ""
        if modifier:
            replaced_key += f"{modifier} + "
        replaced_key += f"{self.key_to_be_replaced} has been replaced with "
        
        # Get the names of the selected keys
        selected_keys = [button.cget('text') for button in self.current_buttons]
        
        # Add the selected keys to the print statement
        replaced_key += " + ".join(selected_keys)
        
        if program:
            replaced_key += f" for {program}"
        if focus:
            replaced_key += f", Requires Focus: {focus}"
        replaced_key += f" on Layer: {layer}"
        
        print(replaced_key)

        # Update the remap_keys.ini file
        remap_keys = self.get_remap_keys()
        for i, (key, original_key) in enumerate(remap_keys):
            if key == self.key_to_be_replaced:
                remap_keys[i] = (key, " + ".join(selected_keys))

        with open('Python/remap_keys.ini', 'w') as file:
            file.write("[\n")
            for key, original_key in remap_keys:
                # Handle the special case for "\"
                if key == "\\":
                    key = "\\\\"
                if original_key == "\\":
                    original_key = "\\\\"
                file.write(f"    (\"{key}\", \"{original_key}\"),\n")
            file.write("]\n")

        self.replace_key_window.destroy()
        self.current_buttons.clear()  # Clear the list of selected buttons

    def reset_replaced_key(self):
        # Update the remap_keys.ini file
        remap_keys = self.get_remap_keys()
        for i, (key, original_key) in enumerate(remap_keys):
            if key == self.key_to_be_replaced:
                remap_keys[i] = (key, key)  # Reset the key value to the original key value

        with open('Python/remap_keys.ini', 'w') as file:
            file.write("[\n")
            for key, original_key in remap_keys:
                # Handle the special case for "\"
                if key == "\\":
                    key = "\\\\"
                if original_key == "\\":
                    original_key = "\\\\"
                file.write(f"    (\"{key}\", \"{original_key}\"),\n")
            file.write("]\n")

        print(f"Key: {self.key_to_be_replaced} has been reset to its original value.")
        self.replace_key_window.destroy()

    def select_button(self, key_button, text):
        print(f"{text} selected")
        if key_button in self.current_buttons:  # If this button is already selected
            self.current_buttons.remove(key_button)  # Deselect it
            key_button.configure(fg_color="transparent")
        else:  # If this button is not selected
            self.current_buttons.append(key_button)  # Select it
            key_button.configure(fg_color=self.button_selected_colour)
        self.save_button.configure(state='normal' if self.current_buttons else 'disabled')

    def print_window_size(self):
        print(f"Current window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Main frame size: {self.main_frame.winfo_width()}x{self.main_frame.winfo_height()}")
        print(f"Home frame size: {self.home_frame.winfo_width()}x{self.home_frame.winfo_height()}")
        print(f"Sidebar size: {self.sidebar_frame.winfo_width()}x{self.sidebar_frame.winfo_height()}")
        
    def toggle_sidebar(self):
        self.SIDEBAR_WIDTH_COLLAPSED = 70
        self.SIDEBAR_WIDTH_EXPANDED = 200
        
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_COLLAPSED)
            self.menu_label.configure(text="", width=0)
            self.home_label.configure(text="", width=0)
            self.macros_label.configure(text="", width=0)
            self.plugin_label.configure(text="", width=0)
            self.profile_label.configure(text="", width=0)
            self.settings_label.configure(text="", width=0)
            self.sidebar_expanded = False
        else:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_EXPANDED)
            self.menu_label.configure(text="Hide")
            self.home_label.configure(text="Home")
            self.macros_label.configure(text="Macros")
            self.plugin_label.configure(text="Plugins")
            self.profile_label.configure(text="Profiles")
            self.settings_label.configure(text="Settings")  
            self.sidebar_expanded = True

    def draw_frame(self, frame_name):
        self.home_frame.pack_forget()
        self.macro_frame.pack_forget()
        self.plugin_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.settings_frame.pack_forget()

        if frame_name == 'home':
            self.home_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'macro':
            self.macro_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'plugin':
            self.plugin_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'profile':
            self.profile_frame.pack(side='top', fill='both', expand=True)   
        elif frame_name == 'settings':
            self.settings_frame.pack(side='top', fill='both', expand=True)
        
    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root, fg_color=self.main_colour)
        main_frame.pack(side='left', fill='both', expand=True)
        return main_frame
        
    def create_version_frame(self):
        version_frame = ctk.CTkFrame(self.main_frame, height=20, fg_color=self.main_colour)
        version_frame.pack(side='bottom', fill='x')
        version_label = ctk.CTkLabel(version_frame, text="v0.0.1", padx=15, anchor='e')
        version_label.pack(side='right')
        return version_frame
    
    def create_sidebar_frame(self):
        sidebar_frame = ctk.CTkFrame(self.main_frame, fg_color=self.main_colour)   
        sidebar_frame.pack_propagate(False)
        sidebar_frame.pack(side='left', fill='y')
        return sidebar_frame

    def create_sidebar_buttons(self):
        menu_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
        home_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
        macros_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
        save_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
        plugins_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
        windowsize_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_windowsize.png").resize((16,16), Image.Resampling.LANCZOS))
        settings_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

        menu_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        menu_frame.pack(side='top', fill='x')
        self.menu_button = ctk.CTkButton(menu_frame, image=menu_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.button_hover_colour, command=self.toggle_sidebar)
        self.menu_button.pack(side='left')
        self.menu_label = ctk.CTkLabel(menu_frame, text="")
        self.menu_label.pack(side='left')

        home_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        home_frame.pack(side='top', fill='x')
        self.home_button = ctk.CTkButton(home_frame, image=home_image, text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=lambda: self.draw_frame('home'))
        self.home_button.pack(side='left')
        self.home_label = ctk.CTkLabel(home_frame, text="")
        self.home_label.pack(side='left')

        macros_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        macros_frame.pack(side='top', fill='x')
        self.macros_button = ctk.CTkButton(macros_frame, image=macros_image, text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=lambda: self.draw_frame('macro'))
        self.macros_button.pack(side='left')
        self.macros_label = ctk.CTkLabel(macros_frame, text="")
        self.macros_label.pack(side='left')

        plugin_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        plugin_frame.pack(side='top', fill='x')
        self.plugin_button = ctk.CTkButton(plugin_frame, image=plugins_image, text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=lambda: self.draw_frame('plugin'))
        self.plugin_button.pack(side='left')
        self.plugin_label = ctk.CTkLabel(plugin_frame, text="")
        self.plugin_label.pack(side='left')

        profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        profile_frame.pack(side='top', fill='x')
        self.profile_button = ctk.CTkButton(profile_frame, image=save_image, text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=lambda: self.draw_frame('profile'))
        self.profile_button.pack(side='left')
        self.profile_label = ctk.CTkLabel(profile_frame, text="")
        self.profile_label.pack(side='left')
        
        window_size_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        window_size_frame.pack(side='top', fill='x')
        self.window_size_button = ctk.CTkButton(window_size_frame, image=windowsize_image ,text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=self.print_window_size)
        self.window_size_button.pack(side='left')   
        self.window_size_label = ctk.CTkLabel(window_size_frame, text="")
        self.window_size_label.pack(side='left')

        settings_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        settings_frame.pack(side='bottom', fill='x')
        self.settings_button = ctk.CTkButton(settings_frame, image=settings_image, text = "", width=70, height=50, fg_color = "transparent", hover_color=self.button_hover_colour, command=lambda: self.draw_frame('settings'))
        self.settings_button.pack(side='left')
        self.settings_label = ctk.CTkLabel(settings_frame, text="")
        self.settings_label.pack(side='left')
    
    def create_home_frame(self):
        home_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_colour)
        home_frame.pack(side='top', fill='both', expand=True)
        return home_frame
    
    def create_modification_frame(self):
        modification_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        modification_frame.pack(side='top', expand=False)

        self.program_var = ctk.StringVar()
        self.focus_var = ctk.StringVar()
        self.modifier_var = ctk.StringVar()
        self.layer_var = ctk.StringVar()

        # Create a new frame for the program and focus dropdowns
        program_focus_frame = ctk.CTkFrame(modification_frame, fg_color="transparent")
        program_focus_frame.pack(side='left')

        program_label = ctk.CTkLabel(program_focus_frame, text="Program Name:")
        program_label.pack(side='left', padx=(0, 10))
        self.program_dropdown = ctk.CTkComboBox(program_focus_frame, variable=self.program_var, values=["", "Option 1", "Option 2", "Option 3"])
        self.program_dropdown.set("")
        self.program_dropdown.pack(side='left', pady=5)

        # Add a trace to the program_var
        self.program_var.trace('w', self.update_focus_dropdown)

        # Create the focus dropdown and initially hide it
        self.focus_label = ctk.CTkLabel(program_focus_frame, text="Requires Focus:")
        self.focus_label.pack(side='left')
        self.focus_label.pack_forget()
        self.focus_dropdown = ctk.CTkComboBox(program_focus_frame, variable=self.focus_var, values=["Yes", "No"])
        self.focus_dropdown.set("")
        self.focus_dropdown.pack(side='left')
        self.focus_dropdown.pack_forget()

        modifier_label = ctk.CTkLabel(modification_frame, text="Modifier Key:")
        modifier_label.pack(side='left', padx=(50, 10))
        self.modifier_dropdown = ctk.CTkComboBox(modification_frame, variable=self.modifier_var, values=["", "Option 1", "Option 2", "Option 3"])
        self.modifier_dropdown.set("")
        self.modifier_dropdown.pack(side='left', pady=5)

        layer_label = ctk.CTkLabel(modification_frame, text="Layer:")
        layer_label.pack(side='left', padx=(50, 10))
        layer_segbutton = ctk.CTkSegmentedButton(modification_frame, variable=self.layer_var, selected_color=self.button_selected_colour, selected_hover_color=self.button_hover_colour, unselected_hover_color=self.segmented_button_hover_colour, values=["0","1", "2", "3"])
        layer_segbutton.set("0")
        layer_segbutton.pack(side='left', pady=5) 
        return modification_frame

    def update_focus_dropdown(self, *args):
        if self.program_var.get():
            self.focus_label.pack(side='left', padx=(50, 10))
            self.focus_dropdown.pack(side='left', pady=5)
            self.focus_dropdown.set("Yes")
        else:
            self.focus_dropdown.set("")
            self.focus_label.pack_forget()
            self.focus_dropdown.pack_forget()
        
    def shrink_button(self, button, original_x, original_y, original_width, original_height, original_font_size):
        shrink_factor_button = 0.93  # Adjust this value as needed
        shrink_factor_font = 0.95  # Adjust this value as needed
        button.configure(width=original_width*shrink_factor_button, height=original_height*shrink_factor_button, fg_color=self.button_hover_colour)
        button.place_configure(x=original_x+(original_width*(1-shrink_factor_button)/2), y=original_y+(original_height*(1-shrink_factor_button)/2))
        new_font_size = int(original_font_size*shrink_factor_font) # Adjust this value as needed
        button._text_label.configure(font=("Roboto", new_font_size))

    def restore_button(self, button, original_x, original_y, original_width, original_height, original_font_size):
        button.configure(width=original_width, height=original_height, fg_color=self.key_button_colour)
        button.place_configure(x=original_x, y=original_y)
        button._text_label.configure(font=("Roboto", original_font_size))

    def create_keys_frame(self):
        max_x = 0
        max_y = 0

        keys_frame = ctk.CTkFrame(self.home_frame, fg_color=self.keys_frame_colour)
        keys_frame.pack(side='top', fill='both', expand=True)

        for key in self.keys:
            text, x, y, width, height = key
            button = ctk.CTkButton(keys_frame, text=text, width=width, height=height, fg_color=self.key_button_colour, command=lambda text=text: self.draw_replace_key(text))
            button._text_label.configure(wraplength=width*0.8)  # Configure word wrap
            button.place(x=x, y=y)
            original_font_size = int(button._text_label.cget("font").split(" ")[1])
            button.bind("<Enter>", lambda event, button=button, x=x, y=y, width=width, height=height, original_font_size=original_font_size: self.shrink_button(button, x, y, width, height, original_font_size))
            button.bind("<Leave>", lambda event, button=button, x=x, y=y, width=width, height=height, original_font_size=original_font_size: self.restore_button(button, x, y, width, height, original_font_size))
            max_x = max(max_x, x + width)
            max_y = max(max_y, y + height)

        keys_frame.configure(width=max_x + 10, height=max_y + 10)
        self.home_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 170) #this is a concern, I would rather not have to hardcode this
        self.main_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 210)
        self.sidebar_frame.configure(width=70, height=self.main_frame['height'])
        self.root.geometry(f"{max_x + self.sidebar_frame['width'] + 100}x{self.sidebar_frame['height']}")
        keys_frame.place(relx=0.5, rely=0.5, anchor='center')
        return keys_frame

    def create_macro_frame(self):
        macro_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_colour)
        macro_frame.pack(side='top', fill='both', expand=True)
        macro_label = ctk.CTkLabel(macro_frame, text="MACROS PAGE")
        macro_label.pack(side='top')
        return macro_frame
    
    def create_plugin_frame(self):
        plugin_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_colour)
        plugin_frame.pack(side='top', fill='both', expand=True)
        plugin_label = ctk.CTkLabel(plugin_frame, text="PLUGIN PAGE")
        plugin_label.pack(side='top')
        return plugin_frame
    
    def create_profile_frame(self):
        profile_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_colour)
        profile_frame.pack(side='top', fill='both', expand=True)
        profile_label = ctk.CTkLabel(profile_frame, text="PROFILE/SAVE PAGE")
        profile_label.pack(side='top')
        return profile_frame
    
    def create_settings_frame(self):
        settings_frame = ctk.CTkFrame(self.main_frame, fg_color=self.bg_colour)
        settings_frame.pack(side='top', fill='both', expand=True)
        return settings_frame

    def create_general_settings_frame(self):        
        general_settings_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        general_settings_frame.pack(side='top', fill='both', expand=True)
        general_settings_label = ctk.CTkLabel(general_settings_frame, text="GENERAL", font=('Bold', 22))
        general_settings_label.pack(side='top', pady=(10,50))
        
        theme_frame = ctk.CTkFrame(general_settings_frame, bg_color="transparent", height=45)
        theme_frame.pack(side='top', fill='x', padx=165, pady=(0,5))
        theme_frame.pack_propagate(False)
        theme_label = ctk.CTkLabel(theme_frame, text="Theme")
        theme_label.pack(side='left')
        theme_dropdown = ctk.CTkOptionMenu(theme_frame)
        theme_dropdown.pack(side='right')
        
        key_tester_frame = ctk.CTkFrame(general_settings_frame, bg_color="transparent", height=45)
        key_tester_frame.pack(side='top', fill='x', padx=165)
        key_tester_frame.pack_propagate(False)
        key_tester_label = ctk.CTkLabel(key_tester_frame, text="Enable Key Tester")
        key_tester_label.pack(side='left')
        key_tester_switch = ctk.CTkSwitch(key_tester_frame, text="")
        key_tester_switch.pack(side='right')
        
        return general_settings_frame
    
    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()

app = MyApp()
app.run()