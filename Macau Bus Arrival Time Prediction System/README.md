# Macau Bus Arrival Time Prediction

This project collects real-time Macau public transportation information, including bus data during the Grand Prix period, and integrates it with weather conditions to predict bus arrival times using machine learning.

## Overview

Accurate bus arrival prediction is essential for improving public transport efficiency, especially during major events like the Macau Grand Prix when traffic patterns deviate significantly from normal conditions. This project focuses on:

- Collecting real-time bus and weather data from Macau's public transit system
- Building predictive models for bus arrival times under normal traffic conditions
- Comparing multiple machine learning algorithms to identify the best-performing approach

## Dataset

The dataset consists of data collected from **Route 3** and **AP1** during normal operating periods in **2025**.

- **Training Data**: Only data from Route 3 and AP1 under normal traffic conditions were used for training
- **Features**: Bus location, route information, stop sequences, and corresponding weather conditions
- **Target**: Bus arrival times at specific stops

## Project Structure

| File | Description |
|------|-------------|
| `5routes_weather.py` | Collects real-time bus data and weather conditions for five routes |
| `bus_stops_list_3.py` | Retrieves the bus stop list for Route 3 |
| `get_weather.py` | Collects all weather information |
| `getfullroute.py` | Retrieves complete bus route information |
| `replace_weather.py` | Replaces weather condition strings with numerical values |
| `split_dataset.ipynb` | Splits the dataset into training and testing sets |
| `KNN(normal-normal)HSA_remove(P).ipynb` | Trains the K-Nearest Neighbors model |
| `RF(normal-normal)HSA_remove(P).ipynb` | Trains the Random Forest model |
| `XGBoost(normal-normal)HSA_remove(P).ipynb` | Trains the XGBoost model |
| `plot_result.ipynb` | Generates comparison plots for the three models |

## Methodology

1. **Data Collection**: Real-time bus location and weather data are collected using the Macau transit API
2. **Preprocessing**: Weather strings are converted to numerical values; datasets are split into training and testing sets
3. **Model Training**: Three machine learning algorithms are trained and evaluated:
   - K-Nearest Neighbors (KNN)
   - Random Forest (RF)
   - XGBoost
4. **Evaluation**: Model performance is compared using standard regression metrics and visualized for analysis

## Requirements

- Python 3.x
- Jupyter Notebook
- pandas, numpy, scikit-learn, xgboost
- requests (for API data collection)

## Usage

1. Run the data collection scripts to gather real-time bus and weather data:
   ```bash
   python 5routes_weather.py
   python get_weather.py