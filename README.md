# Multilingual Sudoku Generator with GUI

Ein moderner Sudoku-Generator mit grafischer Benutzeroberfläche und Kommandozeilen-Interface, der mehrsprachige PDFs mit optionalen Hinweisen erstellt.

## 🌟 Features

### Neue GUI-Features
- **Grafische Benutzeroberfläche** für einfache Bedienung
- **Live-Vorschau** aller Einstellungen
- **Automatisches Speichern** der Konfiguration
- **Debug-Fenster** mit Live-Output
- **Sofortiges PDF-Öffnen** nach Generierung

### Kernfunktionen
- **Automatische Sudoku-Generierung** mit 6 Schwierigkeitsgraden
- **Vollständige Mehrsprachigkeit** (Deutsch/Englisch) für GUI und PDF
- **PDF-Export** mit professionellem Layout
- **Intelligente Hinweise** basierend auf Sudoku-Lösungsstrategien
- **Flexible Layouts**: 2 pro Seite (Rätsel) oder 6 pro Seite (Lösungen)

## 📋 Installation

### Voraussetzungen
```bash
pip install reportlab
```

### Setup
```bash
# Alle Python-Dateien in ein Verzeichnis kopieren
# Sicherstellen, dass alle Module im gleichen Ordner liegen

# Optional: Virtuelle Umgebung
python -m venv sudoku_env
source sudoku_env/bin/activate  # Linux/Mac
# sudoku_env\Scripts\activate   # Windows

pip install reportlab
```

## 🚀 Verwendung

### GUI-Version (Empfohlen)
```bash
python sudoku_gui.py
```

**GUI-Features:**
- 🎯 **Einfache Bedienung**: Alle Parameter per Mausklick
- 🔄 **Live-Updates**: Änderungen werden sofort gespeichert
- 🐛 **Debug-Fenster**: Detaillierte Informationen während Generierung
- 🌍 **Sprach-Umschaltung**: Sofortige GUI und PDF Übersetzung
- 📁 **Datei-Browser**: Einfache Auswahl des Ausgabepfads

### Kommandozeilen-Version
```bash
# Standard: 6 Rätsel, Level 3, Deutsch
python sudoku.py

# Mit Parametern
python sudoku.py --count 8 --level 4 --hintlist --lang en --output "puzzles.pdf"
```

### Parameter-Übersicht

| Parameter | GUI | CLI | Beschreibung | Standard |
|-----------|-----|-----|--------------|----------|
| Anzahl | Slider | `--count` | Anzahl Sudoku-Rätsel | 6 |
| Level | Slider | `--level` | Schwierigkeitsgrad (1-6) | 3 |
| Hinweise | Checkbox | `--hintlist` | Hinweise hinzufügen | Nein |
| Sprache | Dropdown | `--lang` | Sprache (de/en) | de |
| Ausgabe | Eingabe | `--output` | Dateiname | Auto |
| Debug | Checkbox | `--debug` | Debug-Modus | Ja (GUI) |

## 🌍 Mehrsprachigkeit

### Vollständige Übersetzung
- ✅ **GUI-Interface**: Alle Buttons, Labels, Dialoge
- ✅ **PDF-Inhalte**: Titel, Überschriften, Hinweise
- ✅ **Dateinamen**: Automatisch angepasst
- ✅ **Fehlermeldungen**: Konsistente Sprache

### Sprache wechseln
**GUI**: Dropdown-Menü → Sofortige Aktualisierung
**CLI**: `python sudoku.py --lang en`

### Unterstützte Sprachen
- 🇩🇪 **Deutsch**: Vollständig (Standard)
- 🇬🇧 **Englisch**: Vollständig

## 📁 Dateistruktur

```
sudoku-generator/
├── sudoku_gui.py         # GUI-Version (Hauptanwendung)
├── sudoku.py             # CLI-Version
├── main.py               # Alternative CLI
├── sudoku_core.py        # Sudoku-Generierung und -Lösung
├── pdf_generator.py      # PDF-Erstellung (Koordinator)
├── pdf_layouts.py        # PDF-Layout-Logik mit Sprache
├── pdf_tables.py         # Tabellen-Erstellung
├── translations.py       # Erweiterte Übersetzungen
├── config.json           # Automatisch: GUI-Konfiguration
└── README.md             # Diese Dokumentation
```

