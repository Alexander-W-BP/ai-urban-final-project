import pandas as pd
import os
import csv
from io import StringIO
import re # Modul für reguläre Ausdrücke (optional, aber hilfreich)

# --- Konfiguration ---
# Der von Ihnen bereitgestellte absolute Pfad zur Actions-Datei
ACTIONS_FILE = r"C:\Studium_TU_Darmstadt\Master\3. Semester (Auslandssemester - Soul)\AI in Urban Planning and Design\ai-urban-final-project\data\raw\actions.csv"
OUTPUT_FILE = "formatted_city_dates_skeleton.csv"  # Name der Ausgabedatei
# Das Ziel-Schema, das die neue CSV-Datei haben soll
TARGET_COLUMNS = [
    "City_ID",
    "Country",
    "Region_Code",
    "Climate_Zone",
    "Date",
    "Population_2025_Mio",
    "Median_Age_Years",
    "GDP_Billion_USD",
    "GDP_per_Capita_USD"
]
# Benötigte Spalten für die Extraktion
REQUIRED_COLUMNS_FROM_SOURCE = ['City_ID', 'Start Date (Date)']
EXPECTED_NUM_COLUMNS = 9 # Anzahl der Spalten im Header der Quelldatei
# ---------------------

def create_formatted_skeleton_csv(actions_file, output_file, target_columns):
    """
    Liest die Aktions-CSV Zeile für Zeile, identifiziert und meldet Fehler 
    in der Struktur (falsche Spaltenanzahl), rettet die benötigten Daten 
    (City_ID, Date) und extrahiert die gültigen Datensätze.
    """
    actions_file_display = os.path.normpath(actions_file)
    print(f"Starte Verarbeitung der Datei: {actions_file_display}")
    
    valid_records = []
    error_count = 0
    total_lines_read = 0

    # 1. Datei Zeile für Zeile einlesen und Fehler protokollieren/retten
    try:
        with open(actions_file, 'r', encoding='utf-8') as f:
            # Der Trenner MUSS ein Komma sein, basierend auf dem Fehler
            delimiter = ','
            
            # Initialisiere den CSV-Reader (lesen wir ohne den "automatischen" reader)
            file_content = f.read().splitlines()
            
            if not file_content:
                print("FEHLER: Die Datei ist leer.")
                return

            header = file_content[0].split(delimiter)
            total_lines_read = 1
            
            # Finde die Indizes der benötigten Spalten
            try:
                city_id_index = header.index('City_ID')
                date_index = header.index('Start Date (Date)')
            except ValueError as e:
                print(f"FEHLER: Die benötigte Spalte '{e.args[0].split()[1]}' fehlt im Header.")
                return

            # Durchlaufe alle Datenzeilen (ab Zeile 1)
            for line in file_content[1:]:
                total_lines_read += 1
                row = line.split(delimiter)
                
                # Wenn die Zeile die erwartete Spaltenanzahl hat, verarbeite sie normal
                if len(row) == EXPECTED_NUM_COLUMNS:
                    try:
                        city_id = row[city_id_index]
                        date = row[date_index]
                        valid_records.append({'City_ID': city_id, 'Date': date})
                    except IndexError:
                        # Sollte nicht passieren, wenn len(row) korrekt ist
                        print(f"UNERWARTETER FEHLER in Zeile {total_lines_read}: Konnte die Spalten nicht extrahieren.")
                        error_count += 1
                
                # Wenn die Zeile eine falsche Spaltenanzahl hat (der Fehlerfall)
                else:
                    error_count += 1
                    
                    # --- RETTUNG DER DATEN (City_ID und Date) ---
                    
                    # 1. Protokollierung des Fehlers
                    print("\n--- STRUKTURFEHLER GEFUNDEN ---")
                    print(f"❌ Zeile: {total_lines_read}")
                    print(f"❌ Gefundene Spalten: {len(row)}, Erwartet: {EXPECTED_NUM_COLUMNS}")
                    print(f"❌ Fehlerhafte Zeile: {line}")
                    print("HINWEIS: Manuelle Rettung von City_ID und Date wird versucht...")

                    # 2. Versuch, City_ID (Feld 1) und Start Date (Feld 4) zu extrahieren.
                    # City_ID ist das erste Feld, Date ist das vierte Feld.
                    # WICHTIG: Wir müssen die Indizes aus dem gesplitteten 'row' verwenden.
                    # Index 0 = City_ID
                    # Index 3 = Start Date (Date)
                    
                    try:
                        city_id_rescued = row[0] # Das erste Feld ist in 99% der Fälle korrekt
                        date_rescued = row[3] # Das vierte Feld ist das Start Date
                        
                        valid_records.append({'City_ID': city_id_rescued, 'Date': date_rescued})
                        print(f"✅ Gerettet! City_ID: {city_id_rescued}, Date: {date_rescued}")
                    
                    except IndexError:
                        print(f"❌ KRITISCHER FEHLER: Konnte City_ID und Date aus Zeile {total_lines_read} nicht retten.")
                        
                    print("-----------------------------")


    except FileNotFoundError:
        print(f"FEHLER: Die Datei unter dem Pfad '{actions_file_display}' wurde nicht gefunden.")
        return
    except Exception as e:
        print(f"Ein kritischer Fehler ist beim Initialisieren aufgetreten: {e}")
        return

    # 2. Daten in DataFrame laden und weiterverarbeiten
    if not valid_records:
        print("Keine gültigen Datensätze gefunden. Skript beendet.")
        return

    df_actions = pd.DataFrame(valid_records)

    # 3. Duplikate entfernen (Dedublizierung)
    # Die Date-Spalte ist bereits korrekt benannt ('Date')
    df_deduplicated = df_actions.drop_duplicates()

    # 4. Daten in das Ziel-Schema bringen
    df_final = df_deduplicated.reindex(columns=target_columns)

    # 5. Speichern der formatierten Daten
    output_file_display = os.path.abspath(output_file)
    df_final.to_csv(output_file, index=False, na_rep="") 

    print("\n\n--- ZUSAMMENFASSUNG DER VERARBEITUNG ---")
    print(f"✅ Erfolg! Die neue Datei (im Ziel-Schema) wurde unter '{output_file_display}' gespeichert.")
    print(f"Gesamtzeilen (inkl. Header) in der Quelldatei: {total_lines_read}")
    print(f"⚠️ Strukturfehler gefunden und Daten gerettet: {error_count}")
    print(f"Zeilenanzahl in der Ausgabe nach Dedublizierung: {len(df_final)}")
    print("---------------------------------------")


# Hauptausführung des Skripts
if __name__ == "__main__":
    create_formatted_skeleton_csv(ACTIONS_FILE, OUTPUT_FILE, TARGET_COLUMNS)