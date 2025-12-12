import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# --- KONFIGURATION ---
LOCAL_DATA_FILE = "C:\\Studium_TU_Darmstadt\\Master\\3. Semester (Auslandssemester - Soul)\\AI in Urban Planning and Design\\ai-urban-final-project\\data\\temperature\\shanghai_2000_2025.csv"  # Ihre lokalen TÄGLICHEN Daten (date, tavg, ...)
GLOBAL_DATA_FILE = "C:\\Studium_TU_Darmstadt\\Master\\3. Semester (Auslandssemester - Soul)\\AI in Urban Planning and Design\\ai-urban-final-project\\data\\temperature\\global_temperature_2000_2024.csv"  # Ihre jährlichen GLOBALEN Anomalie-Daten (Year, Anomaly)
TEMP_COLUMN = (
    "tavg"  # Spalte mit der täglichen Durchschnittstemperatur in der lokalen Datei
)

# Basisperiode, auf die sich die lokale Anomalie beziehen soll.
# Idealerweise sollte diese mit der globalen Basis (1901-2000) übereinstimmen.
# Da Ihre lokalen Daten vielleicht nicht bis 1901 zurückreichen, verwenden wir
# den Standard, aber falls die lokalen Daten nur ab 2000 starten, berechnen wir
# die lokale Basis relativ zum Mittelwert des verfügbaren lokalen Zeitraums.
LOCAL_BASELINE_START = 1901
LOCAL_BASELINE_END = 2000


# --- FUNKTION ZUM LADEN UND BERECHNEN DER SHANGHAI-ANOMALIE ---
def calculate_shanghai_anomaly(file_path):
    """Lädt die lokalen TAGESDATEN, aggregiert sie jährlich und berechnet die Anomalie."""
    try:
        # 1. Daten laden und Datum verarbeiten
        df = pd.read_csv(file_path, sep=",")
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")

        # 2. Daten bereinigen und zu numerisch konvertieren
        df[TEMP_COLUMN] = pd.to_numeric(df[TEMP_COLUMN], errors="coerce")
        df = df.dropna(subset=[TEMP_COLUMN])

        # 3. Jährlichen Durchschnitt berechnen
        df_yearly = (
            df[TEMP_COLUMN].resample("Y").mean().to_frame(name="Shanghai_Avg_Temp")
        )
        df_yearly["Year"] = df_yearly.index.year

        # 4. Lokalen Basiswert (Mittelwert) berechnen
        baseline_data = df_yearly[
            (df_yearly["Year"] >= LOCAL_BASELINE_START)
            & (df_yearly["Year"] <= LOCAL_BASELINE_END)
        ]

        if baseline_data.empty:
            # Falls die lokalen Daten die gesamte Basisperiode nicht abdecken,
            # verwenden wir den Durchschnitt aller verfügbaren lokalen Jahre als Basis.
            local_baseline = df_yearly["Shanghai_Avg_Temp"].mean()
            print(
                f"WARNUNG: Lokale Daten decken {LOCAL_BASELINE_START}-{LOCAL_BASELINE_END} nicht ab."
            )
            print(
                f"-> Lokaler Basiswert: Durchschnitt aller verfügbaren Jahre ({df_yearly['Year'].min()}-{df_yearly['Year'].max()}) = {local_baseline:.2f}°C"
            )
        else:
            local_baseline = baseline_data["Shanghai_Avg_Temp"].mean()
            print(
                f"Lokaler Basiswert (basierend auf {LOCAL_BASELINE_START}-{LOCAL_BASELINE_END}): {local_baseline:.2f}°C"
            )

        # 5. Anomalie berechnen
        df_yearly["Shanghai_Anomaly_C"] = (
            df_yearly["Shanghai_Avg_Temp"] - local_baseline
        )

        return df_yearly

    except FileNotFoundError:
        print(
            f"FEHLER: Lokale Datei '{LOCAL_DATA_FILE}' nicht gefunden. Bitte speichern Sie Ihre Shanghai-Daten dort."
        )
        return None
    except Exception as e:
        print(
            f"Ein unerwarteter Fehler beim Verarbeiten der lokalen Daten ist aufgetreten: {e}"
        )
        return None


# --- FUNKTION ZUM LADEN DER GLOBALEN ANOMALIE-DATEN ---
def load_global_anomaly_data(file_path):
    """Lädt die GLOBALEN JAHRES-ANOMALIE-DATEN."""
    try:
        # Laden der globalen Anomalie-Daten
        df_global = pd.read_csv(file_path, sep=",")
        df_global = df_global.rename(columns={"Anomaly": "Global_Anomaly_C"})

        # Überprüfung der Spalten
        if (
            "Year" not in df_global.columns
            or "Global_Anomaly_C" not in df_global.columns
        ):
            print(
                "FEHLER: Die globale Datei muss die Spalten 'Year' und 'Anomaly' enthalten."
            )
            return None

        # Nur relevante Spalten behalten
        df_global = df_global[["Year", "Global_Anomaly_C"]].set_index("Year")
        print(
            f"Globale Daten von {df_global.index.min()} bis {df_global.index.max()} geladen."
        )
        return df_global

    except FileNotFoundError:
        print(
            f"FEHLER: Globale Datei '{GLOBAL_DATA_FILE}' nicht gefunden. Bitte speichern Sie Ihre Anomalie-Daten dort."
        )
        return None
    except Exception as e:
        print(
            f"Ein unerwarteter Fehler beim Verarbeiten der globalen Daten ist aufgetreten: {e}"
        )
        return None


