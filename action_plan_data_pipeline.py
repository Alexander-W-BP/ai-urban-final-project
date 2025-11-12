import anthropic
import pandas as pd
import os
import time
import io

# --- KONFIGURATION ---
# Ersetzen Sie dies durch den PFAD zu Ihrer cities.csv
INPUT_FILE_PATH = r"C:\Studium_TU_Darmstadt\Master\3. Semester (Auslandssemester - Soul)\AI in Urban Planning and Design\ai-urban-final-project\data\raw\cities.csv" 
OUTPUT_FILE_NAME = "actions.csv"

# Die erforderlichen Spalten für die Ausgabe-CSV
OUTPUT_COLUMNS = [
    "City_ID", 
    "Action_Name", 
    "Action_ID", 
    "Start Date (Date)", 
    "End Date (Date)", 
    "Costs (Number)", 
    "Scope (String)", 
    "Measure (Label)", 
    "Short Description (Text)"
]

# Die neun spezifischen Maßnahmen (als Teil des Prompts)
MEASURES = [
    "1. Expansion of Pedestrian Paths",
    "2. Expansion of Bicycle Paths",
    "3. Expansion of Public Local Transport",
    "4. Expansion of Public Long-Distance Transport",
    "5. Alternative Drive Systems and Sharing Offers",
    "6. Intelligent Traffic Control",
    "7. Energy-efficient Building Refurbishment",
    "8. Green Infrastructure (Carbon Sinks)",
    "9. Sustainable Land Management (Avoidance of Urban Sprawl)"
]

# --- HILFSFUNKTIONEN ---

def create_initial_actions_file():
    """Erstellt die actions.csv mit den Headern, falls sie noch nicht existiert."""
    if not os.path.exists(OUTPUT_FILE_NAME):
        # CSV-Header mit Komma-Trenner
        header_line = ",".join(OUTPUT_COLUMNS) + "\n"
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(header_line)
        print(f"✅ Ausgabedatei '{OUTPUT_FILE_NAME}' mit Headern erstellt.")
    else:
        print(f"✅ Ausgabedatei '{OUTPUT_FILE_NAME}' existiert bereits. Wird fortgesetzt.")


def generate_prompt(city_name: str) -> str:
    """Erstellt den Claude-Prompt mit dynamischem Stadtnamen."""
    measures_list = "\n".join(MEASURES)
    
    # Der Text ist fast identisch mit Ihrer Anforderung, der City_ID-Platzhalter wird ersetzt.
    prompt = f"""
    List and briefly describe all implemented urban climate protection measures in {city_name} before 2024 related to transport, buildings, and green infrastructure, focusing on the following nine measures:
    {measures_list}
    
    CRITICAL: Present the results ONLY as pure CSV data with NO additional text, explanations, or notes before or after the CSV.
    
    Output format requirements:
    - Start directly with the CSV header line
    - Follow with data rows only
    - Use comma (,) as delimiter
    - Ensure entire output is in English
    - Do NOT include any explanatory text, notes, or commentary
    - Do NOT use markdown code blocks or formatting
    
    The CSV must contain exactly these columns in this order:
    
    City_ID: Use the full city name '{city_name}' for every entry.
    Action_Name: A concise, descriptive English name for the action (e.g., 'Metro LCOI Start').
    Action_ID: A short identifier (e.g., 'A01', 'A02', 'A03').
    Start Date (Date): The year and month when the measure was initiated (e.g., '2007/01').
    End Date (Date): The year and month when the measure was fully executed / finished (e.g. '2025/01', 'Ongoing').
    Costs (Number): Use 'N/A' for all entries.
    Scope (String): Categorize as 'Pilot', 'Medium (District/Corridor)', or 'City-wide'.
    Measure (Label): Must exactly match one of the nine specified measures listed above.
    Short Description (Text): A concise English summary without citation markers like [1], [2].
    
    Output ONLY the CSV data starting with the header line. No other text.
    """
    return prompt.strip()


def query_claude(client: anthropic.Anthropic, prompt: str) -> str:
    """Sendet die Anfrage an Claude mit aktiviertem Web Search Tool."""
    
    # Definition des Web Search Tools (wie von Anthropic bereitgestellt)
    web_search_tool = {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5 
    }
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",  # ✅ AKTUALISIERTES MODELL
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ],
            tools=[web_search_tool]  # Aktiviert die Websuche
        )
        
        # Die Antwort besteht aus einem oder mehreren Textblöcken
        full_text = ""
        for block in response.content:
            if block.type == "text":
                full_text += block.text
        
        return full_text
    
    except Exception as e:
        print(f"‼️ Fehler bei der Claude API Anfrage: {e}")
        return ""


