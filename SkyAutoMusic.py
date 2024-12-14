import pydirectinput
import time
import tkinter as tk
from tkinter import filedialog, Button, messagebox, Label, StringVar, Frame, Checkbutton, BooleanVar, Radiobutton
import winsound
import os
import json
import subprocess
import logging
from typing import Optional, Dict

# Konfiguration des Loggings
logging.basicConfig(
    filename='app.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    filemode='w'
)

# Übersetzungen
LANGUAGES = {
    'de': {
        'title': 'SkyAutoMusic',
        'choose_file': 'Datei auswählen',
        'no_file_selected': 'Keine Datei ausgewählt',
        'file_selected': 'Ausgewählte Datei\n',
        'slow': 'Langsam',
        'medium': 'Mittel',
        'fast': 'Schnell',
        'long_press': 'Langes Drücken',
        'start': 'Start',
        'error': 'Fehler',
        'invalid_json': 'Ungültiges JSON-Format.',
        'unknown_error': 'Unbekannter Fehler.',
        'new_song': 'Neues Lied',
        'oder': 'oder',
        'app_close': 'Die Anwendung schließen?',
        'finish': 'Fertig',
        'error_invalid_json': 'Ungültiges JSON-Format.',
        'error_processing_file': 'Fehler beim Verarbeiten der Datei: '
    },
    'en': {
        'title': 'SkyAutoMusic',
        'choose_file': 'Choose File',
        'no_file_selected': 'No file selected',
        'file_selected': 'Selected file: ',
        'slow': 'Slow',
        'medium': 'Medium',
        'fast': 'Fast',
        'long_press': 'Long Press',
        'start': 'Start',
        'error': 'Error',
        'invalid_json': 'Invalid JSON format.',
        'unknown_error': 'Unknown error.',
        'new_song': 'New song',
        'oder': 'or',
        'app_close': 'Close the application?',
        'finish': 'Finish',
        'error_invalid_json': 'Invalid JSON format.',
        'error_processing_file': 'Error processing the file: '
    }
}

# Funktion zum Verstecken von Dateien
def hide_file(file_path):
    """Markiert die Datei als versteckt."""
    logging.info("========== Verstecke Datei ==========")
    if os.path.exists(file_path):
        subprocess.run(["attrib", "+h", file_path])

# Funktion zum Laden von Konfigurationen aus config.json
def load_config():
    logging.info("========== Konfiguration laden ==========")
    if not os.path.exists("config.json"):
        raise FileNotFoundError("Konfigurationsdatei 'config.json' nicht gefunden.")
    
    with open("config.json", "r", encoding="utf-8") as file:
        logging.info("Konfiguration erfolgreich geladen.")
        return json.load(file)

def save_config(config):
    """Speichert die aktuelle Konfiguration in config.json."""
    logging.info("========== Konfiguration speichern ==========")
    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)
        logging.info("Konfiguration erfolgreich gespeichert.")

def set_icon(window, icon_path="icon.ico"):
    """Setzt das Icon für das gegebene Fenster, wenn verfügbar."""
    logging.info("========== Setze Icon ==========")
    if os.path.exists(icon_path):
        window.iconbitmap(icon_path)
        logging.info(f"Icon '{icon_path}' wurde erfolgreich gesetzt.")
    else:
        logging.warning(f"Icon '{icon_path}' nicht gefunden.")

def on_closing(root):
    """Behandelt das Schließen der Anwendung und schreibt ins Log."""
    logging.info("Anwendung geschlossen")
    root.quit()

def choose_language():
    def set_language():
        nonlocal selected_language
        selected_language = var.get()
        lang_window.destroy()

    selected_language = None
    lang_window = tk.Tk()
    lang_window.title("Choose Language")
    lang_window.geometry("270x100")
    
    set_icon(lang_window)

    var = tk.StringVar()
    var.set(config.get('selected_language', None))

    # RadioButtons für die Sprachauswahl
    tk.Radiobutton(lang_window, text="Deutsch", variable=var, value="de", font=("Helvetica", 12), command=lambda: ok_button.config(state=tk.NORMAL)).pack(anchor=tk.W)
    tk.Radiobutton(lang_window, text="English", variable=var, value="en", font=("Helvetica", 12), command=lambda: ok_button.config(state=tk.NORMAL)).pack(anchor=tk.W)
    
    # OK-Button, anfänglich deaktiviert
    ok_button = tk.Button(lang_window, text="OK", command=set_language, font=("Helvetica", 12), state=tk.DISABLED)
    ok_button.pack()

    lang_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(lang_window))
    lang_window.mainloop()

    return selected_language

