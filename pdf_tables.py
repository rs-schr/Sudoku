# -*- coding: utf-8 -*-
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm

# Translations import mit Fallback
try:
    from translations import t, get_current_language
    TRANSLATIONS_AVAILABLE = True
except ImportError:
    TRANSLATIONS_AVAILABLE = False
    # Fallback-Funktion
    def t(key, *args, **kwargs):
        fallback_texts = {
            'puzzle_title': 'Rätsel {}:',
            'solution_title': 'Lösung {}:',
            'debug_creating_table': 'Erstelle Sudoku-Tabelle',
            'debug_table_size': 'Tabellengröße: {}x{}, Zellgröße: {}',
        }
        text = fallback_texts.get(key, key)
        if args or kwargs:
            try:
                return text.format(*args, **kwargs)
            except:
                return text
        return text
    
    def get_current_language():
        return 'de'

# Globale Debug-Variable
DEBUG_MODE = False

def debug_print(message):
    """Gibt Debug-Nachricht aus, nur wenn Debug-Modus aktiviert"""
    if DEBUG_MODE:
        print(f"DEBUG: {message}")

def create_sudoku_table(puzzle, cell_size=0.6):
    """Erstellt eine Sudoku-Tabelle mit der gegebenen Zellgröße"""
    debug_print(t('debug_creating_table'))
    debug_print(t('debug_table_size', 9, 9, cell_size))
    
    puzzle_data = []
    for row in puzzle:
        puzzle_row = []
        for cell in row:
            puzzle_row.append(str(cell) if cell != 0 else "")
        puzzle_data.append(puzzle_row)
    
    table = Table(puzzle_data, colWidths=[cell_size*cm]*9, rowHeights=[cell_size*cm]*9)
    
    # Standard Sudoku-Styling mit stärkeren Box-Linien
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ('FONTSIZE', (0, 0), (-1, -1), max(8, int(cell_size * 16))),  # Dynamische Schriftgröße
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Stärkere Linien für 3x3 Boxen
        ('LINEBELOW', (0, 2), (-1, 2), 2, colors.black),
        ('LINEBELOW', (0, 5), (-1, 5), 2, colors.black),
        ('LINEAFTER', (2, 0), (2, -1), 2, colors.black),
        ('LINEAFTER', (5, 0), (5, -1), 2, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
    ]))
    
    debug_print(f"Sudoku table created with font size: {max(8, int(cell_size * 16))}")
    return table

def create_solution_table(solution, cell_size=0.6):
    """Erstellt eine Lösungs-Tabelle mit grauem Hintergrund"""
    debug_print("Creating solution table")
    debug_print(t('debug_table_size', 9, 9, cell_size))
    
    solution_data = []
    for row in solution:
        solution_row = []
        for cell in row:
            solution_row.append(str(cell))
        solution_data.append(solution_row)
    
    table = Table(solution_data, colWidths=[cell_size*cm]*9, rowHeights=[cell_size*cm]*9)
    
    # Lösungs-Styling mit grauem Hintergrund
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), max(8, int(cell_size * 16))),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Stärkere Linien für 3x3 Boxen
        ('LINEBELOW', (0, 2), (-1, 2), 2, colors.black),
        ('LINEBELOW', (0, 5), (-1, 5), 2, colors.black),
        ('LINEAFTER', (2, 0), (2, -1), 2, colors.black),
        ('LINEAFTER', (5, 0), (5, -1), 2, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        # Grauer Hintergrund für Lösungen
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
    ]))
    
    debug_print("Solution table created with grey background")
    return table

