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
        #self.debug_settings_frame = self.create_debug_settings_frame()
        self.draw_frame('home')

    def button_event(self, button_name):
        print(f"{button_name} clicked")

        # Create a new window
        replace_key_window = ctk.CTkToplevel(self.root)
        #replace_key_window.resizable(False, False) #makes the toplevel window flicker before opening?
        replace_key_window.geometry('400x450')
        replace_key_window.title(f"Replace Key: {button_name}")
        replace_key_window.attributes('-topmost', True)

        # Create a frame for the search bar
        search_frame = ctk.CTkFrame(replace_key_window)
        search_frame.pack(side='top', fill='x', padx=40, pady=(40,20))

        # Create the search bar
        search_bar = ctk.CTkEntry(search_frame)
        search_bar.configure(placeholder_text="Search...", height=40)
        search_bar.pack(fill='x')

        # Create a scrollable frame for the keys
        keys_frame = ctk.CTkScrollableFrame(replace_key_window, fg_color="transparent")
        keys_frame.pack(side='top', fill='both', expand=True, padx=40, pady=(0,20))
        keys = self.get_keys()
        
        # Populate the keys frame with buttons
        for key in keys:
            text, x, y, width, height, layouts = key
            key_button = ctk.CTkButton(keys_frame, text=text, height=45, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda text=text: print(f"{text} clicked"))
            key_button.pack(side='top', fill='x', padx=0, pady=5)

        # Create a frame for the buttons
        buttons_frame = ctk.CTkFrame(replace_key_window, fg_color="transparent")
        buttons_frame.pack(side='top', fill='x', pady=(0,5))

        # Create the 'Save' button
        save_button = ctk.CTkButton(buttons_frame, text='Save')
        save_button.pack(side='left', padx=5, pady=5)

        # Create the 'Cancel' button
        cancel_button = ctk.CTkButton(buttons_frame, text='Cancel', command=replace_key_window.destroy)
        cancel_button.pack(side='right', padx=5, pady=5)

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
        version_label = ctk.CTkLabel(version_frame, text="v0.0.1", padx = (15), anchor='e')
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
        modification_frame.pack(side='top', expand=False)  # Pack to the left of the parent_frame

        program_label = ctk.CTkLabel(modification_frame, text="Program Name:")
        program_label.pack(side='left', padx=(0, 10))  # Reduce padding to 10 pixels
        program_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
        program_dropdown.set("")
        program_dropdown.pack(side='left', pady=5)  # Add 50 pixels of padding to the left

        modifier_label = ctk.CTkLabel(modification_frame, text="Modifier Key:")
        modifier_label.pack(side='left', padx=(50, 10))  # Reduce padding to 10 pixels
        modifier_dropdown = ctk.CTkComboBox(modification_frame, values=["Option 1", "Option 2", "Option 3"])
        modifier_dropdown.set("")
        modifier_dropdown.pack(side='left', pady=5)  # Add 50 pixels of padding to the right

        layer_label = ctk.CTkLabel(modification_frame, text="Layer:")
        layer_label.pack(side='left', padx=(50, 10))  # Reduce padding to 10 pixels
        layer_segbutton = ctk.CTkSegmentedButton(modification_frame, values=["0","1", "2", "3"])
        layer_segbutton.set("0")
        layer_segbutton.pack(side='left', pady=5) 
        return modification_frame

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
                button = ctk.CTkButton(keys_frame, text=text, width=width, height=height, command=lambda text=text: self.button_event(text))
                button._text_label.configure(wraplength=width*0.8)  # Configure word wrap
                button.place(x=x, y=y)
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
    
    #def create_debug_settings_frame(self):
        debug_settings_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        debug_settings_frame.pack(side='top', fill='both', expand=True)
        debug_settings_label = ctk.CTkLabel(debug_settings_frame, text="DEBUG", font=('Bold', 22))
        debug_settings_label.pack(side='top', pady=(10,30))
        return debug_settings_frame
    
    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()

app = MyApp()
app.run()