# --- HAUPTPROGRAMM ---

# 1. Daten laden und verarbeiten
df_shanghai = calculate_shanghai_anomaly(LOCAL_DATA_FILE)
df_global = load_global_anomaly_data(GLOBAL_DATA_FILE)

if df_shanghai is not None and df_global is not None:
    # 2. Globale und lokale Daten zusammenführen (basierend auf dem gemeinsamen Jahr)
    df_shanghai_yearly = df_shanghai[["Year", "Shanghai_Anomaly_C"]].set_index("Year")

    df_combined = pd.merge(
        df_shanghai_yearly, df_global, left_index=True, right_index=True, how="inner"
    )

    # 3. Trends berechnen
    years_overlap = df_combined.index.values
    shanghai_temps = df_combined["Shanghai_Anomaly_C"].values
    global_temps = df_combined["Global_Anomaly_C"].values

    # Lineare Regression für Shanghai und Global
    slope_shanghai, intercept_shanghai, _, _, _ = linregress(
        years_overlap, shanghai_temps
    )
    slope_global, intercept_global, _, _, _ = linregress(years_overlap, global_temps)

    # 4. Visualisierung
    plt.figure(figsize=(14, 8))

    # Graphen zeichnen
    plt.plot(
        df_combined.index,
        shanghai_temps,
        label="Shanghai Temperatur-Anomalie (Lokal)",
        color="red",
        linewidth=2,
        marker="o",
        markersize=4,
        alpha=0.7,
    )

    plt.plot(
        df_combined.index,
        global_temps,
        label="Globale Temperatur-Anomalie (Land)",
        color="blue",
        linewidth=2,
        linestyle="-",
    )

    # Trendlinien zeichnen
    plt.plot(
        years_overlap,
        intercept_shanghai + slope_shanghai * years_overlap,
        "--",
        color="red",
        alpha=0.8,
        label=f"Shanghai Trend: +{slope_shanghai*10:.2f} °C/Jahrzehnt",
    )

    plt.plot(
        years_overlap,
        intercept_global + slope_global * years_overlap,
        "--",
        color="blue",
        alpha=0.8,
        label=f"Globaler Trend: +{slope_global*10:.2f} °C/Jahrzehnt",
    )

    # Graphikformatierung
    plt.title(
        "Vergleich: Temperatur-Anomalien in Shanghai vs. Globaler Landdurchschnitt",
        fontsize=16,
    )
    plt.xlabel("Jahr", fontsize=12)
    plt.ylabel(f"Temperatur-Anomalie (°C)", fontsize=12)
    plt.axhline(0, color="gray", linestyle="-", linewidth=0.5)
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

    # 5. Schlussfolgerung ausgeben
    print("\n--- ANALYSE DER ERWÄRMUNGSRATE ---")
    print(
        f"Zeitraum der Analyse (Überlappung): {years_overlap.min()} bis {years_overlap.max()}"
    )
    print(f"Erwärmungsrate Shanghai:    +{slope_shanghai*10:.3f} °C pro Jahrzehnt")
    print(f"Erwärmungsrate Global:     +{slope_global*10:.3f} °C pro Jahrzehnt")

    if abs(slope_shanghai - slope_global) < 0.01:
        print(
            "\nSCHLUSSFOLGERUNG: Die Erwärmungsrate in Shanghai entspricht im Wesentlichen der globalen Rate."
        )
    elif slope_shanghai > slope_global:
        difference = slope_shanghai - slope_global
        print(
            f"\nSCHLUSSFOLGERUNG: Die Erwärmungsrate in Shanghai war im analysierten Zeitraum um ca. {difference*10:.3f} °C/Jahrzehnt HÖHER als der globale Durchschnitt."
        )
        print(
            "Dies deutet auf eine regional oder lokal verstärkte Erwärmung hin (z.B. Urban Heat Island-Effekt oder verstärkte regionale Klimafaktoren)."
        )
    else:
        difference = slope_global - slope_shanghai
        print(
            f"\nSCHLUSSFOLGERUNG: Die Erwärmungsrate in Shanghai war im analysierten Zeitraum um ca. {difference*10:.3f} °C/Jahrzehnt NIEDRIGER als der globale Durchschnitt."
        )
