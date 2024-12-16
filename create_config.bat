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
    echo         "Key0, 1Key0, 2Key0": "y",
    echo         "Key1, 1Key1, 2Key1": "u",
    echo         "Key2, 1Key2, 2Key2": "i",
    echo         "Key3, 1Key3, 2Key3": "o",
    echo         "Key4, 1Key4, 2Key4": "p",
    echo         "Key5, 1Key5, 2Key5": "h",
    echo         "Key6, 1Key6, 2Key6": "j",
    echo         "Key7, 1Key7, 2Key7": "k",
    echo         "Key8, 1Key8, 2Key8": "l",
    echo         "Key9, 1Key9, 2Key9": ";",
    echo         "Key10, 1Key10, 2Key10": "n",
    echo         "Key11, 1Key11, 2Key11": "m",
    echo         "Key12, 1Key12, 2Key12": ",",
    echo         "Key13, 1Key13, 2Key13": ".",
    echo         "Key14, 1Key14, 2Key14": "/"
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
