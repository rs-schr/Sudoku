# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from pdf_layouts import create_puzzle_with_hints_layout, create_puzzle_grid_layout, create_solution_grid_layout

def create_pdf(puzzles_and_solutions, filename, level, hintlist=False, language='de'):
    """Erstellt eine PDF mit mehreren Sudoku-Rätseln"""
    try:
        print(f"Erstelle PDF: {filename} (Sprache: {language})")
        doc = SimpleDocTemplate(filename, pagesize=A4)  # Hier war der Fehler!
        styles = getSampleStyleSheet()
        story = []
        
        # Übersetzungen
        texts = {
            'de': {
                'title': 'Sudoku Rätsel (Level {}) - {}',
                'levels': {1: 'Sehr Einfach', 2: 'Einfach', 3: 'Mittel', 4: 'Schwer', 5: 'Sehr Schwer', 6: 'Extrem Schwer'}
            },
            'en': {
                'title': 'Sudoku Puzzles (Level {}) - {}',
                'levels': {1: 'Very Easy', 2: 'Easy', 3: 'Medium', 4: 'Hard', 5: 'Very Hard', 6: 'Extremely Hard'}
            }
        }
        
        t = texts.get(language, texts['de'])
        level_desc = t['levels'].get(level, 'Unknown')
        
        # Titel
        title = Paragraph(t['title'].format(level, level_desc), styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Rätsel-Seiten
        if hintlist:
            story.extend(create_puzzle_with_hints_layout(puzzles_and_solutions, language))
        else:
            story.extend(create_puzzle_grid_layout(puzzles_and_solutions, language))
        
        # Lösungsseiten (OHNE Überschrift!)
        story.append(PageBreak())
        story.extend(create_solution_grid_layout(puzzles_and_solutions, language))
        
        doc.build(story)
        print(f"PDF erfolgreich erstellt: {filename}")
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        raise
