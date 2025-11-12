## 📝 Vektor-Definitionen für das KI-Modell zum Stadtklima – Erweiterung des Output-Vektors

Dieses Dokument definiert die exakte Struktur und Reihenfolge der Features für die Input- und Output-Vektoren. **Die Reihenfolge der Features muss im Code strikt eingehalten werden.**

***

### 1. Input Vector (X)

Der Vektor X ist die Konkatenation des City State Vector (C) und des Action Vector (A).

#### A. City State Vector (C) - Länge: Variabel (mindestens 7 + Anzahl der OHE-Kategorien)

Dieser Vektor repräsentiert den Zustand der Stadt zum Zeitpunkt T, bevor eine neue Aktion implementiert wird.

| Index Range | Feature Name | Beschreibung | Kodierung/Vorbereitung |
| :--- | :--- | :--- | :--- |
| C[0] | **Current Date (T)** | Der Zeitpunkt des Analyse-/Aktionsstarts. | Skalar, normalisiert (z. B. Jahre seit 2000) |
| C[1] | **Population Size** | Die Bevölkerungsgröße der Stadt. | Min-Max-Normalisierung |
| C[2] | **Average Age** | Das Durchschnittsalter der Bevölkerung. | Skalar, normalisiert |
| C[3] | **GDP** | Bruttoinlandsprodukt (oder Äquivalent) der Stadt. | Min-Max-Normalisierung |
| C[4] | **Country/Region (OHE)** | Kategorische Kodierung von Land und Region. | One-Hot-Encoding (OHE) |
| C[5] | **Climate Zone (OHE)** | Die Klimazone der Stadt (z. B. nach Köppen-Geiger). | One-Hot-Encoding (OHE) |
| C[6] | **CO2 History (Values)** | Vektor historischer CO2-Emissionswerte (z. B. die letzten 5 Jahre). | Vektor (mehrere Einträge), normalisiert |
| C[7] | **Temp History (Values)** | Vektor historischer Temperaturwerte (z. B. die letzten 5 Jahre). | Vektor (mehrere Einträge), normalisiert |
| C[X - Y] | **Existing Actions Vector** | OHE der CO2-reduzierenden Maßnahmen, die **VOR T** implementiert wurden. | Binär (0/1) |

***

#### B. Action Vector (A) - Länge: Variabel (3 + Anzahl der Maßnahmen + Anzahl der Scopes)

Dieser Vektor beschreibt die **EINE** neue **CO2-reduzierende** Maßnahme, die zum Zeitpunkt T gestartet wird.

| Index Range | Feature Name | Beschreibung | Kodierung/Vorbereitung |
| :--- | :--- | :--- | :--- |
| A[0] | **Start Date (T_Start)** | Das Datum, an dem die neue Maßnahme gestartet wird. | Skalar, normalisiert (z. B. Monate seit C[0]) |
| A[1] | **Costs (Normalized)** | Geschätzte Kosten (z. B. in Millionen €) der Maßnahme. | Min-Max-Normalisierung |
| A[2 - N] | **Scope (OHE)** | Qualitative Bewertung des Umfangs (z. B. "Pilot", "Mittel", "Stadtweit"). | One-Hot-Encoding (OHE) |
| A[N+1 - Z] | **Measure (OHE)** | One-Hot-Encoding für die **EINE** neue CO2-reduzierende Maßnahme, die zum Zeitpunkt T gestartet wurde. | OHE (Nur 1 ist 1) |

**Liste der CO2-reduzierenden Maßnahmen (für OHE - Reihenfolge beibehalten):**
1. Expansion of Pedestrian Paths
2. Expansion of Bicycle Paths
3. Expansion of Public Local Transport
4. Expansion of Public Long-Distance Transport
5. Alternative Drive Systems and Sharing Offers
6. Intelligent Traffic Control
7. Energy-efficient Building Refurbishment
8. Green Infrastructure (Carbon Sinks)
9. Sustainable Land Management (Avoidance of Urban Sprawl)

***

### 2. Output Vector (Y) 🆕

Der Vektor Y (Länge **20**) stellt die Entwicklung der Zielgrößen über vier zukünftige Zeitpunkte (**T+0.5, T+1, T+2, T+5**) dar, differenziert nach Wirkungsbereich.

| Index | Feature Name | Beschreibung |
| :--- | :--- | :--- |
| **--- T+0.5 Jahre ---** | | |
| Y[0] | **CO2 Dev. (0.5y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+0.5}}$ in der **unmittelbaren Wirkungszone** |
| Y[1] | **CO2 Dev. (0.5y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+0.5}}$ für die **gesamte Stadt** |
| Y[2] | **Elec. Price Dev. (0.5y)** | $\Delta \text{Electricity Price}_{\text{T+0.5}}$ (Stadtweit) |
| Y[3] | **Temp Dev. (0.5y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+0.5}}$ in der **unmittelbaren Wirkungszone** |
| Y[4] | **Temp Dev. (0.5y, Entire City)** | $\Delta \text{Temperature}_{\text{T+0.5}}$ für die **gesamte Stadt** |
| **--- T+1 Jahr ---** | | |
| Y[5] | **CO2 Dev. (1y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+1}}$ in der **unmittelbaren Wirkungszone** |
| Y[6] | **CO2 Dev. (1y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+1}}$ für die **gesamte Stadt** |
| Y[7] | **Elec. Price Dev. (1y)** | $\Delta \text{Electricity Price}_{\text{T+1}}$ (Stadtweit) |
| Y[8] | **Temp Dev. (1y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+1}}$ in der **unmittelbaren Wirkungszone** |
| Y[9] | **Temp Dev. (1y, Entire City)** | $\Delta \text{Temperature}_{\text{T+1}}$ für die **gesamte Stadt** |
| **--- T+2 Jahre ---** | | |
| Y[10] | **CO2 Dev. (2y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+2}}$ in der **unmittelbaren Wirkungszone** |
| Y[11] | **CO2 Dev. (2y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+2}}$ für die **gesamte Stadt** |
| Y[12] | **Elec. Price Dev. (2y)** | $\Delta \text{Electricity Price}_{\text{T+2}}$ (Stadtweit) |
| Y[13] | **Temp Dev. (2y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+2}}$ in der **unmittelbaren Wirkungszone** |
| Y[14] | **Temp Dev. (2y, Entire City)** | $\Delta \text{Temperature}_{\text{T+2}}$ für die **gesamte Stadt** |
| **--- T+5 Jahre (NEU) ---** | | |
| Y[15] | **CO2 Dev. (5y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+5}}$ in der **unmittelbaren Wirkungszone** |
| Y[16] | **CO2 Dev. (5y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+5}}$ für die **gesamte Stadt** |
| Y[17] | **Elec. Price Dev. (5y)** | $\Delta \text{Electricity Price}_{\text{T+5}}$ (Stadtweit) |
| Y[18] | **Temp Dev. (5y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+5}}$ in der **unmittelbaren Wirkungszone** |
| Y[19] | **Temp Dev. (5y, Entire City)** | $\Delta \text{Temperature}_{\text{T+5}}$ für die **gesamte Stadt** |