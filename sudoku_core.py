# -*- coding: utf-8 -*-
import random
import copy
import time

# Translations import mit Fallback
try:
    from translations import t, get_current_language
    TRANSLATIONS_AVAILABLE = True
except ImportError:
    TRANSLATIONS_AVAILABLE = False
    # Fallback-Funktion
    def t(key, *args, **kwargs):
        fallback_texts = {
            'debug_generator_init': 'SudokuGenerator initialisiert',
            'debug_grid_fill_start': 'Beginne Grid-Füllung...',
            'debug_grid_fill_complete': 'Grid-Füllung abgeschlossen in {:.2f}s',
            'debug_remove_numbers': 'Entferne {} Zahlen für Level {}',
            'debug_puzzle_generated': 'Rätsel generiert: {} Zellen entfernt',
            'debug_solver_init': 'SudokuSolver initialisiert',
            'debug_finding_singles': 'Suche nach Naked Singles...',
            'debug_found_singles': 'Gefunden: {} Naked Singles',
            'debug_hint_generation': 'Generiere Hinweise...',
            'debug_hints_generated': '{} Hinweise generiert',
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

def set_debug_mode(debug_mode):
    """Setzt den Debug-Modus für dieses Modul"""
    global DEBUG_MODE
    DEBUG_MODE = debug_mode
    debug_print("Debug mode set for sudoku_core module")

class SudokuGenerator:
    def __init__(self, debug_mode=False):
        global DEBUG_MODE
        DEBUG_MODE = debug_mode
        
        self.size = 9
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        debug_print(t('debug_generator_init'))
        debug_print(f"Grid size: {self.size}x{self.size}")
        
    def is_valid(self, grid, row, col, num):
        """Prüft ob eine Zahl an der Position gültig ist"""
        # Prüfe Reihe
        for x in range(9):
            if grid[row][x] == num:
                debug_print(f"Number {num} already in row {row}")
                return False
        
        # Prüfe Spalte
        for x in range(9):
            if grid[x][col] == num:
                debug_print(f"Number {num} already in column {col}")
                return False
        
        # Prüfe 3x3 Box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    debug_print(f"Number {num} already in 3x3 box at ({start_row}, {start_col})")
                    return False
        
        return True
    
    def fill_grid(self):
        """Füllt das Grid mit einer gültigen Sudoku-Lösung"""
        start_time = time.time()
        debug_print(t('debug_grid_fill_start'))
        
        fill_result = self._fill_grid_recursive()
        
        end_time = time.time()
        debug_print(t('debug_grid_fill_complete', end_time - start_time))
        
        return fill_result
    
    def _fill_grid_recursive(self):
        """Rekursive Hilfsfunktion für Grid-Füllung"""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    debug_print(f"Trying to fill cell ({i}, {j}) with numbers: {numbers}")
                    
                    for num in numbers:
                        if self.is_valid(self.grid, i, j, num):
                            self.grid[i][j] = num
                            debug_print(f"Placed {num} at ({i}, {j})")
                            
                            if self._fill_grid_recursive():
                                return True
                            
                            debug_print(f"Backtracking from ({i}, {j}), removing {num}")
                            self.grid[i][j] = 0
                    
                    debug_print(f"No valid number found for ({i}, {j})")
                    return False
        return True
    
    def remove_numbers(self, level):
        """Entfernt Zahlen basierend auf dem Schwierigkeitsgrad"""
        cells_to_remove = {
            1: 35,  # Sehr einfach
            2: 40,  # Einfach
            3: 45,  # Mittel
            4: 50,  # Schwer
            5: 55,  # Sehr schwer
            6: 60   # Extrem schwer
        }
        
        target_removals = cells_to_remove[level]
        debug_print(t('debug_remove_numbers', target_removals, level))
        
        puzzle = copy.deepcopy(self.grid)
        cells_removed = 0
        attempts = 0
        max_attempts = 500
        
        debug_print(f"Starting removal process: target={target_removals}, max_attempts={max_attempts}")
        
        while cells_removed < target_removals and attempts < max_attempts:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if puzzle[row][col] != 0:
                original_value = puzzle[row][col]
                puzzle[row][col] = 0
                cells_removed += 1
                
                debug_print(f"Removed {original_value} from ({row}, {col}) - Total removed: {cells_removed}")
                
            attempts += 1
        
        debug_print(t('debug_puzzle_generated', cells_removed))
        debug_print(f"Removal completed after {attempts} attempts")
        
        if cells_removed < target_removals:
            debug_print(f"WARNING: Only removed {cells_removed} cells instead of {target_removals}")
        
        return puzzle
    
    def generate_puzzle(self, level):
        """Generiert ein Sudoku-Puzzle mit gegebenem Schwierigkeitsgrad"""
        start_time = time.time()
        debug_print(f"Starting puzzle generation for level {level}")
        
        # Grid zurücksetzen
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        debug_print("Grid reset")
        
        # Grid füllen
        if not self.fill_grid():
            debug_print("ERROR: Failed to fill grid")
            raise Exception("Failed to generate valid Sudoku grid")
        
        solution = copy.deepcopy(self.grid)
        debug_print("Solution grid created")
        
        # Zahlen entfernen
        puzzle = self.remove_numbers(level)
        
        end_time = time.time()
        debug_print(f"Puzzle generation completed in {end_time - start_time:.2f}s")
        
        # Validierung
        if DEBUG_MODE:
            self._validate_puzzle(puzzle, solution)
        
        return puzzle, solution
    
    def _validate_puzzle(self, puzzle, solution):
        """Validiert das generierte Puzzle (nur im Debug-Modus)"""
        debug_print("Validating generated puzzle...")
        
        # Zähle leere Zellen
        empty_cells = sum(row.count(0) for row in puzzle)
        filled_cells = 81 - empty_cells
        
        debug_print(f"Puzzle validation: {filled_cells} filled cells, {empty_cells} empty cells")
        
        # Prüfe ob alle gefüllten Zellen korrekt sind
        errors = 0
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    if puzzle[i][j] != solution[i][j]:
                        debug_print(f"ERROR: Mismatch at ({i}, {j}): puzzle={puzzle[i][j]}, solution={solution[i][j]}")
                        errors += 1
        
        if errors == 0:
            debug_print("Puzzle validation: PASSED")
        else:
            debug_print(f"Puzzle validation: FAILED with {errors} errors")

class SudokuSolver:
    def __init__(self, puzzle, debug_mode=False):
        global DEBUG_MODE
        DEBUG_MODE = debug_mode
        
        self.puzzle = copy.deepcopy(puzzle)
        
        debug_print(t('debug_solver_init'))
        debug_print(f"Puzzle loaded with {self._count_empty_cells()} empty cells")
        
    def _count_empty_cells(self):
        """Zählt leere Zellen im Puzzle"""
        return sum(row.count(0) for row in self.puzzle)
        
    def get_possible_numbers(self, row, col):
        """Gibt alle möglichen Zahlen für eine Zelle zurück"""
        if self.puzzle[row][col] != 0:
            debug_print(f"Cell ({row}, {col}) already filled with {self.puzzle[row][col]}")
            return []
        
        possible = set(range(1, 10))
        
        # Entferne Zahlen aus der Reihe
        for c in range(9):
            if self.puzzle[row][c] in possible:
                possible.remove(self.puzzle[row][c])
        
        # Entferne Zahlen aus der Spalte
        for r in range(9):
            if self.puzzle[r][col] in possible:
                possible.remove(self.puzzle[r][col])
        
        # Entferne Zahlen aus der 3x3 Box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.puzzle[r][c] in possible:
                    possible.remove(self.puzzle[r][c])
        
        possible_list = list(possible)
        debug_print(f"Possible numbers for ({row}, {col}): {possible_list}")
        
        return possible_list
    
    def find_naked_singles(self):
        """Findet Zellen mit nur einer möglichen Zahl"""
        debug_print(t('debug_finding_singles'))
        
        singles = []
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    possible = self.get_possible_numbers(row, col)
                    if len(possible) == 1:
                        singles.append((row, col, possible[0]))
                        debug_print(f"Naked single found: R{row+1}C{col+1}={possible[0]}")
        
        debug_print(t('debug_found_singles', len(singles)))
        return singles
    
    def generate_hint_sequence(self, max_hints=15):
        """Generiert eine Sequenz von logischen Hinweisen"""
        debug_print(t('debug_hint_generation'))
        
        hints = []
        working_puzzle = copy.deepcopy(self.puzzle)
        hint_count = 0
        
        for iteration in range(max_hints):
            debug_print(f"Hint generation iteration {iteration + 1}")
            
            solver = SudokuSolver(working_puzzle, DEBUG_MODE)
            naked_singles = solver.find_naked_singles()
            
            if naked_singles:
                hint = naked_singles[0]  # Nimm den ersten gefundenen Single
                row, col, num = hint
                
                # Formatiere Hinweis sprachabhängig
                current_lang = get_current_language()
                if current_lang == 'en':
                    hint_text = f"R{row+1}C{col+1}={num}"
                else:
                    hint_text = f"R{row+1}C{col+1}={num}"
                
                hints.append(hint_text)
                working_puzzle[row][col] = num
                hint_count += 1
                
                debug_print(f"Hint {hint_count}: {hint_text}")
            else:
                debug_print("No more naked singles found")
                break
        
        debug_print(t('debug_hints_generated', len(hints)))
        
        # Erweiterte Hinweise für schwerere Rätsel
        if len(hints) < 3 and DEBUG_MODE:
            debug_print("Few hints found, puzzle might be difficult")
            # Hier könnten erweiterte Strategien implementiert werden
        
        return hints
    
    def get_difficulty_assessment(self):
        """Bewertet die Schwierigkeit des Puzzles basierend auf verfügbaren Hinweisen"""
        hints = self.generate_hint_sequence(5)  # Teste nur erste 5 Hinweise
        
        if len(hints) >= 4:
            difficulty = "Easy"
        elif len(hints) >= 2:
            difficulty = "Medium"
        else:
            difficulty = "Hard"
        
        debug_print(f"Difficulty assessment: {difficulty} ({len(hints)} easy hints found)")
        return difficulty, len(hints)
