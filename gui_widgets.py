# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from translations import t, get_translator

def create_title_section(parent):
    """Erstellt den Titel-Bereich"""
    title_frame = ttk.Frame(parent)
    title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
    
    title_label = ttk.Label(title_frame, text=t('app_title'), 
                           font=('Arial', 16, 'bold'))
    title_label.pack()
    
    subtitle_label = ttk.Label(title_frame, text=t('app_subtitle'), 
                              font=('Arial', 10))
    subtitle_label.pack()
    
    return title_frame

def create_count_section(parent, count_var, update_callback):
    """Erstellt den Anzahl-Kontrollbereich"""
    count_frame = ttk.LabelFrame(parent, text=t('count_section'), padding="10")
    count_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E), padx=(0, 0))
    
    count_scale = ttk.Scale(count_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
                           variable=count_var, command=update_callback)
    count_scale.pack(fill=tk.X, pady=(0, 5))
    
    count_label = ttk.Label(count_frame, text=t('puzzles_label', count_var.get()), 
                           font=('Arial', 12, 'bold'))
    count_label.pack()
    
    return count_frame, count_label

def create_level_section(parent, level_var):
    """Erstellt den Schwierigkeitsgrad-Bereich"""
    level_frame = ttk.LabelFrame(parent, text=t('level_section'), padding="10")
    level_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
    
    # Schwierigkeitsgrade mit Übersetzung
    levels = [
        (1, t('level_very_easy')),
        (2, t('level_easy')), 
        (3, t('level_medium')),
        (4, t('level_hard')),
        (5, t('level_very_hard')),
        (6, t('level_extreme'))
    ]
    
    for i, (value, text) in enumerate(levels):
        rb = ttk.Radiobutton(level_frame, text=t('level_format', value, text), 
                            variable=level_var, value=value)
        rb.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)
    
    return level_frame

def create_options_section(parent, hints_var):
    """Erstellt den Optionen-Bereich"""
    options_frame = ttk.LabelFrame(parent, text=t('options_section'), padding="10")
    options_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
    
    # Hints Checkbox
    hints_check = ttk.Checkbutton(options_frame, text=t('hints_option'), 
                                 variable=hints_var)
    hints_check.grid(row=0, column=0, sticky=tk.W, pady=2)
    
    return options_frame, hints_check

def create_language_section(parent, language_var, language_callback):
    """Erstellt den Sprach-Bereich"""
    language_frame = ttk.LabelFrame(parent, text=t('language_section'), padding="10")
    language_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
    
    # Sprach-Radiobuttons
    languages = [
        ('de', t('language_german')),
        ('en', t('language_english'))
    ]
    
    for i, (code, name) in enumerate(languages):
        rb = ttk.Radiobutton(language_frame, text=name, 
                            variable=language_var, value=code,
                            command=language_callback)
        rb.grid(row=0, column=i, sticky=tk.W, padx=10, pady=2)
    
    # Info-Text über Neustart
    restart_info = ttk.Label(language_frame, text=t('language_restart'), 
                            font=('Arial', 8), foreground='orange')
    restart_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
    
    return language_frame

def create_debug_section(parent, debug_var):
    """Erstellt einen separaten Debug-Bereich"""
    debug_frame = ttk.LabelFrame(parent, text=t('debug_section'), padding="10")
    debug_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
    
    # Debug Checkbox
    debug_check = ttk.Checkbutton(debug_frame, text=t('debug_option'), 
                                 variable=debug_var)
    debug_check.grid(row=0, column=0, sticky=tk.W, pady=2)
    
    # Info-Label für Debug
    debug_info = ttk.Label(debug_frame, text=t('debug_info'), 
                          font=('Arial', 8), foreground='gray')
    debug_info.grid(row=1, column=0, sticky=tk.W, padx=20, pady=(0, 5))
    
    return debug_frame, debug_check

def create_output_section(parent, output_var, browse_callback):
    """Erstellt den Ausgabedatei-Bereich"""
    output_frame = ttk.LabelFrame(parent, text=t('output_section'), padding="10")
    output_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
    output_frame.columnconfigure(0, weight=1)
    
    file_frame = ttk.Frame(output_frame)
    file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
    file_frame.columnconfigure(0, weight=1)
    
    output_entry = ttk.Entry(file_frame, textvariable=output_var, width=50)
    output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
    
    browse_btn = ttk.Button(file_frame, text=t('browse_button'), command=browse_callback)
    browse_btn.grid(row=0, column=1)
    
    info_label = ttk.Label(output_frame, text=t('output_info'), 
                          font=('Arial', 8), foreground='gray')
    info_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    return output_frame, output_entry

def create_control_section(parent, generate_callback):
    """Erstellt den Kontroll-Bereich mit Button und Progress"""
    control_frame = ttk.Frame(parent)
    control_frame.grid(row=7, column=0, columnspan=3, pady=20)
    
    generate_btn = ttk.Button(control_frame, text=t('generate_button'), 
                             command=generate_callback, 
                             style='Accent.TButton')
    generate_btn.pack(pady=(0, 10))
    
    progress = ttk.Progressbar(control_frame, mode='indeterminate')
    progress.pack(fill=tk.X, padx=20)
    
    return generate_btn, progress

def create_status_section(parent):
    """Erstellt den Status-Anzeigebereich"""
    status_frame = ttk.LabelFrame(parent, text=t('status_section'), padding="10")
    status_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
    status_frame.columnconfigure(0, weight=1)
    status_frame.rowconfigure(0, weight=1)
    
    # Text widget mit Scrollbar
    text_frame = ttk.Frame(status_frame)
    text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)
    
    status_text = tk.Text(text_frame, height=10, wrap=tk.WORD, 
                         font=('Consolas', 9), state=tk.DISABLED)
    status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=status_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    status_text.configure(yscrollcommand=scrollbar.set)
    
    return text_frame, status_text

def update_all_texts():
    """Aktualisiert alle Texte nach Sprachwechsel (für zukünftige Implementierung)"""
    # Diese Funktion könnte später verwendet werden, um alle Texte
    # zu aktualisieren ohne Neustart
    pass