class SkyAutoMusicPlayer:
    def __init__(self, root: tk.Tk, lang: str):
        """Initialisiert die Anwendung und richtet die Benutzeroberfläche ein."""
        logging.info("========== Initialisiere SkyAutoMusicPlayer ==========")
        self.root = root
        self.filename: Optional[str] = None
        self.long_press_duration: Optional[float] = None  # Dauer des langen Tastendrucks
        self.long_press = BooleanVar()  # Variable für das lange Tastendrucken
        self.selected_speed: Optional[str] = None  # Variable für die gewählte Geschwindigkeit
        self.lang = lang  # Sprachwahl
        self.translations = LANGUAGES[self.lang]  # Textübersetzung laden
        self.setup_ui()
        logging.info("SkyAutoMusicPlayer erfolgreich initialisiert")

    def setup_ui(self):
        logging.info("========== Benutzeroberfläche einrichten ==========")
        self.setup_window()
        set_icon(self.root)
        self.add_ui_elements()
        self.root.protocol("WM_DELETE_WINDOW", lambda: on_closing(self.root))
        logging.info("Benutzeroberfläche erfolgreich eingerichtet")

    def setup_window(self):
        """Initialisiert das Hauptfenster."""        
        self.root.title(self.translations['title'])
        self.root.geometry("400x350")

    def add_ui_elements(self):
        """Fügt alle UI-Elemente zum Fenster hinzu."""
        self.add_title()
        self.add_file_selection_button()
        self.add_status_label()
        self.add_speed_buttons()
        self.add_checkbox()
        self.add_play_button()

    def add_title(self):
        """Fügt den Titel zur Oberfläche hinzu.""" 
        logging.info("========== Titel hinzufügen ==========")
        self.title_label = Label(self.root, text=self.translations['title'], font=("Helvetica", 16, "bold"), pady=10)
        self.title_label.pack()
        logging.info("Titel wurde zur Oberfläche hinzugefügt")

    def add_file_selection_button(self):
        """Fügt die Schaltfläche zum Auswählen einer Datei hinzu.""" 
        logging.info("========== Datei-Auswahl-Schaltfläche hinzufügen ==========")
        self.button_frame = Frame(self.root, pady=10)
        self.button_frame.pack(fill=tk.X, padx=20)
        self.choose_file_button = Button(self.button_frame, text=self.translations['choose_file'], command=self.choose_file, font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8)
        self.choose_file_button.pack(pady=5)
        logging.info("Datei-Auswahl-Schaltfläche wurde hinzugefügt")

    def add_status_label(self):
        """Fügt das Label für den Dateistatus hinzu.""" 
        logging.info("========== Statuslabel hinzufügen ==========")
        self.status_var = StringVar()
        self.status_var.set(self.translations['no_file_selected'])
        self.status_label = Label(self.button_frame, textvariable=self.status_var, font=("Helvetica", 12))
        self.status_label.pack(pady=5)
        logging.info("Statuslabel wurde hinzugefügt")

    def add_speed_buttons(self):
        """Fügt den Rahmen für die Geschwindigkeits-Schaltflächen hinzu und zeigt sie an.""" 
        logging.info("========== Geschwindigkeits-Schaltflächen hinzufügen ==========")
        self.speed_frame = Frame(self.root)
        self.speed_frame.pack(fill=tk.X, padx=20)

        button_frame = Frame(self.speed_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        for speed_key, label in [('slow', self.translations['slow']), 
                                ('medium', self.translations['medium']), 
                                ('fast', self.translations['fast'])]:
            Button(button_frame, text=label, command=lambda key=speed_key: self.select_speed(key), font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8).pack(side=tk.LEFT, padx=10)

        logging.info("Geschwindigkeits-Schaltflächen wurden hinzugefügt")

    def add_checkbox(self):
        """Fügt die Checkbox hinzu.""" 
        logging.info("========== Checkbox hinzufügen ==========")
        self.long_press_checkbox = Checkbutton(self.root, text=self.translations['long_press'], variable=self.long_press, font=("Helvetica", 12))
        self.long_press_checkbox.pack(pady=5)
        logging.info("Checkbox für langes Drücken wurde hinzugefügt")

    def add_play_button(self):
        """Fügt den Play-Button hinzu.""" 
        logging.info("========== Play-Button hinzufügen ==========")
        self.play_button = Button(self.root, text=self.translations['start'], command=self.start_process, state=tk.DISABLED, font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8)
        self.play_button.pack(pady=10)
        logging.info("Play-Button wurde hinzugefügt.")

    def choose_file(self):
        """Öffnet einen Dateidialog zur Auswahl einer Datei und zeigt die Geschwindigkeits-Schaltflächen an.""" 
        logging.info("========== Datei auswählen ==========")
        self.filename = filedialog.askopenfilename(
            initialdir="Songs",
            filetypes=(("Alle Daten", "*"), ("Textdateien", "*.txt"), ("Json", "*.json"), ("Skysheet", "*.skysheet"))
        )
        if not self.filename:
            logging.info("Keine Datei ausgewählt")
            return
        
        self.status_var.set(f"{self.translations['file_selected']}{os.path.basename(self.filename)}")
        logging.info(f"Datei ausgewählt: {self.filename}")
        self.update_play_button_state()

    def select_speed(self, speed_key: str):
        """Speichert die ausgewählte Geschwindigkeit und aktiviert den Play-Button.""" 
        logging.info("========== Geschwindigkeit auswählen ==========")
        self.selected_speed = speed_key
        self.long_press_duration = LONG_PRESS_DURATION.get(speed_key)
        logging.info("Geschwindigkeit ausgewählt")
        self.update_play_button_state()

    def update_play_button_state(self):
        """Überprüft, ob eine Datei und eine Geschwindigkeit ausgewählt sind und aktiviert oder deaktiviert den Play-Button.""" 
        logging.info("========== Play-Button-Zustand aktualisieren ==========")
        if self.filename and self.selected_speed:
            self.play_button.config(state=tk.NORMAL)
            logging.info("Play-Button aktiviert")
        else:
            self.play_button.config(state=tk.DISABLED)
            logging.info("Play-Button deaktiviert")

    def get_speed(self) -> Optional[float]:
        """Gibt die Geschwindigkeit basierend auf der Auswahl zurück.""" 
        logging.info("========== Geschwindigkeit abrufen ==========")
        speed_value = SPEEDS.get(self.selected_speed)
        return speed_value

    def start_process(self):
        """Startet den Prozess zum Simulieren von Tasteneingaben basierend auf der gewählten Geschwindigkeit.""" 
        logging.info("========== Prozess starten ==========")
        speed = self.get_speed()
        self.root.withdraw()
        try:
            read_file = self.read_file()
            modified_sentence = self.replace_sent(read_file)
            time.sleep(1.5)
            self.simulate_typing(modified_sentence, speed)
            winsound.Beep(1000, 500)
            self.show_restart_message()
            logging.info("Prozess erfolgreich abgeschlossen")
        except json.JSONDecodeError as e:
            messagebox.showerror(self.translations['error'], self.translations['invalid_json'])
            logging.warning(f"JSON error: {e}")
        except Exception as e:
            messagebox.showerror(self.translations['error'], f"{self.translations['unknown_error']}: {e}")
            logging.error(f"Unexpected error: {e}")
        finally:
            self.root.deiconify()
            logging.info("Prozess beendet")

    def read_file(self) -> str:
        """Liest den Inhalt der Datei und konvertiert Noten zu Zeichen.""" 
        logging.info("========== Datei lesen ==========")
        with open(self.filename, "r", encoding="utf-8") as file:
            content = file.read().strip()
            try:
                data = json.loads(content)
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], Dict) and "songNotes" in data[0]:
                    song_notes = data[0]["songNotes"]
                    logging.info("Songnoten aus JSON gefunden ")
                    return " ".join(self.get_note_key(note) for note in song_notes)
                else:
                    raise ValueError(self.translations['error_invalid_json'])
            except json.JSONDecodeError:
                logging.info("Inhalt als Klartext behandelt")
                return content
            except Exception as e:
                logging.error("Fehler bei der Verarbeitung des Dateiinhalts")
                raise ValueError(f"{self.translations['error_processing_file']}{e}")
                
    def get_note_key(self, note: Dict) -> str:
        """Ersetzt den Key in der Datei durch das entsprechende Zeichen aus dem KEY_MAPPING."""
        key = note["key"]
        key_lower = key.lower()
        mapped_key = KEY_MAPPING.get(key_lower.capitalize(), "")
        return mapped_key

    def replace_sent(self, content: str) -> str:
        """Ersetzt Platzhalter durch entsprechende Zeichen.""" 
        for placeholder, replacement in REPLACEMENTS.items():
            content = content.replace(placeholder, replacement)
        return content

    def simulate_typing(self, sentence: str, speed: float):
        """Simuliert das Schreiben eines Satzes mit der angegebenen Geschwindigkeit, 
        berücksichtigt dabei das lange Tastendrucken, wenn die Checkbox ausgewählt ist und ignoriert Leerzeichen.""" 
        logging.info("========== Tippen simulieren ==========")

        for char in sentence:
            if char == ' ':
                continue

            if self.long_press.get():
                pydirectinput.keyDown(char)
                time.sleep(self.long_press_duration)
                pydirectinput.keyUp(char)
            else:
                pydirectinput.press(char)
                
            # Verzögerung nach jedem Tastenanschlag
            time.sleep(speed)

    def show_restart_message(self):
        """Zeigt eine Nachricht an, die den Benutzer darüber informiert, dass der Prozess abgeschlossen ist.""" 
        logging.info("========== Neustartnachricht anzeigen ==========")

        message = f"{self.translations['new_song']}\n\n" \
                f"{self.translations['oder']}\n\n" \
                f"{self.translations['app_close']}"

        result = messagebox.askyesno(self.translations['finish'], message)

        if result:
            logging.info("Anwendung für neues Lied neu gestartet.")
            self.root.deiconify()
        else:
            logging.info("Anwendung vom Benutzer geschlossen.")
            self.root.quit()

