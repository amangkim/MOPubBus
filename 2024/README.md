# 🚌 Macau Public Bus Data Analysis (2024)

This repository contains data processing and statistical analysis scripts for Macau public bus arrival records collected during **normal days** and **Macau Grand Prix days** in **2024**.

---

## 📁 Dataset Overview

### Data Collection Periods

| Route | Normal Period | Grand Prix Period |
|-------|---------------|-------------------|
| 3     | 2024.10.09 – 2024.10.23 | 2024.11.11 – 2024.11.18 |
| 15    | 2024.10.14 – 2024.10.28 | 2024.11.11 – 2024.11.16, 2024.11.18 – 2024.11.20 |
| 26    | 2024.10.14 – 2024.10.19, 2024.10.21 – 2024.10.28 | 2024.11.11 – 2024.11.18 |
| 73    | 2024.11.24 – 2024.12.09 | 2024.11.11 – 2024.11.18 |
| AP1   | 2024.11.25 – 2024.12.09 | 2024.11.11 – 2024.11.18 |

---

### Data Volume

| Route | Normal Records | Grand Prix Records | Subtotal |
|-------|---------------|--------------------|----------|
| 3     | 36,094        | 6,009              | 42,103   |
| 15    | 21,761        | 4,194              | 25,995   |
| 26    | 54,385        | 15,677             | 70,059   |
| 73    | 34,385        | 6,176              | 41,101   |
| AP1   | 32,568        | 5,759              | 38,327   |
| **Total** | **179,190** | **38,355** | **217,545** |

---

## 📊 Data Features Description

| Feature | Name | Unit | Description | Used in PCA | Used in Heatmap |
|:-------:|------|------|-------------|:-----------:|:---------------:|
| `startStation` | Start station | — | Departure stop of the bus for this segment | | |
| `endStation` | End station | — | Arrival stop of the bus for this segment | ✓ | |
| `time` | Arrival timestamp | hh:mm:ss | Time when bus arrives at `endStation` | ✓ | ✓ |
| `weekday` | Day of week | 0~6 | 0=Monday, … , 6=Sunday | ✓ | ✓ |
| `passengerFlow` | Passenger load | -1, 0~5 | -1 = no data, 0=least crowded, 5=most crowded | ✓ | ✓ |
| `trafficCondition` | Traffic condition | -1, 1~3 | -1 = no data, 1=light, 3=heavy traffic | ✓ | ✓ |
| `busPlate` | Bus license plate | XX0000 | Unique vehicle identifier | | |
| `arrivalDuration` | Travel duration | seconds | Time taken from `startStation` to `endStation` | ✓ | ✓ |

---

## 📂 Source Code Files

All scripts are written in Python and located in the `sourcecodes/` directory.

### 1. `corr_heatmap.py` — Correlation Heatmap

**Purpose:**  
Generate correlation heatmaps for both Normal and Grand Prix datasets to visualise linear relationships between numerical features.

**Key Steps:**
- Loads merged normal and grandprix CSV files.
- Extracts `hour` from `time` column.
- Encodes `route` as numeric labels.
- Computes Pearson correlation matrices.
- Plots triangular heatmaps using Seaborn.

**Output:**  
Two heatmap figures (Normal / Grand Prix) showing correlations among:
- `route`, `hour`, `weekday`, `passengerFlow`, `trafficCondition`, `arrivalDuration`

---

### 2. `pca_figure.py` — Principal Component Analysis (PCA)

**Purpose:**  
Perform PCA to reduce dimensionality and identify which features contribute most to variance in the data.

**Key Steps:**
- Loads normal and grandprix datasets.
- Encodes `endStation` consistently across both datasets.
- Standardises selected features: `endStation`, `hour`, `weekday`, `passengerFlow`, `trafficCondition`, `arrivalDuration`.
- Fits PCA separately for normal and grandprix data.
- Plots:
  - Explained variance ratio (bar + cumulative line).
  - Feature loadings for PC1 and PC2 (bar charts).
  - Biplot (PC1 vs PC2 with feature vectors).

**Output:**  
- Variance explanation plots.
- Feature contribution bar charts.
- Loading vector biplots for both conditions.

---

### 3. `violin_plots.py` — Violin Plots for Feature Distributions

**Purpose:**  
Visualise distribution differences between Normal and Grand Prix periods for key features, with interquartile range (15th–85th percentile) highlighted.

**Key Steps:**
- Loads individual route CSV files (3, 15, 26, 73, AP1) for both periods.
- Filters by specific Grand Prix dates.
- Drops `date` column after filtering.
- Extracts `hour` from `time`.
- Filters data by `passbyNum == 0` (and special handling for AP1).
- Removes outliers beyond ±3 standard deviations for `arrivalDuration`.
- Excludes specific outlier stations manually (e.g., M70, M118 for route 3; M50, T343 for AP1).
- Concatenates all routes into normal and grandprix combined DataFrames.
- Generates 5×2 violin plots comparing distributions of:
  - `hour`, `weekday`, `passengerFlow`, `trafficCondition`, `arrivalDuration`

**Output:**  
A single figure with 10 violin plots (5 features × 2 conditions), where the central 70% of each distribution is highlighted in red.

---

## 🛠 Requirements

Install the required Python packages:

```bash
pip install numpy pandas seaborn matplotlib scikit-learn scikit-learn-intelex
