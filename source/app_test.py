import platform
import queue
import customtkinter # type: ignore
from configparser import ConfigParser
from source.functions import logprint, get_time, open_url

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = ConfigParser()
        self.config.read("config/settings.ini")

        self.queue = queue.Queue()
        self.bot_running = False

        customtkinter.set_appearance_mode(self.config.get("gui_config", "appearance_mode"))
        customtkinter.set_default_color_theme(self.config.get("gui_config", "default_color_theme"))
        
        temp_button = customtkinter.CTkButton(self, text="TEMP")
        self.initial_color = temp_button.cget("fg_color")
        temp_button.destroy()

        system = platform.system()
        icon_app = self.config.get("gui_config", "icon_app")
        if system == "Linux":
            self.iconbitmap("@" + icon_app + ".xbm")
        else:
            self.iconbitmap(icon_app + ".ico")

        self.title(self.config.get("gui_config", "title") + " v" + self.config.get("gui_config", "version"))
        self.resizable(False, False)
        self.corner_radius = int(self.config.get("gui_config", "corner_radius"))
        self.width_frame = int(self.config.get("gui_config", "width_frame"))
        self.height_frame = int(self.config.get("gui_config", "height_frame"))
        self.width_tb = int(self.config.get("gui_config", "width_tb"))
        self.main_font = customtkinter.CTkFont(family="Calibrí", size=13, weight="normal")
        self.bold_font = customtkinter.CTkFont(family="Calibrí", size=13, weight="bold")
        self.small_font = customtkinter.CTkFont(family="Calibrí", size=8)






        # ----------------------- FRAMES -----------------------
        # logs
        self.frame_logs = customtkinter.CTkFrame(self, corner_radius=self.corner_radius, width=self.width_frame * 3, height=self.height_frame)
        self.frame_logs.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        # sidebar
        self.frame_sidebar = customtkinter.CTkFrame(self, corner_radius=self.corner_radius, width=self.width_frame, height=self.height_frame)
        self.frame_sidebar.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        # Configurar columnas para frame_logs y frame_sidebar
        self.frame_logs.grid_columnconfigure(0, weight=1)  # Columna 0
        self.frame_logs.grid_columnconfigure(1, weight=1)  # Columna 1
        self.frame_logs.grid_columnconfigure(2, weight=1)  # Columna 2
        
        self.frame_sidebar.grid_columnconfigure(0, weight=1)  # Columna 0
        self.frame_sidebar.grid_columnconfigure(1, weight=1)  # Columna 1
        self.frame_sidebar.grid_columnconfigure(2, weight=1)  # Columna 2
        
        # ----------------------- WIDGETS -----------------------
        # Colores en frame_logs
        self.label_red = customtkinter.CTkLabel(self.frame_logs, text="", fg_color="red", width=self.width_frame)
        self.label_red.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        
        self.label_green = customtkinter.CTkLabel(self.frame_logs, text="", fg_color="green", width=self.width_frame)
        self.label_green.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
        
        self.label_blue = customtkinter.CTkLabel(self.frame_logs, text="", fg_color="blue", width=self.width_frame)
        self.label_blue.grid(row=0, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")
        
        # Colores en frame_sidebar
        self.label_red_sidebar = customtkinter.CTkLabel(self.frame_sidebar, text="", fg_color="red", width=self.width_frame)
        self.label_red_sidebar.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        
        # Asegurar que el widget verde abarque correctamente las columnas 1 y 2
        self.label_green_sidebar = customtkinter.CTkLabel(self.frame_sidebar, text="", fg_color="green", width=self.width_frame * 2)
        self.label_green_sidebar.grid(row=1, column=1, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="nsew")


       









        # events
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update()

        # center gui
        self.minsize(self.winfo_width(), self.winfo_height())
        x_cordinate = int((self.winfo_screenwidth() / 2) - (self.winfo_width() / 2))
        y_cordinate = int((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))
        self.geometry("{}+{}".format(x_cordinate, y_cordinate - 20))

        # loop to refresh gui
        logprint(self.queue, self.config.get("strings", "gui_loaded"))
        self.gui_update()

    # ----------------------- FUNCTIONS -----------------------

    def gui_update(self):
        try:
            self.check_queue()
        except:
            logprint(self.queue, self.config.get("strings", "error_checking_queue"))
            
        try:
            self.config.read("config/settings.ini")
            
        except:
            logprint(self.queue, self.config.get("strings", "error_gui_update"))
        
        with open("config/settings.ini", "w") as configfile:
                self.config.write(configfile)
            
        self.after(int(self.config.get("gui_config", "gui_update_time"))*1000, self.gui_update)

    def toggle_run(self):
        if self.bot_running:
            self.bot_running = False
            self.btn_run.configure(text="START BOT", fg_color=self.initial_color)
        else:
            self.bot_running = True
            self.btn_run.configure(text="RUNNING", fg_color="green")

        print("Bot Running:", self.bot_running)

    def on_enter(self, event):
        if self.bot_running:
            self.btn_run.configure(text="STOP", fg_color="red")

    def on_leave(self, event):
        if self.bot_running:
            self.btn_run.configure(text="RUNNING", fg_color="green")
        else:
            self.btn_run.configure(text="START BOT", fg_color=self.initial_color)

    def on_close(self):
        logprint(self.queue, self.config.get("strings", "on_close"))
        print("[-] Closing application...")

        if self.bot_running:
            self.thread.stop()

        self.destroy()
    
    def change_theme(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        logprint(self.queue, self.config.get("strings", "change_theme") + " " + new_appearance_mode)