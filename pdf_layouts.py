# -*- coding: utf-8 -*-
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from sudoku_core import SudokuSolver
from pdf_tables import create_sudoku_table, create_solution_table, create_titled_sudoku_cell, create_titled_solution_cell

def get_texts(language):
    """Gibt Übersetzungen zurück"""
    texts = {
        'de': {
            'puzzle': 'Rätsel {}:',
            'solution': 'Lösung {}:',
            'hints': 'Hinweise:',
            'no_hints': 'Keine eindeutigen Hinweise verfügbar'
        },
        'en': {
            'puzzle': 'Puzzle {}:',
            'solution': 'Solution {}:',
            'hints': 'Hints:',
            'no_hints': 'No obvious hints available'
        }
    }
    return texts.get(language, texts['de'])

def create_medium_hint_cell(title, puzzle, language='de', cell_size=0.8):
    """Erstellt eine mittelgroße Zelle mit Sudoku und horizontalen Hinweisen"""
    styles = getSampleStyleSheet()
    t = get_texts(language)
    
    # Hinweise generieren
    solver = SudokuSolver(puzzle)
    hints = solver.generate_hint_sequence()
    
    hints_text = ""
    if hints:
        all_hints = ", ".join(hints[:15])
        hints_text = f"<b>{t['hints']}</b> {all_hints}"
    else:
        hints_text = f"<b>{t['hints']}</b> {t['no_hints']}"
    
    hint_style = styles['Normal']
    hint_style.fontSize = 8
    hint_style.leading = 10
    hints_para = Paragraph(hints_text, hint_style)
    
    cell_data = [
        [Paragraph(title, styles['Heading3'])],
        [create_sudoku_table(puzzle, cell_size)],
        [hints_para]
    ]
    
    cell_table = Table(cell_data, colWidths=[15*cm], rowHeights=[0.8*cm, cell_size*9*cm + 0.8*cm, 1*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (2, 0), (2, 0), 'LEFT'),
    ]))
    
    return cell_table

def create_compact_hint_cell(title, puzzle, language='de', cell_size=0.35):
    """Erstellt eine kompakte Zelle mit Sudoku und Hinweisen für 2x2 Layout"""
    styles = getSampleStyleSheet()
    t = get_texts(language)
    
    # Hinweise generieren
    solver = SudokuSolver(puzzle)
    hints = solver.generate_hint_sequence()
    
    # Kompakte Hinweise (nur erste 4)
    hints_text = ""
    if hints:
        for i, hint in enumerate(hints[:4]):
            hints_text += f"• {hint}\n"
    else:
        hints_text = t['no_hints']
    
    hints_para = Paragraph(hints_text, styles['Normal'])
    
    cell_data = [
        [Paragraph(title, styles['Heading4'])],
        [create_sudoku_table(puzzle, cell_size)],
        [hints_para]
    ]
    
    cell_table = Table(cell_data, colWidths=[8*cm], rowHeights=[0.5*cm, 3.2*cm, 1.8*cm])
    cell_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (2, 0), (2, 0), 8),
    ]))
    
    return cell_table

def create_puzzle_with_hints_layout(puzzles_and_solutions, language='de'):
    """Erstellt 2-pro-Seite Layout für Rätsel mit horizontalen Hinweisen"""
    story = []
    t = get_texts(language)
    
    print("Erstelle Rätsel mit horizontalen Hinweisen (2 pro Seite)...")
    
    for i in range(0, len(puzzles_and_solutions), 2):
        page_puzzles = puzzles_and_solutions[i:i+2]
        
        if len(page_puzzles) >= 1:
            puzzle1, _ = page_puzzles[0]
            story.append(create_medium_hint_cell(t['puzzle'].format(i+1), puzzle1, language))
            story.append(Spacer(1, 0.8*cm))
        
        if len(page_puzzles) >= 2:
            puzzle2, _ = page_puzzles[1]
            story.append(create_medium_hint_cell(t['puzzle'].format(i+2), puzzle2, language))
        
        if i + 2 < len(puzzles_and_solutions):
            story.append(PageBreak())
    
    return story

