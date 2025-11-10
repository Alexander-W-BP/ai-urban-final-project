## 📝 Vector Definitions for the Urban Climate AI Model

This document defines the exact structure and sequence of features for the input and output vectors. **The order of the features must be strictly adhered to in the code.**

***

### 1. Input Vector (X)

The vector X is the concatenation of the City State Vector (C) and the Action Vector (A).

#### A. City State Vector (C) - Length: Variable (minimum 7 + number of OHE categories)

This vector represents the state of the city at time T, before a new action is implemented.

| Index Range | Feature Name | Description | Encoding/Preparation |
| :--- | :--- | :--- | :--- |
| C[0] | **Current Date (T)** | The time point of the analysis/action start. | Scalar, normalized (e.g., years since 2000) |
| C[1] | **Population Size** | The population size of the city. | Min-Max Normalization |
| C[2] | **Average Age** | The average age of the population. | Scalar, normalized |
| C[3] | **GDP** | Gross Domestic Product (or equivalent) of the city. | Min-Max Normalization |
| C[4] | **Country/Region (OHE)** | Categorical encoding of country and region. | One-Hot Encoding (OHE) |
| C[5] | **Climate Zone (OHE)** | The city's climate zone (e.g., according to Köppen-Geiger). | One-Hot Encoding (OHE) |
| C[6] | **CO2 History (Values)** | Vector of historical CO2 emission values (e.g., the last 5 years). | Vektor (multiple entries), normalized |
| C[7] | **Temp History (Values)** | Vector of historical temperature values (e.g., the last 5 years). | Vektor (multiple entries), normalized |
| C[X - Y] | **Existing Actions Vector** | OHE of the CO2-reducing actions that were implemented BEFORE T. | Binary (0/1) |

***

#### B. Action Vector (A) - Length: Variable (3 + number of measures + number of scopes)

This vector describes the **ONE** new **CO2-reducing** measure started at time T.

| Index Range | Feature Name | Description | Encoding/Preparation |
| :--- | :--- | :--- | :--- |
| A[0] | **Start Date (T_Start)** | The date on which the new measure is started. | Scalar, normalized (e.g., months since C[0]) |
| A[1] | **Costs (Normalized)** | Estimated costs (e.g., in millions of €) of the measure. | Min-Max Normalization |
| A[2 - N] | **Scope (OHE)** | Qualitative assessment of the scope (e.g., "Pilot," "Medium," "City-wide"). | One-Hot Encoding (OHE) |
| A[N+1 - Z] | **Measure (OHE)** | One-Hot Encoding for the ONE new CO2-reducing action started at time T. | OHE (Only 1 is 1) |

**List of CO2-Reducing Measures (for OHE - maintain order):**
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

### 2. Output Vector (Y)

Der Vektor Y (Länge 15) stellt die Entwicklung der Zielgrößen über drei zukünftige Zeitpunkte dar, differenziert nach Wirkungsbereich.

| Index | Feature Name | Description |
| :--- | :--- | :--- |
| Y[0] | **CO2 Dev. (0.5y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+0.5}}$ in the **Immediate Area** of Impact |
| Y[1] | **CO2 Dev. (0.5y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+0.5}}$ for the **Entire City** |
| Y[2] | **Elec. Price Dev. (0.5y)** | $\Delta \text{Electricity Price}_{\text{T+0.5}}$ (City-wide) |
| Y[3] | **Temp Dev. (0.5y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+0.5}}$ in the **Immediate Area** of Impact |
| Y[4] | **Temp Dev. (0.5y, Entire City)** | $\Delta \text{Temperature}_{\text{T+0.5}}$ for the **Entire City** |
| Y[5] | **CO2 Dev. (1y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+1}}$ in the **Immediate Area** of Impact |
| Y[6] | **CO2 Dev. (1y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+1}}$ for the **Entire City** |
| Y[7] | **Elec. Price Dev. (1y)** | $\Delta \text{Electricity Price}_{\text{T+1}}$ (City-wide) |
| Y[8] | **Temp Dev. (1y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+1}}$ in the **Immediate Area** of Impact |
| Y[9] | **Temp Dev. (1y, Entire City)** | $\Delta \text{Temperature}_{\text{T+1}}$ for the **Entire City** |
| Y[10] | **CO2 Dev. (2y, Imm. Area)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+2}}$ in the **Immediate Area** of Impact |
| Y[11] | **CO2 Dev. (2y, Entire City)** | $\Delta \text{CO}_2 \text{ Emissions}_{\text{T+2}}$ for the **Entire City** |
| Y[12] | **Elec. Price Dev. (2y)** | $\Delta \text{Electricity Price}_{\text{T+2}}$ (City-wide) |
| Y[13] | **Temp Dev. (2y, Imm. Area)** | $\Delta \text{Temperature}_{\text{T+2}}$ in the **Immediate Area** of Impact |
| Y[14] | **Temp Dev. (2y, Entire City)** | $\Delta \text{Temperature}_{\text{T+2}}$ for the **Entire City** |