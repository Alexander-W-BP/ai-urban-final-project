import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. Konfiguration
# Annahme: Ihre vollständige CSV-Datei heißt 'wetterdaten.csv'
FILE_PATH = "C:\\Studium_TU_Darmstadt\\Master\\3. Semester (Auslandssemester - Soul)\\AI in Urban Planning and Design\\ai-urban-final-project\\data\\temperature\\shanghai_2000_2025.csv"

# 2. Daten laden und vorbereiten
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Fehler: Datei '{FILE_PATH}' nicht gefunden. Bitte den Pfad prüfen.")
    exit()

# Die 'date'-Spalte in das richtige Datumsformat umwandeln und als Index setzen
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Konvertiere 'tavg' zu numerisch. 'errors="coerce"' ersetzt nicht-numerische
# Werte (wie leere Strings oder Kommas) durch NaN (Not a Number).
df["tavg"] = pd.to_numeric(df["tavg"], errors="coerce")

# Entferne Zeilen mit fehlendem 'tavg'
df = df.dropna(subset=["tavg"])


## --- Visualisierung 1: Jährliche Durchschnittstemperatur ---
# Aggregation: Berechne den Mittelwert der 'tavg' für jedes Jahr
df_yearly = df["tavg"].resample("Y").mean()

plt.figure(figsize=(12, 6))

# Zeichne die jährlichen Mittelwerte als Balken
plt.bar(
    df_yearly.index.year,
    df_yearly.values,
    color="skyblue",
    alpha=0.7,
    label="Jährlicher Mittelwert",
)

# Optional: Berechne und zeichne den linearen Trend über die Jahre (Regression)
from scipy.stats import linregress

years = df_yearly.index.year
temps = df_yearly.values
slope, intercept, r_value, p_value, std_err = linregress(years, temps)
plt.plot(
    years,
    intercept + slope * years,
    color="red",
    linestyle="--",
    label=f"Linearer Trend (Anstieg: {slope:.2f}°C/Jahr)",
)

plt.title("Jährliche Durchschnittstemperatur im Zeitverlauf")
plt.xlabel("Jahr")
plt.ylabel("Durchschnittstemperatur (°C)")
plt.grid(axis="y", linestyle="--")
plt.legend()
plt.tight_layout()
plt.show()


## --- Visualisierung 2: Gleitender 365-Tage-Durchschnitt ---
# Berechne den gleitenden Durchschnitt über 365 Tage.
# 'center=True' bedeutet, dass der Durchschnitt in der Mitte des Zeitfensters platziert wird.
df["365-day_avg"] = df["tavg"].rolling(window=365, center=True).mean()

plt.figure(figsize=(14, 7))

# Zeichne die Rohdaten (optional, kann bei sehr großen Datenmengen unübersichtlich sein)
# plt.plot(df.index, df['tavg'], color='lightgray', alpha=0.5, label='Tägliche Durchschnittstemp.')

# Zeichne den gleitenden Durchschnitt
plt.plot(
    df.index,
    df["365-day_avg"],
    color="darkblue",
    linewidth=2,
    label="Gleitender 365-Tage-Durchschnitt",
)

plt.title("Langfristiger Temperaturtrend (Geglätteter Durchschnitt)")
plt.xlabel("Datum")
plt.ylabel("Temperatur (°C)")
plt.grid(axis="y", linestyle="--")
plt.legend()
plt.tight_layout()
plt.show()