def create_titled_sudoku_cell(title, puzzle, cell_size=0.45):
    """Erstellt eine betitelte Sudoku-Zelle für Grid-Layout"""
    styles = getSampleStyleSheet()
    
    debug_print(f"Creating titled sudoku cell: {title}")
    
    cell_data = [
        [Paragraph(title, styles['Heading4'])],
        [Spacer(1, 0.2*cm)],
        [create_sudoku_table(puzzle, cell_size)]
    ]
    
    # Berechne Gesamthöhe basierend auf Zellgröße
    total_height = 1*cm + cell_size*9*cm + 0.5*cm
    
    cell_table = Table(cell_data, colWidths=[9*cm], 
                      rowHeights=[0.8*cm, 0.2*cm, cell_size*9*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    debug_print(f"Titled sudoku cell created with total height: {total_height}")
    return cell_table

def create_titled_solution_cell(title, solution, cell_size=0.4):
    """Erstellt eine betitelte Lösungs-Zelle für Grid-Layout"""
    styles = getSampleStyleSheet()
    
    debug_print(f"Creating titled solution cell: {title}")
    
    cell_data = [
        [Paragraph(title, styles['Heading4'])],
        [Spacer(1, 0.1*cm)],
        [create_solution_table(solution, cell_size)]
    ]
    
    # Kompaktere Höhen für Lösungen
    cell_table = Table(cell_data, colWidths=[9*cm], 
                      rowHeights=[0.6*cm, 0.1*cm, cell_size*9*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    debug_print(f"Titled solution cell created")
    return cell_table

def create_compact_puzzle_table(puzzle, title, cell_size=0.35):
    """Erstellt eine sehr kompakte Puzzle-Tabelle für dichte Layouts"""
    styles = getSampleStyleSheet()
    
    debug_print(f"Creating compact puzzle table: {title}")
    
    # Mini-Titel
    title_style = styles['Heading4']
    title_style.fontSize = 10
    title_style.leading = 12
    
    cell_data = [
        [Paragraph(title, title_style)],
        [create_sudoku_table(puzzle, cell_size)]
    ]
    
    cell_table = Table(cell_data, colWidths=[cell_size*9*cm + 0.5*cm], 
                      rowHeights=[0.5*cm, cell_size*9*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    debug_print("Compact puzzle table created")
    return cell_table

def create_compact_solution_table(solution, title, cell_size=0.35):
    """Erstellt eine sehr kompakte Lösungs-Tabelle für dichte Layouts"""
    styles = getSampleStyleSheet()
    
    debug_print(f"Creating compact solution table: {title}")
    
    # Mini-Titel
    title_style = styles['Heading4']
    title_style.fontSize = 10
    title_style.leading = 12
    
    cell_data = [
        [Paragraph(title, title_style)],
        [create_solution_table(solution, cell_size)]
    ]
    
    cell_table = Table(cell_data, colWidths=[cell_size*9*cm + 0.5*cm], 
                      rowHeights=[0.5*cm, cell_size*9*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    debug_print("Compact solution table created")
    return cell_table

def set_debug_mode(debug_mode):
    """Setzt den Debug-Modus für dieses Modul"""
    global DEBUG_MODE
    DEBUG_MODE = debug_mode
    debug_print("Debug mode set for pdf_tables module")

# Hilfsfunktionen für verschiedene Layout-Stile
def get_optimal_cell_size(puzzles_per_page):
    """Berechnet optimale Zellgröße basierend auf Anzahl Rätsel pro Seite"""
    size_map = {
        1: 0.9,   # Ein großes Rätsel pro Seite
        2: 0.7,   # Zwei Rätsel pro Seite
        4: 0.45,  # Vier Rätsel pro Seite (2x2)
        6: 0.4,   # Sechs Lösungen pro Seite (3x2)
        8: 0.35,  # Acht kleine Rätsel pro Seite
        9: 0.32   # Neun sehr kleine Rätsel pro Seite (3x3)
    }
    
    optimal_size = size_map.get(puzzles_per_page, 0.6)
    debug_print(f"Optimal cell size for {puzzles_per_page} puzzles per page: {optimal_size}")
    return optimal_size

def get_layout_info(layout_type, puzzles_count):
    """Gibt Layout-Informationen zurück"""
    layouts = {
        'single': {'per_page': 1, 'cell_size': 0.9},
        'double': {'per_page': 2, 'cell_size': 0.7},
        'quad': {'per_page': 4, 'cell_size': 0.45},
        'six_pack': {'per_page': 6, 'cell_size': 0.4},
        'compact': {'per_page': 8, 'cell_size': 0.35}
    }
    
    info = layouts.get(layout_type, layouts['double'])
    pages_needed = (puzzles_count + info['per_page'] - 1) // info['per_page']
    
    debug_print(f"Layout '{layout_type}': {info['per_page']} per page, {pages_needed} pages needed for {puzzles_count} puzzles")
    
    return {
        'per_page': info['per_page'],
        'cell_size': info['cell_size'],
        'pages_needed': pages_needed,
        'total_elements': puzzles_count
    }
