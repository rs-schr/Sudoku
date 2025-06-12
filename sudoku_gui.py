# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import json
import threading

from pdf_generator import create_pdf
from sudoku_core import SudokuGenerator

# Konfigurationsdatei
CONFIG_FILE = 'config.json'

# Übersetzungen
TEXTS = {
    'de': {
        'title': 'Sudoku PDF Generator',
        'subtitle': 'Erstellen Sie professionelle Sudoku-Rätsel als PDF',
        'ready': '🎯 Sudoku PDF Generator bereit!',
        'instruction': 'Wählen Sie Ihre Einstellungen und klicken Sie auf \'PDF Generieren\'.',
        'tip_count': '💡 Tipp: Sie können bis zu 100 Rätsel gleichzeitig generieren!',
        'tip_debug': '💡 Tipp: Aktivieren Sie \'Debug-Ausgaben\' für detaillierte Informationen',
        'count_section': 'Anzahl Rätsel',
        'puzzles_label': '{} Rätsel',
        'level_section': 'Schwierigkeitsgrad',
        'level_format': 'Level {}: {}',
        'options_section': 'Optionen',
        'hints_option': 'Hinweise zu Rätseln hinzufügen',
        'debug_section': 'Debug & Entwicklung',
        'debug_option': 'Debug-Ausgaben aktivieren',
        'debug_info': '(Zeigt detaillierte Informationen während der Generierung)',
        'language_section': 'Sprache / Language',
        'language_german': 'Deutsch',
        'language_english': 'English',
        'language_restart': 'Neustart erforderlich für vollständige Sprachänderung',
        'output_section': 'Ausgabedatei (optional)',  # Das fehlende Label!
        'browse_button': 'Durchsuchen...',
        'output_info': 'Leer lassen für automatischen Dateinamen',
        'generate_button': '🎯 PDF Generieren',
        'status_section': 'Status',
        'generating': 'Generiere {} Sudoku-Rätsel (Level {})...',
        'hints_enabled': 'Mit Hinweisen aktiviert',
        'puzzle_progress': 'Generiere Rätsel {}/{}...',
        'creating_pdf': 'Erstelle PDF: {}',
        'pdf_success': 'PDF erfolgreich erstellt: {}',
        'error_occurred': 'Fehler aufgetreten (Exit Code: {})',
        'debug_changed': 'Debug-Modus: {}',
        'hints_changed': 'Hinweise-Status geändert: {}',
        'activated': 'Aktiviert',
        'deactivated': 'Deaktiviert',
        'save_pdf': 'PDF speichern',
        'pdf_files': 'PDF Dateien',
        'all_files': 'Alle Dateien',
        'error': 'Fehler',
        'file_error': 'Fehler beim Erstellen der PDF',
        'open_pdf_question': 'PDF wurde erstellt!\n\nMöchten Sie die Datei jetzt öffnen?',
        'open_pdf_title': 'PDF erstellt'
    },
    'en': {
        'title': 'Sudoku PDF Generator',
        'subtitle': 'Create professional Sudoku puzzles as PDF',
        'ready': '🎯 Sudoku PDF Generator ready!',
        'instruction': 'Choose your settings and click \'Generate PDF\'.',
        'tip_count': '💡 Tip: You can generate up to 100 puzzles at once!',
        'tip_debug': '💡 Tip: Enable \'Debug Output\' for detailed information',
        'count_section': 'Number of Puzzles',
        'puzzles_label': '{} Puzzles',
        'level_section': 'Difficulty Level',
        'level_format': 'Level {}: {}',
        'options_section': 'Options',
        'hints_option': 'Add hints to puzzles',
        'debug_section': 'Debug & Development',
        'debug_option': 'Enable debug output',
        'debug_info': '(Shows detailed information during generation)',
        'language_section': 'Language / Sprache',
        'language_german': 'Deutsch',
        'language_english': 'English',
        'language_restart': 'Restart required for complete language change',
        'output_section': 'Output File (optional)',  # Das fehlende Label!
        'browse_button': 'Browse...',
        'output_info': 'Leave empty for automatic filename',
        'generate_button': '🎯 Generate PDF',
        'status_section': 'Status',
        'generating': 'Generating {} Sudoku puzzles (Level {})...',
        'hints_enabled': 'With hints enabled',
        'puzzle_progress': 'Generating puzzle {}/{}...',
        'creating_pdf': 'Creating PDF: {}',
        'pdf_success': 'PDF successfully created: {}',
        'error_occurred': 'Error occurred (Exit Code: {})',
        'debug_changed': 'Debug mode: {}',
        'hints_changed': 'Hints status changed: {}',
        'activated': 'Activated',
        'deactivated': 'Deactivated',
        'save_pdf': 'Save PDF',
        'pdf_files': 'PDF Files',
        'all_files': 'All Files',
        'error': 'Error',
        'file_error': 'Error creating PDF',
        'open_pdf_question': 'PDF has been created!\n\nWould you like to open the file now?',
        'open_pdf_title': 'PDF Created'
    }
}

