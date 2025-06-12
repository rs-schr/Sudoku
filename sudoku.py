# -*- coding: utf-8 -*-
import argparse
import sys
import os

# Stelle sicher, dass translations verfügbar ist
try:
    from translations import t, get_current_language
    TRANSLATIONS_AVAILABLE = True
except ImportError:
    TRANSLATIONS_AVAILABLE = False
    # Fallback-Funktion wenn translations nicht verfügbar
    def t(key, *args, **kwargs):
        # Einfache Fallback-Übersetzungen
        fallback_texts = {
            'generating_message': 'Generiere {} Sudoku-Rätsel (Level {})...',
            'puzzle_progress': 'Generiere Rätsel {}/{}...',
            'creating_pdf': 'Erstelle PDF: {}',
            'pdf_success': 'PDF erfolgreich erstellt: {}',
            'error_occurred': 'Fehler aufgetreten: {}',
            'debug_mode_enabled': 'Debug-Modus aktiviert',
            'debug_parameters': 'Debug-Parameter: Count={}, Level={}, Hints={}, Output={}',
            'debug_generator_created': 'SudokuGenerator erstellt',
            'debug_puzzle_generated': 'Rätsel {} generiert',
            'debug_filename_generated': 'Dateiname generiert: {}',
        }
        text = fallback_texts.get(key, key)
        if args or kwargs:
            try:
                return text.format(*args, **kwargs)
            except:
                return text
        return text

from sudoku_core import SudokuGenerator
from pdf_generator import create_pdf

# Globale Debug-Variable
DEBUG_MODE = False

def debug_print(message):
    """Gibt Debug-Nachricht aus, nur wenn Debug-Modus aktiviert"""
    if DEBUG_MODE:
        print(f"DEBUG: {message}")

def info_print(message):
    """Gibt normale Info-Nachricht aus"""
    print(message)

def error_print(message):
    """Gibt Fehlermeldung aus"""
    print(f"ERROR: {message}", file=sys.stderr)

def generate_filename(level, count, hintlist):
    """Generiert automatischen Dateinamen"""
    # Sprachabhängige Dateinamen
    if TRANSLATIONS_AVAILABLE:
        current_lang = get_current_language()
        if current_lang == 'en':
            hint_suffix = "_with_hints" if hintlist else "_without_hints"
            filename = f"sudoku_level_{level}_{count}_puzzles{hint_suffix}.pdf"
        else:
            hint_suffix = "_mit_hinweisen" if hintlist else "_ohne_hinweise"
            filename = f"sudoku_level_{level}_{count}_raetsel{hint_suffix}.pdf"
    else:
        # Fallback
        hint_suffix = "_mit_hinweisen" if hintlist else ""
        filename = f"sudoku_level_{level}_{count}_raetsel{hint_suffix}.pdf"
    
    debug_print(t('debug_filename_generated', filename))
    return filename

def main():
    global DEBUG_MODE
    
    parser = argparse.ArgumentParser(description='Sudoku Generator with Multilingual Support')
    parser.add_argument('--count', type=int, default=6, 
                       help='Anzahl der Sudoku-Rätsel / Number of Sudoku puzzles (Default: 6)')
    parser.add_argument('--level', type=int, choices=range(1, 7), default=3, 
                       help='Schwierigkeitsgrad 1-6 / Difficulty level 1-6 (Default: 3)')
    parser.add_argument('--hintlist', action='store_true', 
                       help='Fügt Hinweise zu jedem Rätsel hinzu / Add hints to each puzzle')
    parser.add_argument('--output', type=str, 
                       help='Ausgabedateiname (optional) / Output filename (optional)')
    parser.add_argument('--debug', action='store_true', 
                       help='Aktiviert Debug-Ausgaben / Enable debug output')
    
    args = parser.parse_args()
    
    # Debug-Modus setzen
    DEBUG_MODE = args.debug
    
    try:
        # Debug-Informationen
        if DEBUG_MODE:
            info_print("=" * 60)
            info_print(t('debug_mode_enabled'))
            debug_print(f"Python version: {sys.version}")
            debug_print(f"Arguments: {vars(args)}")
            debug_print(t('debug_parameters', args.count, args.level, args.hintlist, args.output or 'Auto'))
            
            if TRANSLATIONS_AVAILABLE:
                debug_print(f"Current language: {get_current_language()}")
                debug_print("Translations available: Yes")
            else:
                debug_print("Translations available: No (using fallback)")
            
            debug_print(f"Working directory: {os.getcwd()}")
            info_print("=" * 60)
        
        # Normale Ausgabe
        info_print(t('generating_message', args.count, args.level))
        
        if args.hintlist and DEBUG_MODE:
            debug_print("Hints mode enabled")
        
        # Generator erstellen
        generator = SudokuGenerator()
        debug_print(t('debug_generator_created'))
        
        puzzles_and_solutions = []
        
        # Rätsel generieren
        for i in range(args.count):
            if DEBUG_MODE:
                debug_print(t('puzzle_progress', i+1, args.count))
            else:
                # Nur bei mehr als 5 Rätseln Progress anzeigen
                if args.count > 5:
                    info_print(t('puzzle_progress', i+1, args.count))
            
            puzzle, solution = generator.generate_puzzle(args.level)
            puzzles_and_solutions.append((puzzle, solution))
            
            debug_print(t('debug_puzzle_generated', i+1))
        
        # Dateiname bestimmen
        if args.output:
            filename = args.output
            debug_print(f"Using provided filename: {filename}")
        else:
            filename = generate_filename(args.level, args.count, args.hintlist)
            debug_print(f"Generated filename: {filename}")
        
        # PDF erstellen
        info_print(t('creating_pdf', filename))
        
        if DEBUG_MODE:
            debug_print("Calling create_pdf function...")
            debug_print(f"Parameters: filename={filename}, level={args.level}, hintlist={args.hintlist}")
        
        # Debug-Parameter an PDF-Generator weiterleiten
        create_pdf(puzzles_and_solutions, filename, args.level, args.hintlist, debug_mode=DEBUG_MODE)
        
        # Erfolg
        info_print(t('pdf_success', filename))
        
        if DEBUG_MODE:
            debug_print("PDF generation completed successfully")
            debug_print(f"File should be available at: {os.path.abspath(filename)}")
            
            # Datei-Info
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                debug_print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
            else:
                debug_print("WARNING: Output file not found!")
        
    except KeyboardInterrupt:
        error_print("Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        error_print(t('error_occurred', str(e)))
        if DEBUG_MODE:
            import traceback
            debug_print("Full traceback:")
            debug_print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
