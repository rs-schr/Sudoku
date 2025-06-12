# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

def setup_window_style(root):
    """Konfiguriert Window-Style und Theme"""
    style = ttk.Style()
    
    # Try to use modern theme
    try:
        style.theme_use('winnative')  # Windows
    except:
        try:
            style.theme_use('aqua')  # macOS
        except:
            style.theme_use('clam')  # Linux/fallback
    
    return style

def center_window(root):
    """Zentriert das Fenster auf dem Bildschirm"""
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

def validate_count_input(value):
    """Validiert Anzahl-Eingabe"""
    try:
        count = int(value)
        return 1 <= count <= 100
    except (ValueError, TypeError):
        return False

def format_status_message(message_type, message):
    """Formatiert Status-Nachrichten mit Icons"""
    icons = {
        'info': '📄',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'process': '🔄'
    }
    
    icon = icons.get(message_type, '📄')
    return f"{icon} {message}"
