# 🚌 MOPubBus — Macau Public Bus Data Analysis

MOPubBus is a data analysis project focused on **Macau public bus operations**, aiming to compare and analyze bus performance between **normal days** and **Macau Grand Prix periods** using data science methodologies.

---

## 📖 Overview

Macau, as a popular tourist destination, experiences significant traffic disruptions during major events such as the Macau Grand Prix. This project collects and analyzes operational data from multiple major bus routes, covering:

- 📊 Bus arrival times
- 👥 Passenger load conditions
- 🚦 Traffic conditions on road segments
- ⏱️ Travel duration between stops
- 🌤️ Weather conditions
- 🗓️ Day-of-week and time-of-day patterns

Through **correlation analysis**, **Principal Component Analysis (PCA)**, and **distribution visualization**, this project reveals how bus operations change during the Grand Prix period.

---

## 📂 Repository Structure

- `MOPubBus/`
  - `2024/` — 2024 Data Analysis
    - `datasets/` — Raw datasets (CSV)
    - `sourcecodes/` — Python analysis scripts
    - `Supplementary_MacauBus_2024_Pub_AMG.pdf` — Supplementary document
    - `README.md` — Detailed 2024 documentation
  - `2025/` — 2025 Data Analysis
    - `datasets/` — Raw datasets (CSV)
    - `sourcecodes/` — Python analysis scripts
    - `Supplementary_MacauBus_Pub_AMG.pdf` — Supplementary document
    - `README.md` — Detailed 2025 documentation
  - `README.md` — This file

---

## 🔗 Subprojects

| Year | Data & Code Link |
|------|------------------|
| **2024** | [MOPubBus/2024](https://github.com/amangkim/MOPubBus/tree/main/2024) |
| **2025** | [MOPubBus/2025](https://github.com/amangkim/MOPubBus/tree/main/2025) |

Each subdirectory contains:
- Raw CSV datasets (`datasets/`)
- Complete Python analysis scripts (`sourcecodes/`)
- Supplementary documentation (PDF)
- Detailed `README.md` documentation

---

## 📊 Dataset Overview

### Bus Routes Included

| Route | Description |
|-------|-------------|
| 3     | Major Macau Peninsula trunk route |
| 15    | Connects Coloane with Macau Peninsula |
| 26    | North-south route across Macau |
| 73    | University of Macau shuttle route |
| AP1   | Airport route connecting Macau International Airport |

### Collection Periods

- **Normal days**: Regular non-event weekdays
- **Grand Prix days**: November dates when the Macau Grand Prix takes place

### Data Volume (2024 Example)

| Data Type | Records |
|-----------|---------|
| Normal days | 179,190 |
| Grand Prix days | 38,355 |
| **Total** | **217,545** |

---

## 📋 Data Features

| Field | Description | Values |
|-------|-------------|--------|
| `startStation` | Departure stop | Station code |
| `endStation` | Arrival stop | Station code |
| `time` | Arrival time | hh:mm:ss |
| `weekday` | Day of week | 0=Mon ~ 6=Sun |
| `passengerFlow` | Passenger load | -1=no data, 0~5 (higher = more crowded) |
| `trafficCondition` | Traffic condition | -1=no data, 1~3 (higher = more congested) |
| `busPlate` | License plate | Unique vehicle identifier |
| `arrivalDuration` | Travel duration | Seconds |

---

## 🛠 Analysis Methods

### 1. Correlation Heatmap
- Computes Pearson correlation coefficients between numerical features
- Visualizes linear relationships
- Compares correlation patterns between normal and Grand Prix periods

### 2. Principal Component Analysis (PCA)
- Reduces data dimensionality
- Identifies features with greatest contribution to variance
- Reveals key factors influencing bus operations

### 3. Violin Plots
- Visualizes distribution shapes and densities
- Highlights interquartile ranges
- Compares distribution differences between periods

---

## 📧 Contact

For questions or suggestions, please open a GitHub Issue.

---

**MOPubBus** — Understanding Macau's public transport through data 🚌📈
