# 🛡️ Phishing Email Prediction - End-to-End MLOps

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AWS](https://img.shields.io/badge/AWS-EC2%20|%20S3%20|%20ECR-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## 📋 Project Overview
This project is an advanced Machine Learning solution designed to detect and classify phishing emails to enhance cybersecurity. It features a complete **End-to-End MLOps pipeline**, handling everything from raw data ingestion to real-time cloud deployment.

The system ensures high data quality through automated validation and drift detection and utilizes robust classification algorithms to identify malicious patterns with high precision, minimizing the risk of cyber threats.

## 🔑 Key Features
*   **Modular Architecture:** Structured codebase utilizing Config, Entity, and Components for scalability.
*   **Automated Data Pipeline:** Seamless data extraction from **MongoDB Atlas** with automated train-test splitting.
*   **Data Validation & Drift Detection:** Validates schema and monitors statistical drift to ensure model reliability over time.
*   **High-Performance Modeling:** Optimized classification models tracked via **MLflow** & **DagsHub**.
*   **Cloud-Native Deployment:** Automated CI/CD workflow deploying Dockerized application to **AWS EC2** via **ECR**.

## 🛠️ Tech Stack
*   **Language:** Python
*   **Database:** MongoDB Atlas
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy
*   **MLOps:** MLflow, DagsHub
*   **Containerization:** Docker
*   **Cloud (AWS):** S3 (Artifacts), ECR (Container Registry), EC2 (Production Server)
*   **CI/CD:** GitHub Actions

## 📊 Model Performance
The model achieved exceptional metrics, making it suitable for high-security environments where missing an attack (False Negative) is critical.

| Metric | Score |
| :--- | :--- |
| **F1 Score** | 0.9712 |
| **Recall** | 0.9771 |
| **Precision** | 0.9653 |

*   **97.7% Recall:** Ensures nearly 98 out of 100 phishing attacks are successfully detected.
*   **96.5% Precision:** Ensures extremely low false alarms, preventing legitimate emails from being blocked.

## 🏗️ Project Architecture & Workflow

The pipeline follows a strict modular flow:

1.  **Data Ingestion:** 
    *   Connects to MongoDB Atlas.
    *   Exports data to Feature Store.
    *   Performs Train/Test Split.
2.  **Data Validation:** 
    *   Validates dataset against `schema.yaml`.
    *   Detects Data Drift and generates reports.
3.  **Data Transformation:**
    *   Preprocesses text/numerical data (Imputation, Scaling, Encoding).
    *   Saves transformation objects (`preprocessor.pkl`).
4.  **Model Trainer:**
    *   Trains multiple algorithms (Random Forest, Gradient Boosting, etc.).
    *   Fine-tunes Hyperparameters.
    *   Logs best model to MLflow.
5.  **Deployment:**
    *   CI/CD pipeline builds Docker image.
    *   Pushes image to AWS ECR.
    *   Deploys to AWS EC2 instance.

## 📂 Project Structure
```text
├── .github/workflows   # CI/CD Pipeline
├── src
│   ├── components      # Ingestion, Validation, Transformation, Trainer
│   ├── config          # Configuration classes
│   ├── entity          # Data classes
│   ├── pipeline        # Training & Prediction pipelines
│   ├── utils           # Common utilities
├── artifacts           # Generated outputs
├── config              # Configuration YAML
├── app.py              # Application entry point
├── main.py             # Pipeline entry point
├── push_data.py        # MongoDB data seeder
├── Dockerfile          # Container configuration
├── requirements.txt    # Dependencies
└── README.md