## 🎯 Verwendungsbeispiele

### GUI-Workflow
1. **Starten**: `python sudoku_gui.py`
2. **Einstellen**: Anzahl, Level, Optionen wählen
3. **Sprache**: Deutsch/Englisch umschalten
4. **Generieren**: "PDF Generieren" klicken
5. **Öffnen**: Automatische Nachfrage zum PDF öffnen

### Schnelle CLI-Kommandos
```bash
# Einfache deutsche Sudokus
python sudoku.py --count 4 --level 1

# Schwere englische Sudokus mit Hinweisen  
python sudoku.py --count 6 --level 5 --hintlist --lang en

# Batch für Sudoku-Club
python sudoku.py --count 20 --level 3 --output "club_sudokus.pdf"
```

## 🔧 Debug & Entwicklung

### GUI Debug-Fenster
- **Live-Output**: Generierungsfortschritt in Echtzeit
- **Error-Details**: Vollständige Fehlermeldungen
- **Performance**: Timing-Informationen pro Rätsel

### CLI Debug-Modus
```bash
python sudoku.py --debug --count 1
```

**Debug-Informationen:**
- Generierungs-Zeiten
- PDF-Erstellungs-Details
- Hinweis-Algorithmus-Output
- Memory-Usage

## 📊 Leistung & Limits

### Generierungszeiten (GUI)
- **Level 1-3**: 0.1-0.3s pro Rätsel
- **Level 4-5**: 0.2-0.5s pro Rätsel
- **Level 6**: 0.3-1.0s pro Rätsel

### Empfohlene Limits
- **Standard-Use**: 1-20 Rätsel
- **Batch-Generation**: 20-50 Rätsel
- **Maximum**: 100 Rätsel (GUI-Limit)

### PDF-Ausgabe
- **Dateigröße**: 100-500 KB je nach Anzahl
- **Layout**: 2 Rätsel pro Seite, 6 Lösungen pro Seite
- **Qualität**: 300 DPI, professionelles Layout

## 🛠️ Anpassungen & Erweiterungen

### Neue Sprache hinzufügen
```python
# In sudoku_gui.py: TEXTS erweitern
TEXTS['fr'] = {
    'title': 'Générateur Sudoku',
    'count': 'Nombre:',
    # ... weitere Übersetzungen
}

# In pdf_layouts.py: get_texts() erweitern
texts['fr'] = {
    'puzzle': 'Puzzle {}:',
    'solution': 'Solution {}:',
    # ...
}
```

### GUI-Theme anpassen
```python
# In sudoku_gui.py
style = ttk.Style()
style.theme_use('clam')  # oder 'vista', 'xpnative'
```

## 🚨 Troubleshooting

### Häufige Probleme

#### GUI startet nicht
```bash
# Python/Tkinter prüfen
python -c "import tkinter; print('GUI OK')"

# Fallback auf CLI
python sudoku.py
```

#### "ModuleNotFoundError: reportlab"
```bash
pip install reportlab
```

#### PDF immer in falscher Sprache
- **GUI**: Sprache in Dropdown ändern, neu generieren
- **CLI**: `--lang en` Parameter verwenden

#### Sehr langsame Level 6 Generierung
- **Normal**: Level 6 braucht länger (bis 1 Minute für 10 Rätsel)
- **Tipp**: Kleinere Batches verwenden

### Support
- **Debug-Fenster**: Zeigt detaillierte Fehlermeldungen
- **Config-Reset**: `config.json` löschen für Standard-Einstellungen

## 🎲 Schnellstart

### Für Anfänger
1. `python sudoku_gui.py` starten
2. Anzahl: 4, Level: 1, Hinweise: An
3. "PDF Generieren" klicken

### Für Experten  
1. CLI: `python sudoku.py --count 10 --level 6 --lang en`
2. Oder GUI mit Level 6, Debug an für Performance-Analyse

---

🎯 **Viel Spaß beim Sudoku-Generieren und -Lösen!** 🎯

*GUI-Version für beste Benutzerfreundlichkeit empfohlen.*
