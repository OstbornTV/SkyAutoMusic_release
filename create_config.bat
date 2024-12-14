@echo off
setlocal enabledelayedexpansion

REM Setze den Dateinamen für die Konfigurationsdatei
set "configFile=config.json"
set "backupFile=backup_config.json"

REM Überprüfen, ob die config.json bereits existiert und ein Backup erstellen
if exist "%configFile%" (
    copy "%configFile%" "%backupFile%"
)

REM Erstelle die JSON-Konfiguration
(
    echo {
    echo     "key_mapping": {
    echo         "Key0": "y", "Key1": "u", "Key2": "i", "Key3": "o", "Key4": "p",
    echo         "Key5": "h", "Key6": "j", "Key7": "k", "Key8": "l", "Key9": ";",
    echo         "Key10": "n", "Key11": "m", "Key12": ",", "Key13": ".", "Key14": "/"
    echo     },
    echo     "replacements": {
    echo         "A1": "y", "A2": "u", "A3": "i", "A4": "o", "A5": "p",
    echo         "B1": "h", "B2": "j", "B3": "k", "B4": "l", "B5": ";",
    echo         "C1": "n", "C2": "m", "C3": ",", "C4": ".", "C5": "/"
    echo     },
    echo     "speeds": {
    echo         "slow": 0.1,
    echo         "medium": 0.06,
    echo         "fast": 0.001
    echo     },
    echo     "long_press_duration": {
    echo         "slow": 0.348,
    echo         "medium": 0.248,
    echo         "fast": 0.148
    echo     },
    echo     "selected_language": null
    echo }
) > "%configFile%"

REM Überprüfen, ob die Datei erfolgreich erstellt wurde
if exist "%configFile%" (
    echo %configFile%
) else (
    echo Warning
)

endlocal
