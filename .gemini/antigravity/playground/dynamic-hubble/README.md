# Urban Traffic Congestion Prediction

## Project Overview
This project implements a data-driven system to predict urban traffic congestion. It uses synthetic data representing GPS traces, traffic sensors, weather conditions, and event schedules to model and forecast traffic volume.

**Key Achievement:** The Random Forest model achieves an **R² score of 0.93**, successfully capturing the complex non-linear relationships between time of day, weather, and traffic flow.

## Project Structure
*   `data_generator.py`: Generates the synthetic datasets (`gps_data.csv`, `traffic_sensors.csv`, `weather_data.csv`, `event_schedule.csv`).
*   `processing.py`: Cleans, integrates, and encodes the raw data into `processed_data.csv`.
*   `analysis.py`: Performs Exploratory Data Analysis (EDA) and generates visualization plots.
*   `modeling.py`: Trains and evaluates Linear Regression and Random Forest models.
*   `project_report.md`: Detailed report of findings, methodology, and recommendations.

## How to Run
1.  **Generate Data**:
    ```bash
    python data_generator.py
    ```
2.  **Process Data**:
    ```bash
    python processing.py
    ```
3.  **Run Analysis**:
    ```bash
    python analysis.py
    ```
4.  **Train Model**:
    ```bash
    python modeling.py
    ```

## Requirements
*   Python 3.x
*   pandas
*   numpy
*   scikit-learn
*   matplotlib
*   seaborn
