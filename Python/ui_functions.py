# UI FUNCTIONS FOR GUI WILL ALL BE PLACED HERE
import customtkinter as ctk
import ast
import os
import configparser


class UI_Functions:
    def __init__(self):
        self.themes = self.get_available_themes()
        self.set_theme(self.themes[0])  # Set the first available theme
        self.sidebar_expanded = False
        self.current_buttons = []
        self.draw_frame('home')

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

        keys = self.get_keys()

        search_var = ctk.StringVar()
        search_bar = ctk.CTkEntry(search_frame, textvariable=search_var, height=35)
        search_bar.pack(fill='x')

        keys_frame = ctk.CTkScrollableFrame(self.replace_key_window, fg_color="transparent")
        keys_frame.pack(side='top', fill='both', expand=True, padx=40, pady=20)

        self.current_buttons = []
        self.key_buttons = []

        for key in keys:
            text, x, y, width, height, layouts = key
            key_button = ctk.CTkButton(keys_frame, text=text, height=45, fg_color="transparent", hover_color=self.button_hover_colour, border_width=2, text_color=("gray10", "#DCE4EE"))
            key_button.configure(command=lambda key_button=key_button, text=text: self.update_search_bar(key_button, text, search_bar))
            key_button.pack(side='top', fill='x', padx=0, pady=5)
            self.key_buttons.append(key_button)

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

        buttons_frame = ctk.CTkFrame(self.replace_key_window, fg_color="transparent")
        buttons_frame.pack(side='top', fill='x', padx=80, pady=(10,15))
        self.save_button = ctk.CTkButton(buttons_frame, width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Save", command=self.save_replaced_key)
        self.save_button.configure(state='disabled')
        self.save_button.pack(side='left')
        cancel_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", hover_color=self.button_hover_colour, text_color=("gray10", "#DCE4EE"), text="Cancel", command=self.replace_key_window.destroy)
        cancel_button.pack(side='right')

    def update_search_bar(self, key_button, text, search_bar):
        current_text = search_bar.get()
        if key_button in self.current_buttons:  # If this button is already selected
            self.current_buttons.remove(key_button)  # Deselect it
            key_button.configure(fg_color="transparent")
            # Remove the text of the button from the search bar
            parts = current_text.split(' + ')
            parts.remove(text)
            new_text = ' + '.join(parts)
        else:  # If this button is not selected
            self.current_buttons.append(key_button)  # Select it
            key_button.configure(fg_color=self.button_selected_colour)
            # Replace the current text in the search bar with the button text
            if '+' in current_text:
                base_text, _ = current_text.rsplit('+', 1)
                new_text = base_text + '+ ' + text
            else:
                new_text = text

        # Update the search bar
        search_bar.delete(0, 'end')
        search_bar.insert(0, new_text.strip())

        self.save_button.configure(state='normal' if self.current_buttons else 'disabled')

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
        self.replace_key_window.destroy()
        self.current_buttons.clear()  # Clear the list of selected buttons
        
    def highlight_button(self, key_button, text):
        print(f"{text} clicked")
        if key_button in self.current_buttons:  # If this button is already selected
            self.current_buttons.remove(key_button)  # Deselect it
            key_button.configure(fg_color="transparent")
        else:  # If this button is not selected
            self.current_buttons.append(key_button)  # Select it
            key_button.configure(fg_color=self.button_selected_colour)
        self.save_button.configure(state='normal' if self.current_buttons else 'disabled')
        
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

    def get_available_themes(self):
        themes = []
        theme_files = os.listdir("Python/Themes")
        for file in theme_files:
            if file.endswith('.ini'):
                themes.append(file[:-4])  # Remove the .ini extension
        print('Detected themes:', themes)
        return themes

    def print_window_size(self):
        print(f"Current window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Main frame size: {self.main_frame.winfo_width()}x{self.main_frame.winfo_height()}")
        print(f"Home frame size: {self.home_frame.winfo_width()}x{self.home_frame.winfo_height()}")
        print(f"Sidebar size: {self.sidebar_frame.winfo_width()}x{self.sidebar_frame.winfo_height()}")

    def get_keys(self):
        with open('Python/Layouts/Keys.ini', 'r') as file:
            keys = ast.literal_eval(file.read())
        return keys