def create_puzzle_grid_layout(puzzles_and_solutions, language='de'):
    """Erstellt 2-pro-Seite Layout für Rätsel ohne Hinweise"""
    story = []
    t = get_texts(language)
    
    print("Erstelle Rätsel ohne Hinweise (2 pro Seite)...")
    
    for i in range(0, len(puzzles_and_solutions), 2):
        page_puzzles = puzzles_and_solutions[i:i+2]
        
        if len(page_puzzles) >= 1:
            puzzle1, _ = page_puzzles[0]
            cell_data1 = [
                [Paragraph(t['puzzle'].format(i+1), getSampleStyleSheet()['Heading2'])],
                [Spacer(1, 0.5*cm)],
                [create_sudoku_table(puzzle1, 0.9)]
            ]
            
            table1 = Table(cell_data1, colWidths=[15*cm])
            table1.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(table1)
            story.append(Spacer(1, 1.5*cm))
        
        if len(page_puzzles) >= 2:
            puzzle2, _ = page_puzzles[1]
            cell_data2 = [
                [Paragraph(t['puzzle'].format(i+2), getSampleStyleSheet()['Heading2'])],
                [Spacer(1, 0.5*cm)],
                [create_sudoku_table(puzzle2, 0.9)]
            ]
            
            table2 = Table(cell_data2, colWidths=[15*cm])
            table2.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(table2)
        
        if i + 2 < len(puzzles_and_solutions):
            story.append(PageBreak())
    
    return story

def create_solution_grid_layout(puzzles_and_solutions, language='de'):
    """Erstellt 4x2 Grid Layout für optimale Seitennutzung (8 Lösungen pro Seite)"""
    story = []
    t = get_texts(language)
    
    print("Erstelle Lösungsseiten (8 pro Seite)...")
    
    for i in range(0, len(puzzles_and_solutions), 8):
        page_solutions = puzzles_and_solutions[i:i+8]
        
        solution_data = []
        
        # Erste Zeile (2 Lösungen)
        row1 = []
        if len(page_solutions) >= 1:
            _, solution1 = page_solutions[0]
            row1.append(create_titled_solution_cell(t['solution'].format(i+1), solution1, 0.42))
        else:
            row1.append("")
            
        if len(page_solutions) >= 2:
            _, solution2 = page_solutions[1]
            row1.append(create_titled_solution_cell(t['solution'].format(i+2), solution2, 0.42))
        else:
            row1.append("")
        
        solution_data.append(row1)
        
        # Zweite Zeile (2 Lösungen)
        if len(page_solutions) >= 3:
            row2 = []
            _, solution3 = page_solutions[2]
            row2.append(create_titled_solution_cell(t['solution'].format(i+3), solution3, 0.42))
            
            if len(page_solutions) >= 4:
                _, solution4 = page_solutions[3]
                row2.append(create_titled_solution_cell(t['solution'].format(i+4), solution4, 0.42))
            else:
                row2.append("")
            
            solution_data.append(row2)
        
        # Dritte Zeile (2 Lösungen)
        if len(page_solutions) >= 5:
            row3 = []
            _, solution5 = page_solutions[4]
            row3.append(create_titled_solution_cell(t['solution'].format(i+5), solution5, 0.42))
            
            if len(page_solutions) >= 6:
                _, solution6 = page_solutions[5]
                row3.append(create_titled_solution_cell(t['solution'].format(i+6), solution6, 0.42))
            else:
                row3.append("")
            
            solution_data.append(row3)
        
        # Vierte Zeile (2 Lösungen)
        if len(page_solutions) >= 7:
            row4 = []
            _, solution7 = page_solutions[6]
            row4.append(create_titled_solution_cell(t['solution'].format(i+7), solution7, 0.42))
            
            if len(page_solutions) >= 8:
                _, solution8 = page_solutions[7]
                row4.append(create_titled_solution_cell(t['solution'].format(i+8), solution8, 0.42))
            else:
                row4.append("")
            
            solution_data.append(row4)
        
        # Haupttabelle erstellen
        if solution_data:
            # Größere Zeilenhöhen für bessere Nutzung des Platzes
            if len(solution_data) == 1:
                row_heights = [15*cm]
            elif len(solution_data) == 2:
                row_heights = [7.5*cm, 7.5*cm]
            elif len(solution_data) == 3:
                row_heights = [6*cm, 6*cm, 6*cm]
            else:  # 4 Zeilen - optimiert für A4
                row_heights = [5.8*cm, 5.8*cm, 5.8*cm, 5.8*cm]
            
            main_solution_table = Table(solution_data, colWidths=[10.5*cm, 10.5*cm], rowHeights=row_heights)
            main_solution_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            story.append(main_solution_table)
        
        # Nur Seitenumbruch wenn noch mehr Lösungen kommen
        if i + 8 < len(puzzles_and_solutions):
            story.append(PageBreak())
    
    return story