def load_config():
    """Lädt die Konfiguration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der Konfiguration: {e}")
    
    return {
        'count': 6,
        'level': 3,
        'hints': False,
        'debug': True,
        'language': 'de',
        'output_file': ''
    }

def save_config(config):
    """Speichert die Konfiguration"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Fehler beim Speichern der Konfiguration: {e}")

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.current_language = self.config.get('language', 'de')
        
        # GUI initialisieren
        self.init_gui()
        self.load_settings()
        
    def t(self, key, *args):
        """Übersetzungsfunktion"""
        text = TEXTS[self.current_language].get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def init_gui(self):
        self.root.title(self.t('title'))
        self.root.geometry("700x800")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel-Bereich
        title_frame = ttk.LabelFrame(main_frame, text="🎯 " + self.t('title'), padding="15")
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(title_frame, text=self.t('subtitle'), font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(title_frame, text=self.t('ready'), font=('Arial', 10, 'bold'), foreground='green').grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Label(title_frame, text=self.t('instruction'), font=('Arial', 9)).grid(row=2, column=0, sticky=tk.W, pady=(2, 0))
        ttk.Label(title_frame, text=self.t('tip_count'), font=('Arial', 8), foreground='blue').grid(row=3, column=0, sticky=tk.W, pady=(8, 0))
        ttk.Label(title_frame, text=self.t('tip_debug'), font=('Arial', 8), foreground='blue').grid(row=4, column=0, sticky=tk.W, pady=(2, 0))
        
        # Anzahl-Bereich
        count_frame = ttk.LabelFrame(main_frame, text=self.t('count_section'), padding="10")
        count_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10), pady=(0, 10))
        
        self.count_var = tk.IntVar(value=self.config.get('count', 6))
        self.count_label = ttk.Label(count_frame, text=self.t('puzzles_label', self.count_var.get()), font=('Arial', 12, 'bold'))
        self.count_label.grid(row=0, column=0, pady=(0, 5))
        
        count_scale = ttk.Scale(count_frame, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.count_var, command=self.on_count_change)
        count_scale.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        count_frame.columnconfigure(0, weight=1)
        
        # Level-Bereich
        level_frame = ttk.LabelFrame(main_frame, text=self.t('level_section'), padding="10")
        level_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.level_var = tk.IntVar(value=self.config.get('level', 3))
        
        level_descriptions = {
            'de': {1: 'Sehr Einfach', 2: 'Einfach', 3: 'Mittel', 4: 'Schwer', 5: 'Sehr Schwer', 6: 'Extrem Schwer'},
            'en': {1: 'Very Easy', 2: 'Easy', 3: 'Medium', 4: 'Hard', 5: 'Very Hard', 6: 'Extremely Hard'}
        }
        
        self.level_label = ttk.Label(level_frame, text=self.t('level_format', self.level_var.get(), level_descriptions[self.current_language][self.level_var.get()]), font=('Arial', 12, 'bold'))
        self.level_label.grid(row=0, column=0, pady=(0, 5))
        
        level_scale = ttk.Scale(level_frame, from_=1, to=6, orient=tk.HORIZONTAL, variable=self.level_var, command=self.on_level_change)
        level_scale.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        level_frame.columnconfigure(0, weight=1)
        
        # Optionen-Bereich
        options_frame = ttk.LabelFrame(main_frame, text=self.t('options_section'), padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.hints_var = tk.BooleanVar(value=self.config.get('hints', False))
        hints_check = ttk.Checkbutton(options_frame, text=self.t('hints_option'), variable=self.hints_var, command=self.on_hints_change)
        hints_check.grid(row=0, column=0, sticky=tk.W)
        
        # Debug-Bereich
        debug_frame = ttk.LabelFrame(main_frame, text=self.t('debug_section'), padding="10")
        debug_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.debug_var = tk.BooleanVar(value=self.config.get('debug', True))
        debug_check = ttk.Checkbutton(debug_frame, text=self.t('debug_option'), variable=self.debug_var, command=self.on_debug_change)
        debug_check.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(debug_frame, text=self.t('debug_info'), font=('Arial', 8), foreground='gray').grid(row=1, column=0, sticky=tk.W, pady=(2, 0))
        
        # Sprach-Bereich
        language_frame = ttk.LabelFrame(main_frame, text=self.t('language_section'), padding="10")
        language_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.language_var = tk.StringVar(value=self.current_language)
        
        ttk.Radiobutton(language_frame, text="🇩🇪 " + self.t('language_german'), variable=self.language_var, value='de', command=self.on_language_change).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(language_frame, text="🇬🇧 " + self.t('language_english'), variable=self.language_var, value='en', command=self.on_language_change).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(language_frame, text=self.t('language_restart'), font=('Arial', 8), foreground='orange').grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        # Ausgabe-Bereich
        output_frame = ttk.LabelFrame(main_frame, text=self.t('output_section'), padding="10")
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Eingabefeld und Browse-Button in einer Zeile
        output_inner_frame = ttk.Frame(output_frame)
        output_inner_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        output_frame.columnconfigure(0, weight=1)

        self.output_var = tk.StringVar(value=self.config.get('output_file', ''))
        output_entry = ttk.Entry(output_inner_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        browse_button = ttk.Button(output_inner_frame, text=self.t('browse_button'), command=self.browse_file)
        browse_button.grid(row=0, column=1)

        output_inner_frame.columnconfigure(0, weight=1)

        ttk.Label(output_frame, text=self.t('output_info'), font=('Arial', 8), foreground='gray').grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # Generieren-Button
        generate_button = ttk.Button(main_frame, text=self.t('generate_button'), command=self.generate_pdf, style='Accent.TButton')
        generate_button.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

        # Status-Bereich
        status_frame = ttk.LabelFrame(main_frame, text=self.t('status_section'), padding="10")
        status_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.status_text = scrolledtext.ScrolledText(status_frame, height=12, width=70, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

        # Responsives Layout
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Erste Status-Nachricht
        self.update_status(self.t('ready'))
        self.update_status(self.t('instruction'))

    def load_settings(self):
        """Lädt die gespeicherten Einstellungen"""
        self.count_var.set(self.config.get('count', 6))
        self.level_var.set(self.config.get('level', 3))
        self.hints_var.set(self.config.get('hints', False))
        self.debug_var.set(self.config.get('debug', True))
        self.output_var.set(self.config.get('output_file', ''))
        
        # Labels aktualisieren
        self.on_count_change(None)
        self.on_level_change(None)
    
    def save_current_config(self):
        """Speichert die aktuelle Konfiguration"""
        self.config = {
            'count': self.count_var.get(),
            'level': self.level_var.get(),
            'hints': self.hints_var.get(),
            'debug': self.debug_var.get(),
            'language': self.current_language,
            'output_file': self.output_var.get()
        }
        save_config(self.config)
    
    def on_count_change(self, value):
        """Wird aufgerufen wenn sich die Anzahl ändert"""
        count = int(float(self.count_var.get()))
        self.count_label.config(text=self.t('puzzles_label', count))
        self.save_current_config()
    
    def on_level_change(self, value):
        """Wird aufgerufen wenn sich das Level ändert"""
        level = int(float(self.level_var.get()))
        level_descriptions = {
            'de': {1: 'Sehr Einfach', 2: 'Einfach', 3: 'Mittel', 4: 'Schwer', 5: 'Sehr Schwer', 6: 'Extrem Schwer'},
            'en': {1: 'Very Easy', 2: 'Easy', 3: 'Medium', 4: 'Hard', 5: 'Very Hard', 6: 'Extremely Hard'}
        }
        self.level_label.config(text=self.t('level_format', level, level_descriptions[self.current_language][level]))
        self.save_current_config()
    
    def on_hints_change(self):
        """Wird aufgerufen wenn sich die Hinweise-Option ändert"""
        status = self.t('activated') if self.hints_var.get() else self.t('deactivated')
        self.update_status(self.t('hints_changed', status))
        self.save_current_config()
    
    def on_debug_change(self):
        """Wird aufgerufen wenn sich die Debug-Option ändert"""
        status = self.t('activated') if self.debug_var.get() else self.t('deactivated')
        self.update_status(self.t('debug_changed', status))
        self.save_current_config()
    
    def on_language_change(self):
        """Wird aufgerufen wenn sich die Sprache ändert"""
        self.current_language = self.language_var.get()
        self.save_current_config()
        self.update_status(f"Language changed to: {self.current_language}")
        self.update_status(self.t('language_restart'))
    
    def browse_file(self):
        """Öffnet den Datei-Dialog"""
        filename = filedialog.asksaveasfilename(
            title=self.t('save_pdf'),
            defaultextension=".pdf",
            filetypes=[
                (self.t('pdf_files'), "*.pdf"),
                (self.t('all_files'), "*.*")
            ]
        )
        if filename:
            self.output_var.set(filename)
            self.save_current_config()
    
    def update_status(self, message):
        """Aktualisiert das Status-Fenster"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def generate_pdf_thread(self):
        """PDF-Generierung in separatem Thread"""
        try:
            count = self.count_var.get()
            level = self.level_var.get()
            hints = self.hints_var.get()
            output_file = self.output_var.get().strip()
            
            # Status-Updates
            self.update_status("=" * 50)
            self.update_status(self.t('generating', count, level))
            if hints:
                self.update_status(self.t('hints_enabled'))
            
            # PDF-Name generieren falls leer
            if not output_file:
                if self.current_language == 'de':
                    hint_suffix = "_mit_hinweisen" if hints else "_ohne_hinweise"
                    output_file = f"sudoku_level_{level}_{count}_raetsel{hint_suffix}.pdf"
                else:
                    hint_suffix = "_with_hints" if hints else "_without_hints"
                    output_file = f"sudoku_level_{level}_{count}_puzzles{hint_suffix}.pdf"
            
            # Sudokus generieren
            generator = SudokuGenerator()
            puzzles_and_solutions = []
            
            for i in range(count):
                if self.debug_var.get():
                    self.update_status(self.t('puzzle_progress', i+1, count))
                puzzle, solution = generator.generate_puzzle(level)
                puzzles_and_solutions.append((puzzle, solution))
            
            # PDF erstellen
            self.update_status(self.t('creating_pdf', output_file))
            create_pdf(puzzles_and_solutions, output_file, level, hints, self.current_language)
            
            self.update_status(self.t('pdf_success', output_file))
            self.update_status("=" * 50)
            
            # Nachfrage ob PDF öffnen
            def ask_open_pdf():
                if messagebox.askyesno(self.t('open_pdf_title'), self.t('open_pdf_question')):
                    try:
                        if sys.platform.startswith('win'):
                            os.startfile(output_file)
                        elif sys.platform.startswith('darwin'):
                            subprocess.call(['open', output_file])
                        else:
                            subprocess.call(['xdg-open', output_file])
                    except Exception as e:
                        self.update_status(f"Fehler beim Öffnen der PDF: {e}")
            
            # UI-Update im Hauptthread
            self.root.after(0, ask_open_pdf)
            
        except Exception as e:
            error_msg = f"{self.t('file_error')}: {str(e)}"
            self.update_status(error_msg)
            self.root.after(0, lambda: messagebox.showerror(self.t('error'), error_msg))
    
    def generate_pdf(self):
        """Startet die PDF-Generierung"""
        # Thread für PDF-Generierung starten
        thread = threading.Thread(target=self.generate_pdf_thread, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
