# Swarali Degaonkar - Lab 2 Submission

## Airflow Lab 1

An Apache Airflow workflow for analyzing student sleep patterns using using a Random Forest Regressor.

## Overview

This lab demonstrates how to build a data pipeline using Apache Airflow and Docker. The workflow automatically loads student sleep data, preprocesses it, trains a using a Random Forest Regressor model, and predicts Sleet Quality .

## Dataset

**Source:** [Student Sleep Patterns Dataset (Kaggle)](https://www.kaggle.com/datasets/arsalanjamal002/student-sleep-patterns/data)

**Features used for clustering:**
- Sleep Duration (hours)
- Sleep Quality (1-10 rating)
- Caffeine Intake (drinks per day)
- Screen Time (hours)
- Physical Activity (minutes)

**Data split:**
- Training: 495 students (file.csv)
- Testing: 5 students (test.csv)

## Project Structure
```
airflow_lab1/
├── dags/
│   ├── airflow.py          # DAG definition
│   ├── data/
│   │   ├── file.csv        # Training data
│   │   └── test.csv        # Test data
│   ├── model/
│   │   └── model.sav       # Saved Random Forest Regressor
│   └── src/
│       ├── __init__.py
│       └── lab.py          # ML functions
├── logs/                   # Airflow logs
├── plugins/                # Airflow plugins
├── config/                 # Airflow config
├── .env                    # Environment variables
├── docker-compose.yaml     # Docker configuration
└── README.md
```

## Prerequisites

- Docker Desktop installed and running
- At least 4GB RAM allocated to Docker
- Python 3.8+ (for local development)


## Workflow Tasks

The DAG consists of 4 sequential tasks:

1. **load_data_task** - Loads sleep patterns data from CSV
2. **data_preprocessing_task** - Cleans data and selects clustering features
3. **build_save_model_task** - Trains random forect models
4. **load_model_task** - Determines optimal clusters using elbow method and makes predictions


## Technologies Used

- **Apache Airflow 2.7.1** - Workflow orchestration
- **Docker & Docker Compose** - Containerization
- **Python 3.8** - Programming language
- **pandas** - Data manipulation
- **scikit-learn** - Random Forest 

### Features Used for Prediction
- Sleep Duration (hours)
- Caffeine Intake (drinks per day)
- Screen Time (hours)
- Physical Activity (minutes)

### Target Variable
- Sleep Quality (1–10 rating)


### Random Forest Regressor
The model predicts Sleep Quality based on selected lifestyle and sleep-related features.

Random Forest was chosen because:
- It handles non-linear relationships
- It captures feature interactions
- It performs well on structured tabular data
- It reduces overfitting compared to single decision trees


## Results 

### Training Performance
Train RMSE: 1.1823

### Test Predictions
Predicted Sleep_Quality for test students:
[6.0066, 4.5266, 4.52, 8.6933, 3.5833]

### Returned Value from DAG
6.006666666666667

## Conclusion

The Random Forest model successfully trained and generated predictions.
The Airflow DAG executed without errors and produced reasonable prediction results.


## Author

Swarali Degaonkar
