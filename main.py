from tkinter import filedialog, messagebox
import win32api
import win32con
import os
import json
import sys
import webbrowser
import customtkinter as ctk
import requests
from tkinter import messagebox
import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TrueStretched Valorant")
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        icon_path = os.path.join(os.path.dirname(__file__), "icon2.ico")
        root.iconbitmap(icon_path)

        self.root.configure(bg="#0e0e0e")

        self.selected_file = None
        self.selected_resolution = (1440, 1080)
        self.prog_version = "3.3"
        self.config_dir = self.get_config_directory()
        self.create_widgets()
        self.load_settings()
        self.check_for_updates()

    def check_for_updates(self):
        try:
            response = requests.get("https://api.github.com/repos/FRZNba/truestretched_valorant/releases/latest")
            response.raise_for_status()  
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            release_url = latest_release['html_url']

            if self.prog_version != latest_version:
                self.show_update_notification(release_url)
        except requests.RequestException as e:
            print(f"Erreur lors de la vérification des mises à jour : {e}")

    def show_update_notification(self, release_url):
        update_window = tk.Toplevel(self.root)
        update_window.title("Mise à jour disponible")
        update_window.geometry("300x150")
        update_window.configure(bg="#0e0e0e")

     
        update_window.overrideredirect(True)  
        

        x = self.root.winfo_screenwidth() - 1200
        y = self.root.winfo_screenheight() - 540
        update_window.geometry(f"300x125+{x}+{y}")

        message = "Mise à jour de TrueStretched Disponible : "
        label = tk.Label(update_window, text=message, bg="#0e0e0e", fg="white", font=("Arial", 12))
        label.pack(pady=10)



        link = ctk.CTkLabel(update_window, text="Cliquez ici pour voir les détails", text_color="#0055ca", cursor="hand2", bg_color="#0e0e0e")
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open(release_url))

        close_button = ctk.CTkButton(update_window, text="Fermer", command=update_window.destroy, fg_color="white", text_color="black", width=70, hover_color="#808080")
        close_button.pack( padx=5)
        close_button.pack(pady=10)


    def get_config_directory(self):
        if getattr(sys, 'frozen', False):  
            application_path = os.path.dirname(sys.executable)
        else: 
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        config_dir = os.path.join(application_path, "config")
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        return config_dir

    def get_settings_file_path(self):
        return os.path.join(self.config_dir, "last.json")

    def create_widgets(self):
        self.frames = {}
        self.create_page("res")
        self.create_page("help")

        self.show_page("res")


        version_label = ctk.CTkLabel(
            self.root,
            text=f" v{self.prog_version} ",
            text_color="white",
            bg_color=self.root.cget('bg'),
            fg_color=self.root.cget('bg')
        )
        version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def create_page(self, page_name):
        frame = ctk.CTkFrame(self.root, fg_color="#0e0e0e")
        frame.pack(fill="both", expand=True)

        if page_name == "res":
            top_frame = ctk.CTkFrame(frame, fg_color="#0e0e0e")
            top_frame.pack(side=ctk.TOP, anchor="w", pady=5)

            help_button = ctk.CTkButton(top_frame, text="Aide", command=lambda: self.show_page("help"), fg_color="white", text_color="black", width=50, hover_color="#808080")
            help_button.pack(side=ctk.LEFT, padx=5)

            self.file_label = ctk.CTkLabel(frame, text="Aucun fichier sélectionné", text_color="white", wraplength=250)
            self.file_label.pack(pady=10)

            choose_button = ctk.CTkButton(frame, text="Choisir le fichier", command=self.choose_file, fg_color="white", text_color="black", hover_color="#808080")
            choose_button.pack(pady=5)

            custom_resolution_label = ctk.CTkLabel(frame, text="Résolution personnalisée", text_color="white")
            custom_resolution_label.pack(pady=10)

            input_frame = ctk.CTkFrame(frame, fg_color="#0e0e0e")
            input_frame.pack(pady=5)

            self.width_entry = ctk.CTkEntry(input_frame, width=50, fg_color="white", text_color="black", border_width=0)
            self.width_entry.pack(side=ctk.LEFT, padx=5)

            self.height_entry = ctk.CTkEntry(input_frame, width=50, fg_color="white", text_color="black", border_width=0)
            self.height_entry.pack(side=ctk.LEFT, padx=5)

            custom_resolution_button = ctk.CTkButton(frame, text="Appliquer", command=self.apply_custom_resolution, fg_color="white", text_color="black", hover_color="#808080")
            custom_resolution_button.pack(pady=5)

            self.frames["res"] = frame

        elif page_name == "help":
            help_text = ctk.StringVar(value="Choisis le dossier de ton compte puis entre dans le dossier windows et sélectionne le fichier GameUserSettings.ini. Le programme se charge de changer ta résolution d'écran, il ne te reste plus qu'à lancer Valorant. Attention, il se peut que si ta résolution est trop différente le taux de rafraîchissement de ton écran change donc pense bien à le remettre au maximum si tu constates une différence.")

            help_label = ctk.CTkLabel(frame, textvariable=help_text, wraplength=250, text_color="white")
            help_label.pack(pady=20, padx=10)

            link_label = ctk.CTkLabel(frame, text="Autre Problème ?", text_color="#0055ca", cursor="hand2")
            link_label.pack(pady=5)
            link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/FRZNba/truestretched_valorant"))

            back_button = ctk.CTkButton(frame, text="Retour", command=lambda: self.show_page("res"), fg_color="white", text_color="black", hover_color="#808080")
            back_button.pack(pady=5)

            self.frames["help"] = frame
            self.help_text = help_text

    def show_page(self, page_name):
        for frame_name, frame in self.frames.items():
            if frame_name == page_name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def choose_file(self):
        user_profile_path = os.path.expanduser("~")
        valorant_config_path = os.path.join(user_profile_path, "AppData", "Local", "VALORANT", "Saved", "Config")

        file_path = filedialog.askopenfilename(
            initialdir=valorant_config_path,
            title="Select GameUserSettings.ini",
            filetypes=(("INI files", "*.ini"), ("All files", "*.*"))
        )

        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=f"Fichier sélectionné : {file_path}")
            self.save_settings()
        else:
            self.selected_file = None
            self.file_label.configure(text="Aucun fichier sélectionné")

    def save_settings(self):
        settings = {
            "file_path": self.selected_file,
            "width": self.selected_resolution[0],
            "height": self.selected_resolution[1]
        }
        settings_file_path = self.get_settings_file_path()
        with open(settings_file_path, "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        settings_file_path = self.get_settings_file_path()
        if os.path.exists(settings_file_path):
            with open(settings_file_path, "r") as f:
                data = json.load(f)
                self.selected_file = data.get("file_path", None)
                if self.selected_file:
                    self.file_label.configure(text=f"Fichier sélectionné : {self.selected_file}")
                width = data.get("width", 1440)
                height = data.get("height", 1080)
                self.selected_resolution = (width, height)
                self.width_entry.insert(0, str(width))
                self.height_entry.insert(0, str(height))

    def set_resolution(self, width, height):
        self.selected_resolution = (width, height)
        if not self.selected_file:
            messagebox.showwarning("Erreur", "Aucun fichier sélectionné.")
            return

        try:
            devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
            devmode.PelsWidth = width
            devmode.PelsHeight = height
            devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            win32api.ChangeDisplaySettings(devmode, 0)

            self.update_ini_file(self.selected_file, width, height)

            messagebox.showinfo("Succès", f"La résolution a été modifiée à {width}x{height} avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def apply_custom_resolution(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.set_resolution(width, height)
            self.save_settings()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour la largeur et la hauteur.")

    def update_ini_file(self, filename, width, height):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            new_lines = []
            in_section = False
            fullscreen_mode_exists = False

            for line in lines:
                # Vérifie si on est dans la section [/Script/ShooterGame.ShooterGameUserSettings]
                if line.strip() == '[/Script/ShooterGame.ShooterGameUserSettings]':
                    in_section = True
                    new_lines.append(line)
                    continue

                # Vérifie si on sort de la section
                if in_section and line.strip().startswith('['):
                    in_section = False
                    if not fullscreen_mode_exists:
                        new_lines.append('FullscreenMode=2\n')
                    new_lines.append(line)
                    continue

                # Si on est dans la section, vérifier ou ajouter FullscreenMode
                if in_section:
                    if line.startswith('FullscreenMode='):
                        fullscreen_mode_exists = True
                        new_lines.append('FullscreenMode=2\n')
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

                # Modification des autres paramètres indépendamment de la section
                if line.startswith('ResolutionSizeX='):
                    new_lines[-1] = f'ResolutionSizeX={width}\n'
                elif line.startswith('ResolutionSizeY='):
                    new_lines[-1] = f'ResolutionSizeY={height}\n'
                elif line.startswith('PreferredFullscreenMode='):
                    new_lines[-1] = 'PreferredFullscreenMode=2\n'
                elif line.startswith('LastConfirmedFullscreenMode='):
                    new_lines[-1] = 'LastConfirmedFullscreenMode=2\n'
                elif line.startswith('bShouldLetterbox='):
                    new_lines[-1] = 'bShouldLetterbox=False\n'
                elif line.startswith('bLastConfirmedShouldLetterbox='):
                    new_lines[-1] = 'bLastConfirmedShouldLetterbox=False\n'

            # S'assurer d'ajouter FullscreenMode si la section était la dernière
            if in_section and not fullscreen_mode_exists:
                new_lines.append('FullscreenMode=2\n')

            with open(filename, 'w') as file:
                file.writelines(new_lines)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la mise à jour du fichier INI : {e}")



if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
