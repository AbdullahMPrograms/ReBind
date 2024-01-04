import customtkinter as ctk
from PIL import Image, ImageTk
import ast

class MyApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ReBind")
        self.sidebar_expanded = False
        self.main_frame = self.create_main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.home_frame = self.create_home_frame()
        self.modification_frame = self.create_modification_frame()
        self.keys_frame = self.create_keys_frame()
        self.settings_frame = self.create_settings_frame()
        self.version_frame = self.create_version_frame()
        self.create_sidebar_buttons()
        self.switch_frame('home')

    def button_event(self, button_name):
        print(f"{button_name} clicked")

    def print_window_size(self):
        print(f"Current window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Main frame size: {self.main_frame.winfo_width()}x{self.main_frame.winfo_height()}")
        print(f"Home frame size: {self.home_frame.winfo_width()}x{self.home_frame.winfo_height()}")
        print(f"Home frame width: {self.home_frame['width']}")
        print(f"Keys frame size: {self.keys_frame.winfo_width()}x{self.keys_frame.winfo_height()}")
        print(f"Sidebar size: {self.sidebar_frame.winfo_width()}x{self.sidebar_frame.winfo_height()}")
        print(f"Version frame placement: x={self.version_frame.winfo_x()}, y={self.version_frame.winfo_y()}")
        print(f"modification frame placement: x={self.modification_frame.winfo_width()}")

    def switch_frame(self, frame_name):
        self.home_frame.pack_forget()
        self.settings_frame.pack_forget()

        if frame_name == 'home':
            self.home_frame.pack(side='top', fill='both', expand=True)
        elif frame_name == 'settings':
            self.settings_frame.pack(side='top', fill='both', expand=True)

    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(side='left', fill='both', expand=True)
        return main_frame
        
    def create_sidebar_frame(self):
        sidebar_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        sidebar_frame.pack_propagate(0)  # Don't allow the widgets inside to dictate the frame's width
        sidebar_frame.pack(side='left', fill='y')
        return sidebar_frame
    
    def create_home_frame(self):
        home_frame = ctk.CTkFrame(self.main_frame)
        home_frame.pack(side='top', fill='both', expand=True)
        return home_frame
    
    def create_settings_frame(self):
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(side='top', fill='both', expand=True)
        program_label = ctk.CTkLabel(settings_frame, text="SETTINGS PAGE")
        program_label.pack(side='top')  # Reduce padding to 10 pixels
        return settings_frame
    
    def toggle_sidebar(self):
        self.SIDEBAR_WIDTH_COLLAPSED = 70
        self.SIDEBAR_WIDTH_EXPANDED = 200
        
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_COLLAPSED)
            self.menu_label.configure(text="", width=0)
            self.home_label.configure(text="", width=0)
            self.macros_label.configure(text="", width=0)
            self.plugin_label.configure(text="", width=0)
            self.save_label.configure(text="", width=0)
            self.settings_label.configure(text="", width=0)
            self.sidebar_expanded = False
        else:
            self.sidebar_frame.configure(width=self.SIDEBAR_WIDTH_EXPANDED)
            self.menu_label.configure(text="Hide")
            self.home_label.configure(text="Home")
            self.macros_label.configure(text="Macros")
            self.plugin_label.configure(text="Plugins")
            self.save_label.configure(text="Profiles")
            self.settings_label.configure(text="Settings")  
            self.sidebar_expanded = True

    def create_modification_frame(self):
        modification_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        modification_frame.pack(side='top', expand=False)  # Pack to the left of the parent_frame

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

        with open('Python/Layouts/Keys.ini', 'r') as file:
            keys = ast.literal_eval(file.read())

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
        self.home_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 170)
        self.main_frame.configure(width=self.sidebar_frame['width'] + self.home_frame['width'], height=max_y + 210)
        self.sidebar_frame.configure(width=70, height=self.main_frame['height'])
        self.root.geometry(f"{max_x + self.sidebar_frame['width'] + 100}x{self.sidebar_frame['height']}")
        keys_frame.place(relx=0.5, rely=0.5, anchor='center')
        return keys_frame

    def create_version_frame(self):
        version_frame = ctk.CTkFrame(self.main_frame, height=20, fg_color="transparent")
        version_frame.pack(side='bottom', fill='x')
        version_label = ctk.CTkLabel(version_frame, text="v0.0.1", padx = (15), anchor='e')
        version_label.pack(side='right')
        return version_frame

    def create_sidebar_buttons(self):
        menu_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_menu.png").resize((18,18), Image.Resampling.LANCZOS))
        home_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_home.png").resize((16,16), Image.Resampling.LANCZOS))
        macros_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_macros.png").resize((16,16), Image.Resampling.LANCZOS))
        save_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_save.png").resize((16,16), Image.Resampling.LANCZOS))
        plugins_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_plugins.png").resize((16,16), Image.Resampling.LANCZOS))
        settings_image = ImageTk.PhotoImage(Image.open("Python/Images/Icons/icon_settings.png").resize((18,18), Image.Resampling.LANCZOS))

        menu_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        menu_frame.pack(side='top', fill='x')
        self.menu_button = ctk.CTkButton(menu_frame, image=menu_image, text = "", width=70, height=50, fg_color = "transparent", command=self.toggle_sidebar)
        self.menu_button.pack(side='left')
        self.menu_label = ctk.CTkLabel(menu_frame, text="", fg_color="transparent")
        self.menu_label.pack(side='left')

        home_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        home_frame.pack(side='top', fill='x')
        self.home_button = ctk.CTkButton(home_frame, image=home_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.switch_frame('home'))
        self.home_button.pack(side='left')
        self.home_label = ctk.CTkLabel(home_frame, text="", fg_color="transparent")
        self.home_label.pack(side='left')

        macros_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        macros_frame.pack(side='top', fill='x')
        self.macros_button = ctk.CTkButton(macros_frame, image=macros_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.button_event('Macros'))
        self.macros_button.pack(side='left')
        self.macros_label = ctk.CTkLabel(macros_frame, text="", fg_color="transparent")
        self.macros_label.pack(side='left')

        plugin_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        plugin_frame.pack(side='top', fill='x')
        self.plugin_button = ctk.CTkButton(plugin_frame, image=plugins_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.button_event('Plugins'))
        self.plugin_button.pack(side='left')
        self.plugin_label = ctk.CTkLabel(plugin_frame, text="", fg_color="transparent")
        self.plugin_label.pack(side='left')

        save_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        save_frame.pack(side='top', fill='x')
        self.save_button = ctk.CTkButton(save_frame, image=save_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.button_event('Profiles'))
        self.save_button.pack(side='left')
        self.save_label = ctk.CTkLabel(save_frame, text="", fg_color="transparent")
        self.save_label.pack(side='left')

        settings_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        settings_frame.pack(side='bottom', fill='x')
        self.settings_button = ctk.CTkButton(settings_frame, image=settings_image, text = "", width=70, height=50, fg_color = "transparent", command=lambda: self.switch_frame('settings'))
        self.settings_button.pack(side='left')
        self.settings_label = ctk.CTkLabel(settings_frame, text="1", bg_color="transparent")
        self.settings_label.pack(side='left')

    def run(self):
        self.root.resizable(False, False)
        self.root.mainloop()

app = MyApp()
app.run()