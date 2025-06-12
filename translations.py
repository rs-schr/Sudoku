# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, Any

class TranslationManager:
    def __init__(self):
        self.current_language = 'de'  # Standard: Deutsch
        self.config_file = 'language_config.json'
        self.translations = {
            'de': {
                # GUI Hauptelemente
                'app_title': 'Sudoku PDF Generator',
                'app_subtitle': 'Erstellen Sie professionelle Sudoku-Rätsel als PDF',
                
                # Titel-Bereich
                'ready_message': '🎯 Sudoku PDF Generator bereit!',
                'instruction_message': 'Wählen Sie Ihre Einstellungen und klicken Sie auf \'PDF Generieren\'.',
                'tip_count': '💡 Tipp: Sie können bis zu 100 Rätsel gleichzeitig generieren!',
                'tip_debug': '💡 Tipp: Aktivieren Sie \'Debug-Ausgaben\' für detaillierte Informationen',
                
                # Anzahl-Bereich
                'count_section': 'Anzahl Rätsel',
                'puzzles_label': '{} Rätsel',
                
                # Schwierigkeitsgrad
                'level_section': 'Schwierigkeitsgrad',
                'level_very_easy': 'Sehr Einfach',
                'level_easy': 'Einfach',
                'level_medium': 'Mittel',
                'level_hard': 'Schwer',
                'level_very_hard': 'Sehr Schwer',
                'level_extreme': 'Extrem Schwer',
                'level_format': 'Level {}: {}',
                
                # Optionen
                'options_section': 'Optionen',
                'hints_option': 'Hinweise zu Rätseln hinzufügen',
                
                # Debug
                'debug_section': 'Debug & Entwicklung',
                'debug_option': 'Debug-Ausgaben aktivieren',
                'debug_info': '(Zeigt detaillierte Informationen während der Generierung)',
                
                # Sprache
                'language_section': 'Sprache / Language',
                'language_german': 'Deutsch',
                'language_english': 'English',
                'language_restart': 'Neustart erforderlich für vollständige Sprachänderung',
                
                # Ausgabe
                'output_section': 'Ausgabedatei (optional)',
                'browse_button': 'Durchsuchen...',
                'output_info': 'Leer lassen für automatischen Dateinamen',
                
                # Aktionen
                'generate_button': '🎯 PDF Generieren',
                'status_section': 'Status',
                
                # Status-Nachrichten
                'generating_message': 'Generiere {} Sudoku-Rätsel (Level {})...',
                'hints_enabled': 'Mit Hinweisen aktiviert',
                'puzzle_progress': 'Generiere Rätsel {}/{}...',
                'creating_pdf': 'Erstelle PDF: {}',
                'pdf_success': 'PDF erfolgreich erstellt: {}',
                'error_occurred': 'Fehler aufgetreten (Exit Code: {})',
                'debug_mode_changed': 'Debug-Modus: {}',
                'hints_status_changed': 'Hinweise-Status geändert: {}',
                'activated': 'Aktiviert',
                'deactivated': 'Deaktiviert',
                
                # PDF-Inhalte
                'puzzle_title': 'Rätsel {}:',
                'solution_title': 'Lösung {}:',
                'solutions_page': 'Lösungen',
                'hints_label': 'Hinweise:',
                'no_hints': 'Keine eindeutigen Hinweise verfügbar',
                'pdf_title_with_hints': 'Sudoku Rätsel (Level {}) - {} - Mit Hinweisen',
                'pdf_title_without_hints': 'Sudoku Rätsel (Level {}) - {} - Ohne Hinweise',
                
                # Datei-Dialog
                'save_pdf': 'PDF speichern',
                'pdf_files': 'PDF Dateien',
                'all_files': 'Alle Dateien',
                
                # Fehlermeldungen
                'error': 'Fehler',
                'file_error': 'Fehler beim Erstellen der PDF',
                'generation_error': 'Fehler bei der Generierung',
            },
            'en': {
                # GUI Main Elements
                'app_title': 'Sudoku PDF Generator',
                'app_subtitle': 'Create professional Sudoku puzzles as PDF',
                
                # Title Area
                'ready_message': '🎯 Sudoku PDF Generator ready!',
                'instruction_message': 'Choose your settings and click \'Generate PDF\'.',
                'tip_count': '💡 Tip: You can generate up to 100 puzzles at once!',
                'tip_debug': '💡 Tip: Enable \'Debug Output\' for detailed information',
                
                # Count Area
                'count_section': 'Number of Puzzles',
                'puzzles_label': '{} Puzzles',
                
                # Difficulty Level
                'level_section': 'Difficulty Level',
                'level_very_easy': 'Very Easy',
                'level_easy': 'Easy',
                'level_medium': 'Medium',
                'level_hard': 'Hard',
                'level_very_hard': 'Very Hard',
                'level_extreme': 'Extremely Hard',
                'level_format': 'Level {}: {}',
                
                # Options
                'options_section': 'Options',
                'hints_option': 'Add hints to puzzles',
                
                # Debug
                'debug_section': 'Debug & Development',
                'debug_option': 'Enable debug output',
                'debug_info': '(Shows detailed information during generation)',
                
                # Language
                'language_section': 'Language / Sprache',
                'language_german': 'Deutsch',
                'language_english': 'English',
                'language_restart': 'Restart required for complete language change',
                
                # Output
                'output_section': 'Output File (optional)',
                'browse_button': 'Browse...',
                'output_info': 'Leave empty for automatic filename',
                
                # Actions
                'generate_button': '🎯 Generate PDF',
                'status_section': 'Status',
                
                # Status Messages
                'generating_message': 'Generating {} Sudoku puzzles (Level {})...',
                'hints_enabled': 'With hints enabled',
                'puzzle_progress': 'Generating puzzle {}/{}...',
                'creating_pdf': 'Creating PDF: {}',
                'pdf_success': 'PDF successfully created: {}',
                'error_occurred': 'Error occurred (Exit Code: {})',
                'debug_mode_changed': 'Debug mode: {}',
                'hints_status_changed': 'Hints status changed: {}',
                'activated': 'Activated',
                'deactivated': 'Deactivated',
                
                # PDF Contents
                'puzzle_title': 'Puzzle {}:',
                'solution_title': 'Solution {}:',
                'solutions_page': 'Solutions',
                'hints_label': 'Hints:',
                'no_hints': 'No obvious hints available',
                'pdf_title_with_hints': 'Sudoku Puzzles (Level {}) - {} - With Hints',
                'pdf_title_without_hints': 'Sudoku Puzzles (Level {}) - {} - Without Hints',
                
                # File Dialog
                'save_pdf': 'Save PDF',
                'pdf_files': 'PDF Files',
                'all_files': 'All Files',
                
                # Error Messages
                'error': 'Error',
                'file_error': 'Error creating PDF',
                'generation_error': 'Error during generation',
            }
        }
        
        # Lade gespeicherte Spracheinstellung
        self.load_language_config()
    
    def get_text(self, key: str, *args, **kwargs) -> str:
        """Holt übersetzten Text für aktuellen Sprache"""
        try:
            text = self.translations[self.current_language].get(key, key)
            # Formatierung unterstützen
            if args or kwargs:
                return text.format(*args, **kwargs)
            return text
        except (KeyError, ValueError):
            return key
    
    def set_language(self, language_code: str):
        """Setzt die aktuelle Sprache"""
        if language_code in self.translations:
            self.current_language = language_code
            self.save_language_config()
    
    def get_current_language(self) -> str:
        """Gibt aktuellen Sprachcode zurück"""
        return self.current_language
    
    def get_available_languages(self) -> Dict[str, str]:
        """Gibt verfügbare Sprachen zurück"""
        return {
            'de': self.get_text('language_german'),
            'en': self.get_text('language_english')
        }
    
    def save_language_config(self):
        """Speichert Sprachkonfiguration in Datei"""
        try:
            config = {
                'language': self.current_language
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Could not save language config: {e}")
    
    def load_language_config(self):
        """Lädt Sprachkonfiguration aus Datei"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_language = config.get('language', 'de')
        except Exception as e:
            print(f"Could not load language config: {e}")
            self.current_language = 'de'  # Fallback auf Deutsch

# Globale Instanz
_translator = TranslationManager()

def get_translator() -> TranslationManager:
    """Gibt globale Translator-Instanz zurück"""
    return _translator

def t(key: str, *args, **kwargs) -> str:
    """Kurze Funktion für Übersetzungen"""
    return _translator.get_text(key, *args, **kwargs)

def set_language(language_code: str):
    """Setzt globale Sprache"""
    _translator.set_language(language_code)

def get_current_language() -> str:
    """Gibt aktuelle Sprache zurück"""
    return _translator.get_current_language()
