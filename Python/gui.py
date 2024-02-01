import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import json

class MyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ReBind")
        self.root.minsize(1250, 570)
        self.initialize_settings()
        self.initialize_frames()

    def initialize_settings(self):
        self.settings_file = "Python/data/settings.json"
        self.load_settings()
        self.themes = self.get_available_themes()
        self.set_theme(self.current_theme)
        self.layouts = self.get_available_layouts()
        self.set_layout(self.current_layout)
        
    def initialize_frames(self):
        self.main_frame = self.create_main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.home_frame = self.create_home_frame()
        self.macro_frame = self.create_macro_frame()
        self.plugin_frame = self.create_plugin_frame()
        self.profile_frame = self.create_profile_frame()
        self.settings_frame = self.create_settings_frame()
        self.modification_frame = self.create_modification_frame()
        self.keys_frame = self.create_keys_frame()
        self.version_frame = self.create_version_frame()
        self.create_sidebar_buttons()
        self.general_settings_frame = self.create_general_settings_frame()
        self.draw_frame('home')

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.current_theme = settings['theme']
                self.current_layout = settings['layout']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.current_theme = 'EclipseBlack'
            self.current_layout = 'IK75'

    def save_settings(self):
        settings = {
            'theme': self.current_theme,
            'layout': self.current_layout
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    def get_available_themes(self):
        self.available_themes = []
        theme_files = os.listdir("Python/Themes")
        for file in theme_files:
            if file.endswith('.json'):  # Look for .json files instead of .ini
                self.available_themes.append(file[:-5])  # Remove the .json extension
        return self.available_themes

    def set_theme(self, theme):
        with open(f'Python/Themes/{theme}.json', 'r') as f:  # Open the .json file
            config = json.load(f)  # Parse the JSON
        colours = config['colours']
        self.bg_colour = colours['background']
        self.main_colour = colours['main']
        self.button_hover_colour = colours['button_hover']
        self.button_press_colour = colours['button_press']
        self.button_selected_colour = colours['button_selected']
        self.segmented_button_hover_colour = colours['segmented_button_hover']
        self.dropdown_colour = colours['dropdown']
        self.keys_frame_colour = colours['keys_frame']
        self.key_button_colour = colours['key_button']
        self.notification_frame_colour = colours['notification_frame']
        self.selected_frame_indicator_colour = colours['selected_frame_indicator']
        self.current_theme = theme
        self.save_settings()

    def get_available_layouts(self):
        self.available_layouts = []
        layout_files = os.listdir("Python/data/layouts")
        for file in layout_files:
            if file.endswith('.json'):  # Look for .json files instead of .ini
                self.available_layouts.append(file[:-5])  # Remove the .json extension
        return self.available_layouts

    def set_layout(self, layout):
        self.current_layout = layout
        self.save_settings()
        self.keyboard_keys = self.get_layout_keys(layout)

    def get_layout_keys(self, layout):
        with open(f'Python/data/layouts/{layout}.json', 'r') as file:  # Open the .json file
            keys = json.load(file)  # Parse the JSON
        return keys

    def get_remap_keys(self):
        try:
            with open('Python/data/remap_keys.json', 'r') as file:
                remap_keys = json.load(file)
        except FileNotFoundError:
            remap_keys = {"original_keys": {}, "remapped_keys": {"global": {}}}
        return remap_keys

    def draw_replace_key(self, button_name):
        self.replace_key_window = ctk.CTkToplevel(self.root)
        self.replace_key_window.geometry('400x460')
        #self.replace_key_window.resizable(False, False)
        self.key_to_be_replaced = button_name

        modifier = self.modifier_dropdown.get()
        layer = "layer_" + self.layer_var.get()

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

        remap_keys_frame = ctk.CTkScrollableFrame(self.replace_key_window, fg_color="transparent")
        remap_keys_frame.pack(side='top', fill='both', expand=True, padx=40, pady=20)

        self.selected_remappable_keys = []
        self.remappable_keys = []

        buttons_frame = ctk.CTkFrame(self.replace_key_window, fg_color="transparent")
        buttons_frame.pack(side='top', fill='x', padx=80, pady=(10,15))
        self.save_button = ctk.CTkButton(buttons_frame, width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Save", command=self.save_replaced_key)
        self.save_button.configure(state='disabled')
        self.save_button.pack(side='left')
        reset_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Reset", command=self.reset_replaced_key)
        reset_button.pack_forget()  # Hide the Reset button initially
        cancel_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Cancel", command=self.replace_key_window.destroy)
        cancel_button.pack(side='right')

        self.create_buttons(remap_keys_frame, search_bar, buttons_frame, reset_button, program, modifier, layer)

        def update_buttons(*args):
            search_term = search_var.get().lower()

            # If the search term ends with '+', show all buttons
            if search_term.strip().endswith('+'):
                for remappable_key in self.remappable_keys:
                    remappable_key.pack(side='top', fill='x', padx=0, pady=5)
            else:
                for remappable_key in self.remappable_keys:
                    remappable_key.pack_forget()

                for remappable_key in self.selected_remappable_keys:
                    remappable_key.pack(side='top', fill='x', padx=0, pady=5)

                search_terms = search_term.split('+')
                for term in search_terms:
                    term = term.strip()
                    for remappable_key in self.remappable_keys:
                        key_text = remappable_key.cget("text").lower()
                        if term == key_text and remappable_key not in self.selected_remappable_keys:
                            remappable_key.pack(side='top', fill='x', padx=0, pady=5)

                    for remappable_key in self.remappable_keys:
                        key_text = remappable_key.cget("text").lower()
                        if term in key_text and remappable_key not in self.selected_remappable_keys and term != key_text:
                            remappable_key.pack(side='top', fill='x', padx=0, pady=5)

        search_var.trace("w", update_buttons)

    def create_buttons(self, remap_keys_frame, search_bar, buttons_frame, reset_button, program, modifier, layer=None):
        remap_keys = self.get_remap_keys()
        for key in remap_keys["keys"]:
            remappable_key = ctk.CTkButton(remap_keys_frame, text=key, height=45, fg_color="transparent", hover_color=self.button_hover_colour, border_width=2, text_color=("gray10", "#DCE4EE"))
            remappable_key.configure(command=lambda remappable_key=remappable_key, text=key: self.update_search_bar(remappable_key, text, search_bar))
            remappable_key.pack(side='top', fill='x', padx=0, pady=5)
            self.remappable_keys.append(remappable_key)

            # Check if the clicked key's original value and key value are different
            if program and layer and modifier and self.key_to_be_replaced in remap_keys["remapped_keys"].get(program, {}).get(layer, {}).get(modifier, {}) and remap_keys["remapped_keys"][program][layer][modifier][self.key_to_be_replaced]["key"] != key:
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)
            elif program and layer and self.key_to_be_replaced in remap_keys["remapped_keys"].get(program, {}).get(layer, {}) and remap_keys["remapped_keys"][program][layer][self.key_to_be_replaced]["key"] != key:
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)
            elif layer and modifier and self.key_to_be_replaced in remap_keys["remapped_keys"]["global"].get(layer, {}).get(modifier, {}) and remap_keys["remapped_keys"]["global"][layer][modifier][self.key_to_be_replaced]["key"] != key:
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)
            elif layer and self.key_to_be_replaced in remap_keys["remapped_keys"]["global"].get(layer, {}) and remap_keys["remapped_keys"]["global"][layer][self.key_to_be_replaced]["key"] != key:
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)
            elif self.key_to_be_replaced in remap_keys["remapped_keys"]["global"] and remap_keys["remapped_keys"]["global"][self.key_to_be_replaced]["key"] != key:
                buttons_frame.pack(side='top', fill='x', padx=30, pady=(10,15))
                reset_button.pack(anchor='center', expand=True)

    def update_search_bar(self, remappable_key, text, search_bar):
        current_text = search_bar.get()
        self.select_button(remappable_key, text) 

        if remappable_key not in self.selected_remappable_keys:
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
        program = self.program_dropdown.get()
        focus = self.focus_dropdown.get()
        layer = "layer_" + self.layer_var.get()  # Add "layer_" here
        modifier = self.modifier_dropdown.get()
        
        # Start building the print statement
        replaced_key = self.key_to_be_replaced + " has been replaced with "
        # Get the names of the selected keys
        selected_keys = [button.cget('text') for button in self.selected_remappable_keys]
        # Add the selected keys to the print statement
        replaced_key += " + ".join(selected_keys)
        
        if program:
            replaced_key += f" for {program}"
        if focus:
            replaced_key += f", Requires Focus: {focus}"
        if layer:
            replaced_key += f" on Layer: {layer}"
        
        self.create_notification_frame("Saving...", replaced_key)

        remap_keys = self.get_remap_keys()
        
        # Update the remap_keys
        remapped_key = self.key_to_be_replaced
        
        if program:
            if program not in remap_keys["remapped_keys"]:
                remap_keys["remapped_keys"][program] = {}
            if layer and layer not in remap_keys["remapped_keys"][program]:
                remap_keys["remapped_keys"][program][layer] = {}
            if modifier and modifier not in remap_keys["remapped_keys"][program][layer]:
                remap_keys["remapped_keys"][program][layer][modifier] = {}
            if layer and modifier:
                remap_keys["remapped_keys"][program][layer][modifier][remapped_key] = {"key": " + ".join(selected_keys), "focus_modifier": focus}
            elif layer:
                remap_keys["remapped_keys"][program][layer][remapped_key] = {"key": " + ".join(selected_keys), "focus_modifier": focus}
            else:
                remap_keys["remapped_keys"][program][remapped_key] = {"key": " + ".join(selected_keys), "focus_modifier": focus}
        else:
            if layer and layer not in remap_keys["remapped_keys"]["global"]:
                remap_keys["remapped_keys"]["global"][layer] = {}
            if modifier and modifier not in remap_keys["remapped_keys"]["global"][layer]:
                remap_keys["remapped_keys"]["global"][layer][modifier] = {}
            if layer and modifier:
                remap_keys["remapped_keys"]["global"][layer][modifier][remapped_key] = {"key": " + ".join(selected_keys)}
            elif layer:
                remap_keys["remapped_keys"]["global"][layer][remapped_key] = {"key": " + ".join(selected_keys)}
            else:
                remap_keys["remapped_keys"]["global"][remapped_key] = {"key": " + ".join(selected_keys)}

        with open('Python/data/remap_keys.json', 'w') as file:
            json.dump(remap_keys, file, indent=4)

        self.replace_key_window.destroy()
        self.selected_remappable_keys.clear()

    def reset_replaced_key(self):
        # Get the selected options
        program = self.program_dropdown.get()
        layer = "layer_" + self.layer_var.get()  # Append "layer_" to the layer number

        # Load the existing JSON file
        with open('Python/data/remap_keys.json', 'r') as file:
            remap_keys = json.load(file)

        # Check if the key is in the global section or a program section
        if program and layer and self.key_to_be_replaced in remap_keys["remapped_keys"].get(program, {}).get(layer, {}):
            # Remove the key from the program section
            del remap_keys["remapped_keys"][program][layer][self.key_to_be_replaced]
            # If the layer section is now empty, remove it
            if not remap_keys["remapped_keys"][program][layer]:
                del remap_keys["remapped_keys"][program][layer]
            # If the program section is now empty, remove it
            if not remap_keys["remapped_keys"][program]:
                del remap_keys["remapped_keys"][program]
        elif layer and self.key_to_be_replaced in remap_keys["remapped_keys"]["global"].get(layer, {}):
            # Remove the key from the global section
            del remap_keys["remapped_keys"]["global"][layer][self.key_to_be_replaced]
            # If the layer section is now empty, remove it
            if not remap_keys["remapped_keys"]["global"][layer]:
                del remap_keys["remapped_keys"]["global"][layer]

        # Save the updated remap_keys to the JSON file
        with open('Python/data/remap_keys.json', 'w') as file:
            json.dump(remap_keys, file, indent=4)

        self.create_notification_frame("Resetting...", f"Key: {self.key_to_be_replaced} has been reset to its original value.")
        self.replace_key_window.destroy()
        self.selected_remappable_keys.clear()  # Clear the list of selected buttons

    def create_notification_frame(self, title, body_text):
        self.notification_frame = ctk.CTkFrame(self.home_frame, border_width=1, border_color="white", fg_color=self.notification_frame_colour, bg_color=self.bg_colour)
        self.notification_frame.place(relx=0.99, rely=0.015, anchor='ne')
        
        self.label_frame = ctk.CTkFrame(self.notification_frame, fg_color="transparent")
        self.label_frame.pack(side='top', fill='both', expand=False, padx=(10,30), pady=(10,0))

        title_label = ctk.CTkLabel(self.label_frame, text=title)
        title_label.pack(side='top', anchor="w")

        body_label = ctk.CTkLabel(self.label_frame, text=body_text)
        body_label.pack(side='top', anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.notification_frame, progress_color=self.key_button_colour, determinate_speed=0.4, height=6)
        self.progress_bar.pack(side="bottom", fill="x", pady=(10,2), padx=3)
        self.progress_bar.set(0)
        self.progress_bar.start()

        self.check_progress()

    def check_progress(self):
        value = self.progress_bar.get()

        # If the progress bar is full, destroy the frame
        if value >= 0.96:
            self.notification_frame.destroy()
        else:
            # Otherwise, check again after a short delay
            self.root.after(50, self.check_progress)

    def select_button(self, remappable_key, text):
        if remappable_key in self.selected_remappable_keys:  # If this button is already selected
            self.selected_remappable_keys.remove(remappable_key)  # Deselect it
            remappable_key.configure(fg_color="transparent")
        else:  # If this button is not selected
            self.selected_remappable_keys.append(remappable_key)  # Select it
            remappable_key.configure(fg_color=self.button_selected_colour)
        self.save_button.configure(state='normal' if self.selected_remappable_keys else 'disabled')

    def print_window_size(self):
        print(f"Current window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Main frame size: {self.main_frame.winfo_width()}x{self.main_frame.winfo_height()}")
        print(f"Home frame size: {self.home_frame.winfo_width()}x{self.home_frame.winfo_height()}")
        print(f"Sidebar size: {self.sidebar_frame.winfo_width()}x{self.sidebar_frame.winfo_height()}")

    def draw_frame(self, frame_name):
        try:
            self.selected_frame_indicator.place_forget()
        except AttributeError:
            self.selected_frame_indicator = ctk.CTkLabel(self.sidebar_frame, width=2, height=50, fg_color=self.selected_frame_indicator_colour, text="")

        self.home_frame.pack_forget()
        self.macro_frame.pack_forget()
        self.plugin_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.settings_frame.pack_forget()

        if frame_name == 'home':
            self.selected_frame_indicator.place(x=0, y=50)
            self.home_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'macro':
            self.selected_frame_indicator.place(x=0, y=100)
            self.macro_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'plugin':
            self.selected_frame_indicator.place(x=0, y=150)
            self.plugin_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'profile':
            self.selected_frame_indicator.place(x=0, y=200)
            self.profile_frame.pack(side='top', fill='both', expand=True)   
        elif frame_name == 'settings':
            self.selected_frame_indicator.place(x=0, y=(self.root.winfo_height()-50))
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
        sidebar_frame = ctk.CTkFrame(self.main_frame, width=70, fg_color=self.main_colour)   
        sidebar_frame.pack_propagate(False)
        sidebar_frame.pack(side='left', fill='y')
        self.sidebar_expanded = False
        return sidebar_frame
    
    # yes this is stupid but it will work for now
    def bind_widgets(self, parent, frame_name):
        parent.bind("<Enter>", lambda event, self=self: self.enter_sidebar_button_frame(event, frame_name))
        parent.bind("<Leave>", lambda event, self=self: self.leave_sidebar_button_frame(event, frame_name))
        parent.bind("<Button-1>", lambda event, self=self: self.click_sidebar_button_frame(event, frame_name))
        for child in parent.winfo_children():
            child.bind("<Enter>", lambda event, self=self: self.enter_sidebar_button_frame(event, frame_name))
            child.bind("<Leave>", lambda event, self=self: self.leave_sidebar_button_frame(event, frame_name))
            child.bind("<Button-1>", lambda event, self=self: self.click_sidebar_button_frame(event, frame_name))
            self.bind_widgets(child, frame_name)

    def enter_sidebar_button_frame(self, event, frame_name):
        if frame_name == 'menu':
            self.sidebar_menu_frame.configure(fg_color=self.button_hover_colour)
        elif frame_name == 'home':
            self.sidebar_home_frame.configure(fg_color=self.button_hover_colour)
        elif frame_name == 'macro':
            self.sidebar_macro_frame.configure(fg_color=self.button_hover_colour)
        elif frame_name == 'plugin':
            self.sidebar_plugin_frame.configure(fg_color=self.button_hover_colour)
        elif frame_name == 'profile':
            self.sidebar_profile_frame.configure(fg_color=self.button_hover_colour)
        elif frame_name == 'settings':
            self.sidebar_settings_frame.configure(fg_color=self.button_hover_colour)

    def leave_sidebar_button_frame(self, event, frame_name):
        if frame_name == 'menu':
            self.sidebar_menu_frame.configure(fg_color=self.main_colour)
        elif frame_name == 'home':
            self.sidebar_home_frame.configure(fg_color=self.main_colour)
        elif frame_name == 'macro':
            self.sidebar_macro_frame.configure(fg_color=self.main_colour)
        elif frame_name == 'plugin':
            self.sidebar_plugin_frame.configure(fg_color=self.main_colour)
        elif frame_name == 'profile':
            self.sidebar_profile_frame.configure(fg_color=self.main_colour) 
        elif frame_name == 'settings':
            self.sidebar_settings_frame.configure(fg_color=self.main_colour)
            
    def click_sidebar_button_frame(self, event, frame_name):
        if frame_name == 'menu':
            self.toggle_sidebar()
        elif frame_name == 'home':
            self.draw_frame('home')
        elif frame_name == 'macro':
            self.draw_frame('macro')
        elif frame_name == 'plugin':
            self.draw_frame('plugin')
        elif frame_name == 'profile':
            self.draw_frame('profile')
        elif frame_name == 'settings':
            self.draw_frame('settings')

    def toggle_sidebar(self):
        self.SIDEBAR_WIDTH_COLLAPSED = 70
        self.SIDEBAR_WIDTH_EXPANDED = 200
        
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_COLLAPSED)
            self.sidebar_expanded = False
        else:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_EXPANDED)
            self.sidebar_expanded = True

    def create_sidebar_buttons(self):
        menu_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
        home_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
        macros_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
        save_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
        plugins_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
        windowsize_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_windowsize.png").resize((16,16), Image.Resampling.LANCZOS))
        settings_image = ImageTk.PhotoImage(Image.open("Python/data/icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

        self.sidebar_menu_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_menu_frame.pack(side='top', fill='x')
        self.menu_button = ctk.CTkButton(self.sidebar_menu_frame, image=menu_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.menu_button.pack(side='left')
        self.menu_label = ctk.CTkLabel(self.sidebar_menu_frame, text="Hide")
        self.menu_label.pack(side='left')
        self.bind_widgets(self.sidebar_menu_frame, 'menu')

        self.sidebar_home_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_home_frame.pack(side='top', fill='x')
        self.home_button = ctk.CTkButton(self.sidebar_home_frame, image=home_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.home_button.pack(side='left')
        self.home_label = ctk.CTkLabel(self.sidebar_home_frame, text="Home")
        self.home_label.pack(side='left')
        self.bind_widgets(self.sidebar_home_frame, 'home')

        self.sidebar_macro_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_macro_frame.pack(side='top', fill='x')
        self.macros_button = ctk.CTkButton(self.sidebar_macro_frame, image=macros_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.macros_button.pack(side='left')
        self.macros_label = ctk.CTkLabel(self.sidebar_macro_frame, text="Macros")
        self.macros_label.pack(side='left')
        self.bind_widgets(self.sidebar_macro_frame, 'macro')

        self.sidebar_plugin_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_plugin_frame.pack(side='top', fill='x')
        self.plugin_button = ctk.CTkButton(self.sidebar_plugin_frame, image=plugins_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.plugin_button.pack(side='left')
        self.plugin_label = ctk.CTkLabel(self.sidebar_plugin_frame, text="Plugins")
        self.plugin_label.pack(side='left')
        self.bind_widgets(self.sidebar_plugin_frame, 'plugin')

        self.sidebar_profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_profile_frame.pack(side='top', fill='x')
        self.profile_button = ctk.CTkButton(self.sidebar_profile_frame, image=save_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.profile_button.pack(side='left')
        self.profile_label = ctk.CTkLabel(self.sidebar_profile_frame, text="Profiles")
        self.profile_label.pack(side='left')
        self.bind_widgets(self.sidebar_profile_frame, 'profile')
        
        window_size_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        window_size_frame.pack(side='top', fill='x')
        self.window_size_button = ctk.CTkButton(window_size_frame, image=windowsize_image ,text = "", width=70, height=50, fg_color="transparent", hover_color=self.button_hover_colour, command=self.print_window_size)
        self.window_size_button.pack(side='left')   
        self.window_size_label = ctk.CTkLabel(window_size_frame, text="")
        self.window_size_label.pack(side='left')

        self.sidebar_settings_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", cursor="hand2")
        self.sidebar_settings_frame.pack(side='bottom', fill='x')
        self.settings_button = ctk.CTkButton(self.sidebar_settings_frame, image=settings_image, text = "", width=70, height=50, fg_color="transparent", hover_color=self.main_colour)
        self.settings_button.pack(side='left')
        self.settings_label = ctk.CTkLabel(self.sidebar_settings_frame, text="Settings")
        self.settings_label.pack(side='left')
        self.bind_widgets(self.sidebar_settings_frame, 'settings')
    
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
        self.program_dropdown = ctk.CTkComboBox(program_focus_frame, variable=self.program_var, fg_color=self.bg_colour, border_color=self.dropdown_colour, button_color=self.dropdown_colour, values=["", "Option 1", "Option 2", "Option 3"])
        self.program_dropdown.set("")
        self.program_dropdown.pack(side='left', pady=5)

        # Add a trace to the program_var
        self.program_var.trace('w', self.update_focus_dropdown)

        # Create the focus dropdown and initially hide it
        self.focus_label = ctk.CTkLabel(program_focus_frame, text="Requires Focus:")
        self.focus_label.pack(side='left')
        self.focus_label.pack_forget()
        self.focus_dropdown = ctk.CTkComboBox(program_focus_frame, variable=self.focus_var, fg_color=self.bg_colour, border_color=self.dropdown_colour, button_color=self.dropdown_colour, values=["Yes", "No"])
        self.focus_dropdown.set("")
        self.focus_dropdown.pack(side='left')
        self.focus_dropdown.pack_forget()

        modifier_label = ctk.CTkLabel(modification_frame, text="Modifier Key:")
        modifier_label.pack(side='left', padx=(50, 10))
        self.modifier_dropdown = ctk.CTkComboBox(modification_frame, variable=self.modifier_var, fg_color=self.bg_colour, border_color=self.dropdown_colour, button_color=self.dropdown_colour, values=["", "Option 1", "Option 2", "Option 3"])
        self.modifier_dropdown.set("")
        self.modifier_dropdown.pack(side='left', pady=5)

        layer_label = ctk.CTkLabel(modification_frame, text="Layer:")
        layer_label.pack(side='left', padx=(50, 10))
        layer_segbutton = ctk.CTkSegmentedButton(modification_frame, variable=self.layer_var, selected_color=self.button_selected_colour, selected_hover_color=self.button_hover_colour, unselected_hover_color=self.segmented_button_hover_colour, fg_color=self.dropdown_colour, unselected_color=self.dropdown_colour, values=["0","1", "2", "3"])
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

        keyboard_keys_frame = ctk.CTkFrame(self.home_frame, fg_color=self.keys_frame_colour, border_width=2, border_color="white")
        keyboard_keys_frame.pack(side='top', fill='both', expand=True)

        for keyboard_key in self.keyboard_keys:
            text, x, y, width, height = keyboard_key.values()  # Get the values from the dictionary
            key_button = ctk.CTkButton(keyboard_keys_frame, text=text, width=width, height=height, fg_color=self.key_button_colour, command=lambda text=text: self.draw_replace_key(text))
            key_button._text_label.configure(wraplength=width*0.8)  # Configure word wrap
            if text == "Num Wheel":
                key_button.configure(text=" ", corner_radius=20)
            key_button.place(x=x, y=y)
            original_font_size = int(key_button._text_label.cget("font").split(" ")[1])
            key_button.bind("<Enter>", lambda event, key_button=key_button, x=x, y=y, width=width, height=height, original_font_size=original_font_size: self.shrink_button(key_button, x, y, width, height, original_font_size))
            key_button.bind("<Leave>", lambda event, key_button=key_button, x=x, y=y, width=width, height=height, original_font_size=original_font_size: self.restore_button(key_button, x, y, width, height, original_font_size))
            max_x = max(max_x, x + width)
            max_y = max(max_y, y + height)

        keyboard_keys_frame.configure(width=max_x + 10, height=max_y + 10) #this will go soon
        self.home_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 170) #set as min size in home frame creation
        self.main_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 210) #set as min size in main frame creation
        keyboard_keys_frame.place(relx=0.5, rely=0.5, anchor='center')
        return keyboard_keys_frame

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
        
        settings_theme_frame = ctk.CTkFrame(general_settings_frame, fg_color="transparent", height=45)
        settings_theme_frame.pack(side='top', fill='x', padx=225, pady=(0,5))
        settings_theme_frame.pack_propagate(False)
        settings_theme_label = ctk.CTkLabel(settings_theme_frame, text="Theme")
        settings_theme_label.pack(side='left')
        settings_theme_dropdown = ctk.CTkOptionMenu(settings_theme_frame, fg_color=self.main_colour, button_color=self.dropdown_colour, button_hover_color=self.button_hover_colour, command=lambda theme: [self.set_theme(theme), self.restart_program()])
        settings_theme_dropdown.configure(values=self.available_themes)
        settings_theme_dropdown.set(self.current_theme)
        settings_theme_dropdown.pack(side='right')
        
        settings_layout_frame = ctk.CTkFrame(general_settings_frame, fg_color="transparent", height=45)
        settings_layout_frame.pack(side='top', fill='x', padx=225, pady=(0,5))
        settings_layout_frame.pack_propagate(False)
        settings_layout_label = ctk.CTkLabel(settings_layout_frame, text="Layout")
        settings_layout_label.pack(side='left')
        settings_layout_dropdown = ctk.CTkOptionMenu(settings_layout_frame, fg_color=self.main_colour, button_color=self.dropdown_colour, button_hover_color=self.button_hover_colour, command=lambda layout: [self.set_layout(layout), self.restart_program()])
        settings_layout_dropdown.configure(values=self.available_layouts)
        settings_layout_dropdown.set(self.current_layout)
        settings_layout_dropdown.pack(side='right')
        return general_settings_frame
    
    def restart_program(self):
        #this somehow restarts the window idk how lmao
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()

app = MyApp()
app.run()