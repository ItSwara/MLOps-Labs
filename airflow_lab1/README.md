# Swarali Degaonkar - Lab 2 Submission

## Airflow Lab 1

An Apache Airflow workflow for analyzing student sleep patterns using K-Means clustering and the elbow method.

## Overview

This lab demonstrates how to build a data pipeline using Apache Airflow and Docker. The workflow automatically loads student sleep data, preprocesses it, trains a K-Means clustering model, and determines the optimal number of sleep pattern clusters.

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
│   │   └── model.sav       # Saved K-Means model
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

## Setup Instructions

### 1. Clone or Download the Project
```bash
cd ~/Desktop/MLOps/Github_Labs/Lab1/MLOps-Labs/airflow_lab1
```

### 2. Download Docker Compose File
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.1/docker-compose.yaml'
```

### 3. Create Required Directories
```bash
mkdir -p ./dags ./logs ./plugins ./config
```

### 4. Set Environment Variables
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### 5. Modify docker-compose.yaml

Update the following in `docker-compose.yaml`:
```yaml
# Disable example DAGs
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

# Enable XCom pickling
AIRFLOW__CORE__ENABLE_XCOM_PICKLING: 'True'

# Install required Python packages
_PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- pandas scikit-learn kneed}

# Change admin credentials (optional)
_AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow2}
_AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow2}
```

### 6. Initialize Airflow
```bash
docker compose up airflow-init
```

Wait for: `airflow-init-1 exited with code 0`

### 7. Start Airflow
```bash
docker compose up
```

### 8. Access Airflow UI

Open browser and go to: `http://localhost:8080`

**Login credentials:**
- Username: `airflow2`
- Password: `airflow2`

## Running the DAG

1. In the Airflow UI, locate the `Airflow_Lab1` DAG
2. Click the "Trigger DAG" button (play icon)
3. Monitor progress in the Graph view
4. Check logs for results

## Workflow Tasks

The DAG consists of 4 sequential tasks:

1. **load_data_task** - Loads sleep patterns data from CSV
2. **data_preprocessing_task** - Cleans data and selects clustering features
3. **build_save_model_task** - Trains K-Means models (k=1 to 49) and saves optimal model
4. **load_model_task** - Determines optimal clusters using elbow method and makes predictions

## Results

**Expected Output:**
```
Optimal no. of clusters for sleep patterns: 12
Test students assigned to clusters: [4, 9, 0, 1, 7]
```

The analysis identifies 12 distinct sleep pattern clusters among students, such as:
- Healthy sleepers with good duration and quality
- Sleep-deprived students with high caffeine intake
- Active students with poor sleep quality
- And more...

## Stopping Airflow
```bash
# Open a new terminal
docker compose down
```

## Technologies Used

- **Apache Airflow 2.7.1** - Workflow orchestration
- **Docker & Docker Compose** - Containerization
- **Python 3.8** - Programming language
- **pandas** - Data manipulation
- **scikit-learn** - K-Means clustering
- **kneed** - Elbow method for optimal k

## Key Learnings

- Setting up Airflow with Docker
- Creating DAGs with task dependencies
- Using PythonOperator for ML tasks
- Serializing data with pickle and base64 for XCom
- Applying K-Means clustering with elbow method
- Monitoring workflows in Airflow UI

## Author

Swarali Degaonkar
