# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
from translations import t, set_language, get_current_language

class EventHandlers:
    def __init__(self, gui):
        self.gui = gui
        
    def update_count_label(self, value=None):
        """Aktualisiert das Label für die Anzahl der Rätsel"""
        if value is None:
            count = self.gui.count_var.get()
        else:
            count = int(float(value))
        
        # Aktualisiere Label mit übersetztem Text
        self.gui.count_label.config(text=t('puzzles_label', count))
        
        # Debug-Ausgabe falls aktiviert
        if self.gui.debug_var.get():
            self.gui.add_status(f"DEBUG: {t('puzzles_label', count)}")
    
    def on_language_change(self):
        """Behandelt Sprachwechsel"""
        selected_language = self.gui.language_var.get()
        current_language = get_current_language()
        
        if selected_language != current_language:
            # Sprache in Translator setzen
            set_language(selected_language)
            
            # Benutzer über Sprachwechsel informieren
            if selected_language == 'de':
                self.gui.add_status("🌍 Sprache geändert zu: Deutsch")
                self.gui.add_status("⚠️ Neustart der Anwendung empfohlen für vollständige Sprachänderung")
            else:
                self.gui.add_status("🌍 Language changed to: English")
                self.gui.add_status("⚠️ Application restart recommended for complete language change")
            
            # Debug-Ausgabe
            if self.gui.debug_var.get():
                self.gui.add_status(f"DEBUG: Language changed from {current_language} to {selected_language}")
    
    def browse_file(self):
        """Öffnet Dateiauswahl-Dialog"""
        try:
            # Dateiauswahl mit übersetzten Texten
            filename = filedialog.asksaveasfilename(
                title=t('save_pdf'),
                defaultextension=".pdf",
                filetypes=[
                    (t('pdf_files'), "*.pdf"),
                    (t('all_files'), "*.*")
                ]
            )
            
            if filename:
                self.gui.output_var.set(filename)
                self.gui.add_status(f"📁 {t('output_section')}: {filename}")
                
                # Debug-Ausgabe
                if self.gui.debug_var.get():
                    self.gui.add_status(f"DEBUG: Output file selected: {filename}")
                    
        except Exception as e:
            error_msg = f"{t('error')}: {str(e)}"
            self.gui.add_status(error_msg)
            if self.gui.debug_var.get():
                self.gui.add_status(f"DEBUG: File dialog error: {e}")
    
    def generate_pdf(self):
        """Startet PDF-Generierung in separatem Thread"""
        # Deaktiviere Button während Generierung
        self.gui.generate_btn.config(state='disabled')
        self.gui.progress.start()
        
        # Starte Generierung in separatem Thread
        thread = threading.Thread(target=self._generate_pdf_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_pdf_thread(self):
        """PDF-Generierung in separatem Thread"""
        try:
            # Parameter sammeln
            count = self.gui.count_var.get()
            level = self.gui.level_var.get()
            hints = self.gui.hints_var.get()
            debug = self.gui.debug_var.get()
            output = self.gui.output_var.get().strip()
            
            # Status-Nachrichten
            self.gui.add_status("=" * 50)
            self.gui.add_status(t('generating_message', count, level))
            
            if hints:
                self.gui.add_status(f"✅ {t('hints_enabled')}")
            
            if debug:
                self.gui.add_status("🔧 Debug-Modus aktiviert")
                
            # Kommando für Subprocess aufbauen
            cmd = [
                'python', 'sudoku.py',
                '--count', str(count),
                '--level', str(level)
            ]
            
            # Debug-Parameter hinzufügen
            if debug:
                cmd.append('--debug')
            
            # Hints-Parameter hinzufügen
            if hints:
                cmd.append('--hintlist')
            
            # Output-Parameter hinzufügen
            if output:
                cmd.extend(['--output', output])
            
            # Debug: Kommando anzeigen
            if debug:
                self.gui.add_status(f"DEBUG: Command: {' '.join(cmd)}")
            
            # Subprocess starten
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            # Output verarbeiten
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        self.gui.add_status(line)
            
            # Fehler verarbeiten
            if result.stderr:
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        self.gui.add_status(f"⚠️ {line}")
            
            # Erfolg/Fehler Status
            if result.returncode == 0:
                self.gui.add_status("✅ " + t('pdf_success', output if output else 'Auto-generierter Name'))
                self.gui.add_status("=" * 50)
            else:
                self.gui.add_status(f"❌ {t('error_occurred', result.returncode)}")
                if debug:
                    self.gui.add_status(f"DEBUG: Return code: {result.returncode}")
                    self.gui.add_status(f"DEBUG: Command: {' '.join(cmd)}")
                
        except Exception as e:
            error_msg = f"❌ {t('generation_error')}: {str(e)}"
            self.gui.add_status(error_msg)
            if self.gui.debug_var.get():
                self.gui.add_status(f"DEBUG: Exception: {e}")
                import traceback
                self.gui.add_status(f"DEBUG: Traceback: {traceback.format_exc()}")
        
        finally:
            # GUI-Elemente wieder aktivieren
            self.gui.generate_btn.config(state='normal')
            self.gui.progress.stop()
    
    def on_hints_changed(self, *args):
        """Callback wenn sich Hints-Status ändert"""
        status = self.gui.hints_var.get()
        status_text = t('activated') if status else t('deactivated')
        
        if self.gui.debug_var.get():
            self.gui.add_status(f"DEBUG: {t('hints_status_changed', status_text)}")
    
    def on_debug_changed(self, *args):
        """Callback wenn sich Debug-Status ändert"""
        status = self.gui.debug_var.get()
        status_text = t('activated') if status else t('deactivated')
        self.gui.add_status(f"🔧 {t('debug_mode_changed', status_text)}")
        
        # Zeige/verstecke zusätzliche Debug-Informationen
        if status:
            self.gui.add_status("🔧 Debug-Informationen werden nun angezeigt")
            self.gui.add_status(f"🔧 Aktuelle Sprache: {get_current_language()}")
            self.gui.add_status(f"🔧 Python-Version: {self._get_python_version()}")
        else:
            self.gui.add_status("🔧 Debug-Informationen deaktiviert")
    
    def _get_python_version(self):
        """Ermittelt Python-Version für Debug-Ausgabe"""
        try:
            import sys
            return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except:
            return "Unbekannt"
    
    def show_about(self):
        """Zeigt About-Dialog"""
        about_text = f"""
{t('app_title')}

{t('app_subtitle')}

Version: 2.0
Sprache: {get_current_language().upper()}

Features:
• {t('count_section')}: 1-100
• {t('level_section')}: 1-6
• {t('hints_option')}
• {t('debug_option')}
• Mehrsprachig (DE/EN)
        """
        
        messagebox.showinfo(
            title=f"About {t('app_title')}",
            message=about_text.strip()
        )
    
    def clear_status(self):
        """Löscht Status-Anzeige"""
        self.gui.clear_status()
        self.gui.add_status(t('ready_message'))
        
        if self.gui.debug_var.get():
            self.gui.add_status("DEBUG: Status cleared")
    
    def restart_application(self):
        """Startet Anwendung neu (für Sprachwechsel)"""
        if messagebox.askyesno(
            title=t('language_section'),
            message=t('language_restart') + "\n\nNeustart jetzt durchführen?\nRestart now?"
        ):
            try:
                import sys
                import os
                python = sys.executable
                os.execl(python, python, *sys.argv)
            except Exception as e:
                self.gui.add_status(f"❌ Restart failed: {e}")
