## 📝 Vektordefinitionen für das Urban Climate AI Modell

Dieses Dokument definiert die genaue Struktur und Reihenfolge der Features für die Input- und Output-Vektoren. **Die Reihenfolge der Features muss im Code strikt eingehalten werden.**

### 1. Input-Vektor (X)

Der Vektor X ist die Konkatenation des Stadt-Zustandsvektors (C) und des Aktions-Vektors (A).

#### A. Stadt-Zustandsvektor (C) - Länge: [C_Länge angeben]

| Index-Bereich | Feature-Name | Beschreibung | Codierung/Aufbereitung |
| :--- | :--- | :--- | :--- |
| C[0] | Einw.zahl (Normiert) | Einwohnerzahl der Stadt zum Zeitpunkt T. | [cite_start]Min-Max Normalisierung [cite: 48] |
| C[1] | Anteil Grünflächen | Proportionale Fläche der Parks/Grünanlagen. | [cite_start]Skalar, normalisiert [cite: 48] |
| C[2-X] | Bestehende Aktionen Vektor | [cite_start]OHE der Aktionen, die VOR T implementiert wurden (z.B. "One Less Nuclear Plant" [cite: 9]). | Binär (0/1) |
| C[X+1] | CO2-Trend (5 Jahre) | Steigung der CO2-Daten der letzten 5 Jahre. | [cite_start]Skalar, normalisiert [cite: 46] |
| ... | ... | ... | ... |

#### B. Aktions-Vektor (A) - Länge: [A_Länge angeben]

| Index-Bereich | Feature-Name | Beschreibung | Codierung/Aufbereitung |
| :--- | :--- | :--- | :--- |
| A[0-N] | One-Hot Encoding (A_neu) | [cite_start]Die EINE neue, zum Zeitpunkt T gestartete Aktion (z.B. "Zero Waste City"-Zertifizierung [cite: 13]). | OHE (N Einträge, nur 1 ist 1) |

---

### 2. Output-Vektor (Y)

Der Vektor Y (Länge 6) stellt die Veränderung der Zielgrößen über Zeit dar.

| Index | Feature-Name | Beschreibung |
| :--- | :--- | :--- |
| Y[0] | Delta CO2 (nach 0,5 Jahren) | $\text{CO}_2 \text{-Emissionen}_{\text{T+0.5}} - \text{CO}_2 \text{-Emissionen}_{\text{T}}$ |
| Y[1] | Delta Temp (nach 0,5 Jahren) | $\text{Temperatur}_{\text{T+0.5}} - \text{Temperatur}_{\text{T}}$ |
| Y[2] | Delta CO2 (nach 1 Jahr) | ... |
| Y[3] | Delta Temp (nach 1 Jahr) | ... |
| Y[4] | Delta CO2 (nach 2 Jahren) | ... |
| Y[5] | Delta Temp (nach 2 Jahren) | ... |