def append_data_to_csv(csv_string: str):
    """
    Nimmt den CSV-String von Claude, extrahiert nur die CSV-Datenzeilen
    und hängt sie an die actions.csv an.
    """
    if not csv_string:
        return
    
    # Entferne Markdown-Code-Blöcke falls vorhanden
    csv_string = csv_string.replace("```csv", "").replace("```", "")
    
    # Teile den String in Zeilen
    lines = csv_string.strip().split('\n')
    
    # Finde alle gültigen CSV-Zeilen (die mit dem erwarteten Format übereinstimmen)
    valid_data_lines = []
    header_found = False
    
    for line in lines:
        line = line.strip()
        
        # Überspringe leere Zeilen
        if not line:
            continue
            
        # Erkenne den Header (beginnt mit "City_ID")
        if line.lower().startswith("city_id"):
            header_found = True
            continue  # Header überspringen
        
        # Wenn Header gefunden wurde, sammle alle Zeilen die Kommas enthalten
        # und mindestens 9 Felder haben (unsere 9 Spalten)
        if header_found:
            # Prüfe ob die Zeile mindestens 8 Kommas hat (= 9 Felder)
            if line.count(',') >= 8:
                valid_data_lines.append(line)
        # Falls kein Header gefunden wurde, aber Zeile viele Kommas hat
        elif line.count(',') >= 8 and not any(x in line.lower() for x in ['note:', 'important:', '**', 'however', 'missing', 'limited']):
            valid_data_lines.append(line)
    
    if not valid_data_lines:
        print("    ➡️ Keine gültigen CSV-Datenzeilen zum Anhängen gefunden.")
        print(f"    📄 Claude Antwort (erste 500 Zeichen):\n{csv_string[:500]}")
        return

    # Füge die Zeilen an die Ausgabedatei an
    with open(OUTPUT_FILE_NAME, 'a', encoding='utf-8') as f:
        f.write("\n" + "\n".join(valid_data_lines))
        
    print(f"    ✅ {len(valid_data_lines)} Zeilen erfolgreich an '{OUTPUT_FILE_NAME}' angehängt.")


# --- HAUPT-PIPELINE ---

def main():
    """Die Hauptfunktion der Daten-Pipeline."""
    
    # 1. API-Client initialisieren
    # Liest ANTHROPIC_API_KEY automatisch aus der Umgebungsvariable
    try:
        client = anthropic.Anthropic()
    except Exception as e:
        print(f"‼️ FEHLER: Stellen Sie sicher, dass die Umgebungsvariable ANTHROPIC_API_KEY gesetzt ist.")
        print(e)
        return

    # 2. Input-Daten laden
    try:
        cities_df = pd.read_csv(INPUT_FILE_PATH)
        cities_to_process = cities_df['Stadt_ID'].unique()
    except FileNotFoundError:
        print(f"‼️ FEHLER: Eingabedatei nicht gefunden unter: {INPUT_FILE_PATH}")
        return
    except KeyError:
        print("‼️ FEHLER: Die Spalte 'Stadt_ID' wurde in der cities.csv nicht gefunden.")
        return

    print(f"Starte Verarbeitung für {len(cities_to_process)} Städte.")
    print("-" * 30)

    # 3. Output-Datei vorbereiten
    create_initial_actions_file()

    # 4. Städte iterieren und API aufrufen
    for i, city in enumerate(cities_to_process):
        print(f"[{i+1}/{len(cities_to_process)}] Verarbeite Stadt: {city}...")
        
        # A) Prompt generieren
        city_prompt = generate_prompt(city)
        
        # B) Claude abfragen
        claude_csv_output = query_claude(client, city_prompt)
        
        # C) Ergebnisse anhängen
        if claude_csv_output:
            append_data_to_csv(claude_csv_output)
        else:
            print(f"    ➡️ Keine verwertbare Antwort für {city} erhalten.")
            
        # Optional: Eine kurze Pause, um Rate Limits zu vermeiden
        time.sleep(5) 
        
        print("-" * 30)


if __name__ == "__main__":
    main()