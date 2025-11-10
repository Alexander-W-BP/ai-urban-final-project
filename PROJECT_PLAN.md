# 🗺️ Projektplan: KI-gestützte Wirksamkeitsanalyse städtischer Klimaschutzaktivitäten

Dieses Dokument skizziert den phasenweisen Ablauf des Projekts zur Analyse der Effektivität von Klimaschutzmaßnahmen mittels eines Deep Neural Networks (DNN) / Autoencoders.

## 🔗 Projekt-Phasen-Übersicht

| Phase | Ziel | Ort im Git-Projekt |
| :--- | :--- | :--- |
| **0. Setup** | Grundstruktur etablieren | `.` (Root) |
| **1. Datenerfassung & Bereinigung** | Rohdaten sammeln und standardisieren | `data/raw`, `data/external` |
| **2. Feature Engineering & Vektorisierung** | Rohe Daten in trainierbare $X$ und $Y$ Vektoren umwandeln | `src/features`, `data/processed` |
| **3. Modell-Design & Training** | DNN/Autoencoder-Architektur definieren und trainieren | `src/models`, `notebooks` |
| **4. Evaluierung & Interpretation** | Modellleistung messen und Wirkung der Maßnahmen verstehen | `notebooks`, `docs` |
| **5. Anwendung & Fazit** | Ergebnisse präsentieren und Fazit ziehen | `.` (Final Report) |

***

## 1. Phase: Datenerfassung & Bereinigung 🔍

Diese Phase konzentriert sich auf die Beschaffung, Strukturierung und Qualitätsprüfung der Daten, die zur Erstellung der Vektoren notwendig sind.

### 🎯 Meilensteine

1.  **Städte-Auswahl:** Definieren der **Zielstädte** (z.B. 50-100 Städte weltweit) für die Datenbeschaffung.
2.  **Aktionen-Masterliste:** Erstellung einer vollständigen, kategorisierten **Masterliste** aller Klimaschutzmaßnahmen ($N$), die die Basis für das **One-Hot-Encoding** bildet.
3.  **Datensammlung:**
    * **Historische Klimadaten** (Temperatur, CO₂) pro Stadt und Jahr (`data/external`).
    * **Strukturdaten** (BIP, Dichte, Grünflächen) pro Stadt (`data/external`).
    * **Aktionshistorie:** Erstellung einer Tabelle, die für jede Stadt und jede Aktion das genaue **Implementierungsdatum** speichert (`data/raw`).
4.  **Bereinigung:** Standardisierung aller Daten. Lösung von fehlenden Werten (**Imputation**) und Behandlung von Ausreißern.

***

## 2. Phase: Feature Engineering & Vektorisierung ⚙️

Die rohen Daten werden in das maschinenlesbare Format der **Input-Vektoren** $X$ und **Output-Vektoren** $Y$ transformiert.

### 🎯 Meilensteine

1.  **Implementierung der Vektor-Klassen (in `src/features`):**
    * **`CityStatusVectorizer`:** Erstellt den skalierten **Stadt-Zustandsvektor (C)**, einschließlich der Berechnung historischer Trends und des Binärvektors $A_{\text{best}}$ der *bestehenden* Aktionen.
    * **`ActionOneHotEncoder`:** Erstellt den **One-Hot-Encoded Vektor (A)** für die *eine neue* Aktion.
    * **`OutputTargetCalculator`:** Berechnet den **Ziel-Vektor (Y)**, d.h. die sequenziellen Veränderungen ($\Delta \text{CO}_2$, $\Delta \text{Temp}$) nach 0,5, 1 und 2 Jahren.
2.  **Dataset-Generierung:** Iteration über alle historischen Zeitpunkte und Städte, um die finalen, numerischen Input-Vektoren $X = [C \mid A]$ und die Ziel-Vektoren $Y$ zu generieren.
3.  **Finales Dataset:** Speichern des fertigen, skalierten **Trainings- und Test-Sets** in `data/processed`.

***

## 3. Phase: Modell-Design & Training 🧠

Definition und Optimierung des Deep Neural Networks (DNN), das die Funktion $f(X) \approx Y$ erlernt.

### 🎯 Meilensteine

1.  **Architektur-Design (in `src/models`):**
    * Definition der **DNN-Architektur** (wahlweise mit einer Encoder-Decoder-Struktur zur Dimensionsreduktion der Features).
    * Wahl der **Aktivierungsfunktionen** (z.B. ReLU).
2.  **Training-Pipeline:**
    * Definition der **Loss Function** (Verlustfunktion): **Mean Squared Error (MSE)**, da es sich um ein Regressionsproblem handelt.
    * Wahl des **Optimierers** (z.B. Adam).
    * Training des Modells unter Verwendung einer **Validierungsmenge** zur Überwachung des Overfittings.
3.  **Hyperparameter-Optimierung:** Experimentieren mit Lernrate, Batch-Größe und Schicht-Struktur.
4.  **Modell-Speicherung:** Speichern des trainierten Modells in `src/models` (z.B. als `.h5`-Datei).

***

## 4. Phase: Evaluierung & Interpretation 📈

Bewertung der Modellleistung und Ableitung der Schlüsse über die Wirksamkeit der Maßnahmen.

### 🎯 Meilensteine

1.  **Metriken-Analyse:** Evaluierung des Modells auf dem **Test-Set** mit Metriken (z.B. MSE, $R^2$) und Visualisierung in einem Notebook (`notebooks`).
2.  **Visualisierung der Vorhersage:** Vergleich der vorhergesagten $Y$-Vektoren mit den tatsächlichen $Y$-Vektoren für exemplarische Städte über die Zeit.
3.  **Modell-Interpretation (Wichtiger Projektschritt):**
    * Durchführung einer **Sensitivitätsanalyse** oder **SHAP/LIME-Analyse** (Erklärbarkeit der KI).
    * Ziel: Verstehen, welche **Aktionen** oder **Stadteigenschaften** den größten Einfluss auf die Reduktion von $\Delta \text{CO}_2$ haben.
4.  **Ergebnis-Dokumentation:** Zusammenfassung der wichtigsten Erkenntnisse über die Wirksamkeit von Maßnahmen in `docs`.

***

## 5. Phase: Anwendung & Fazit ✨

Die Ergebnisse werden in eine anwendbare Form gebracht und das Projekt abgeschlossen.

### 🎯 Meilensteine

1.  **Simulations-Tool:** Erstellung einer einfachen Python-Funktion (in `src/utils`), die als **"Was-wäre-wenn"-Simulator** dient, indem sie reale Stadtdaten und eine fiktive Aktion als Input nimmt und die prognostizierte Entwicklung $Y$ liefert.
2.  **Finale Schlussfolgerung:** Beantwortung der zentralen Forschungsfrage des Midterm Proposals: Welche Klimaschutzmaßnahmen sind im Kontext welcher Städte am effektivsten?
3.  **Abschlussbericht/Präsentation:** Vorbereitung des finalen Ergebnisses.