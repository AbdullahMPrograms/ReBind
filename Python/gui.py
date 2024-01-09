import customtkinter as ctk
from PIL import Image, ImageTk
import ast

class MyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ReBind")
        self.root.minsize(1250, 570) #Tenkeyless size, works well with 60%
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
        self.version_frame = self.create_version_frame()
        self.create_sidebar_buttons()
        self.general_settings_frame = self.create_general_settings_frame()
        self.draw_frame('home')

    def draw_replace_key(self, button_name):
        print(f"{button_name} clicked")
        self.replace_key_window = ctk.CTkToplevel(self.root)
        self.replace_key_window.geometry('400x460')
        self.replace_key_window.title(f"Replace Key: {button_name}")
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

        self.current_button = None
        self.key_buttons = []

        for key in keys:
            text, x, y, width, height, layouts = key
            key_button = ctk.CTkButton(keys_frame, text=text, height=45, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            key_button.configure(command=lambda key_button=key_button, text=text: self.highlight_button(key_button, text))
            key_button.pack(side='top', fill='x', padx=0, pady=5)
            self.key_buttons.append(key_button)

        def update_buttons(*args):
            search_term = search_var.get().lower()
            for key_button in self.key_buttons:
                key_text = key_button.cget("text").lower()
                if search_term in key_text:
                    if search_term == key_text:
                        # If it's an exact match, pack it at the top
                        key_button.pack(side='top', fill='x', padx=0, pady=5)
                    else:
                        # If it's not an exact match, pack it at the bottom
                        key_button.pack(side='bottom', fill='x', padx=0, pady=5)
                else:
                    key_button.pack_forget()
        
        search_var.trace("w", update_buttons)

        buttons_frame = ctk.CTkFrame(self.replace_key_window, fg_color="transparent")
        buttons_frame.pack(side='top', fill='x', padx=80, pady=(10,15))
        self.save_button = ctk.CTkButton(buttons_frame, width=100, height=35, border_width=2, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text="Save")
        self.save_button.configure(state='disabled')
        self.save_button.pack(side='left')
        cancel_button = ctk.CTkButton(buttons_frame,width=100, height=35, border_width=2, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text="Cancel", command=self.replace_key_window.destroy)
        cancel_button.pack(side='right')
        
    def highlight_button(self, key_button, text):
        print(f"{text} clicked")
        if self.current_button:         # Unhighlight the currently highlighted button
            self.current_button.configure(fg_color="transparent")
        key_button.configure(fg_color='#1f6aa5')          # Highlight the new button
        self.current_button = key_button
        self.save_button.configure(state='normal', command=self.save_replaced_key)
    
    def save_replaced_key(self):
        print("Save button clicked")
        self.replace_key_window.destroy()

    def print_window_size(self):
        print(f"Current window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Main frame size: {self.main_frame.winfo_width()}x{self.main_frame.winfo_height()}")
        print(f"Home frame size: {self.home_frame.winfo_width()}x{self.home_frame.winfo_height()}")
        print(f"Sidebar size: {self.sidebar_frame.winfo_width()}x{self.sidebar_frame.winfo_height()}")
        
    def get_keys(self):
        with open('Python/Layouts/Keys.ini', 'r') as file:
            keys = ast.literal_eval(file.read())
        return keys

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
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(side='left', fill='both', expand=True)
        return main_frame
        
    def create_version_frame(self):
        version_frame = ctk.CTkFrame(self.main_frame, height=20, fg_color="transparent")
        version_frame.pack(side='bottom', fill='x')
        version_label = ctk.CTkLabel(version_frame, text="v0.0.1", padx=15, anchor='e')
        version_label.pack(side='right')
        return version_frame
    
    def create_sidebar_frame(self):
        sidebar_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")   
        sidebar_frame.pack_propagate(False)  # Don't allow the widgets inside to dictate the frame's width
        sidebar_frame.pack(side='left', fill='y')
        return sidebar_frame

    def create_sidebar_buttons(self):
        menu_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
        home_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
        macros_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
        save_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
        plugins_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
        windowsize_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_windowsize.png").resize((18,18), Image.Resampling.LANCZOS))
        settings_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

        menu_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        menu_frame.pack(side='top', fill='x')
        self.menu_button = ctk.CTkButton(menu_frame, image=menu_image, text = "", width=70, height=50, fg_color = "transparent", command=self.toggle_sidebar)
        self.menu_button.pack(side='left')
        self.menu_label = ctk.CTkLabel(menu_frame, text="", fg_color="transparent")
        self.menu_label.pack(side='left')

        home_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        home_frame.pack(side='top', fill='x')
        self.home_button = ctk.CTkButton(home_frame, image=home_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.draw_frame('home'))
        self.home_button.pack(side='left')
        self.home_label = ctk.CTkLabel(home_frame, text="", fg_color="transparent")
        self.home_label.pack(side='left')

        macros_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        macros_frame.pack(side='top', fill='x')
        self.macros_button = ctk.CTkButton(macros_frame, image=macros_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.draw_frame('macro'))
        self.macros_button.pack(side='left')
        self.macros_label = ctk.CTkLabel(macros_frame, text="", fg_color="transparent")
        self.macros_label.pack(side='left')

        plugin_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        plugin_frame.pack(side='top', fill='x')
        self.plugin_button = ctk.CTkButton(plugin_frame, image=plugins_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.draw_frame('plugin'))
        self.plugin_button.pack(side='left')
        self.plugin_label = ctk.CTkLabel(plugin_frame, text="", fg_color="transparent")
        self.plugin_label.pack(side='left')

        profile_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        profile_frame.pack(side='top', fill='x')
        self.profile_button = ctk.CTkButton(profile_frame, image=save_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.draw_frame('profile'))
        self.profile_button.pack(side='left')
        self.profile_label = ctk.CTkLabel(profile_frame, text="", fg_color="transparent")
        self.profile_label.pack(side='left')
        
        window_size_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        window_size_frame.pack(side='top', fill='x')
        self.window_size_button = ctk.CTkButton(window_size_frame, image=windowsize_image ,text = "", width=70, height=50, fg_color = "transparent", command=self.print_window_size)
        self.window_size_button.pack(side='left')   
        self.window_size_label = ctk.CTkLabel(window_size_frame, text="", fg_color="transparent")
        self.window_size_label.pack(side='left')

        settings_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        settings_frame.pack(side='bottom', fill='x')
        self.settings_button = ctk.CTkButton(settings_frame, image=settings_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.draw_frame('settings'))
        self.settings_button.pack(side='left')
        self.settings_label = ctk.CTkLabel(settings_frame, text="", bg_color="transparent")
        self.settings_label.pack(side='left')
    
    def create_home_frame(self):
        home_frame = ctk.CTkFrame(self.main_frame)
        home_frame.pack(side='top', fill='both', expand=True)
        return home_frame
    
    def create_modification_frame(self):
        modification_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        modification_frame.pack(side='top', expand=False)

        program_label = ctk.CTkLabel(modification_frame, text="Program Name:")
        program_label.pack(side='left', padx=(0, 10))
        program_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
        program_dropdown.set("")
        program_dropdown.pack(side='left', pady=5)

        modifier_label = ctk.CTkLabel(modification_frame, text="Modifier Key:")
        modifier_label.pack(side='left', padx=(50, 10))
        modifier_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
        modifier_dropdown.set("")
        modifier_dropdown.pack(side='left', pady=5)

        layer_label = ctk.CTkLabel(modification_frame, text="Layer:")
        layer_label.pack(side='left', padx=(50, 10))
        layer_segbutton = ctk.CTkSegmentedButton(modification_frame, values=["0","1", "2", "3"])
        layer_segbutton.set("0")
        layer_segbutton.pack(side='left', pady=5) 
        return modification_frame

    def shrink_button(self, button, original_x, original_y, original_width, original_height, original_font_size):
        shrink_factor_button = 0.93  # Adjust this value as needed
        shrink_factor_font = 0.95  # Adjust this value as needed
        button.configure(width=original_width*shrink_factor_button, height=original_height*shrink_factor_button, fg_color="#144870")
        button.place_configure(x=original_x+(original_width*(1-shrink_factor_button)/2), y=original_y+(original_height*(1-shrink_factor_button)/2))
        new_font_size = int(original_font_size*shrink_factor_font) # Adjust this value as needed
        button._text_label.configure(font=("Roboto", new_font_size))

    def restore_button(self, button, original_x, original_y, original_width, original_height, original_font_size):
        button.configure(width=original_width, height=original_height, fg_color="#1f6aa5")
        button.place_configure(x=original_x, y=original_y)
        button._text_label.configure(font=("Roboto", original_font_size))

    def create_keys_frame(self):
        max_x = 0
        max_y = 0

        isSixty = False
        isTenKeyless = True
        isFullSized = False

        if isSixty:
            current_layout = "sixty"
        elif isTenKeyless:
            current_layout = "tenkeyless"
        elif isFullSized:
            current_layout = "full"
        else:
            current_layout = None

        keys_frame = ctk.CTkFrame(self.home_frame, bg_color="transparent")
        keys_frame.pack(side='top', fill='both', expand=True)

        keys = self.get_keys()

        for key in keys:
            text, x, y, width, height, layouts = key
            if current_layout in layouts:
                if current_layout == 'sixty':
                    y -= 60
                button = ctk.CTkButton(keys_frame, text=text, width=width, height=height, command=lambda text=text: self.draw_replace_key(text))
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
        macro_frame = ctk.CTkFrame(self.main_frame)
        macro_frame.pack(side='top', fill='both', expand=True)
        macro_label = ctk.CTkLabel(macro_frame, text="MACROS PAGE")
        macro_label.pack(side='top')
        return macro_frame
    
    def create_plugin_frame(self):
        plugin_frame = ctk.CTkFrame(self.main_frame)
        plugin_frame.pack(side='top', fill='both', expand=True)
        plugin_label = ctk.CTkLabel(plugin_frame, text="PLUGIN PAGE")
        plugin_label.pack(side='top')
        return plugin_frame
    
    def create_profile_frame(self):
        profile_frame = ctk.CTkFrame(self.main_frame)
        profile_frame.pack(side='top', fill='both', expand=True)
        profile_label = ctk.CTkLabel(profile_frame, text="PROFILE/SAVE PAGE")
        profile_label.pack(side='top')
        return profile_frame
    
    def create_settings_frame(self):
        settings_frame = ctk.CTkFrame(self.main_frame)
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