if __name__ == "__main__":
    try:
        # Überprüfen, ob die Konfigurationsdatei existiert, und ggf. erstellen
        if not os.path.exists("config.json"):
            logging.warning("Konfigurationsdatei 'config.json' nicht gefunden. Erstelle sie mit create_config.bat.")
            subprocess.run(["create_config.bat"], check=True)
            if not os.path.exists("config.json"):
                raise FileNotFoundError("Konfigurationsdatei 'config.json' konnte nach dem Aufruf von create_config.bat nicht erstellt werden.")
        
        config = load_config()
        hide_file("create_config.bat")
        selected_language = config.get('selected_language')
        if selected_language is None:
            selected_language = choose_language()
            config['selected_language'] = selected_language
            save_config(config)

        # Zugriff auf Sprache, Tastenzuordnung, Platzhalter und Geschwindigkeiten aus der geladenen Konfiguration
        KEY_MAPPING = config.get('key_mapping', {})
        REPLACEMENTS = config.get('replacements', {})
        SPEEDS = config.get('speeds', {})
        LONG_PRESS_DURATION = config.get("long_press_duration", {})

    except Exception as e:
        logging.error(f"Fehler beim Laden der Konfiguration: {str(e)}")
        messagebox.showerror("Fehler", str(e))

    logging.info("========== Anwendung starten ==========")

    root = tk.Tk()
    app = SkyAutoMusicPlayer(root, selected_language)
    root.mainloop()
