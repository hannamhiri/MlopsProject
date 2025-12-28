# 📊 Customer Churn Prediction - MLOps Project

This project implements a **Customer Churn Prediction** model within a complete **MLOps architecture**. It is designed to automate the entire lifecycle of a machine learning model, from data ingestion to production deployment [1].

## 🎯 Project Objectives
1.  **Data Preparation**: Collection and rigorous processing of customer data [1].
2.  **Churn Prediction**: Building a model to identify customers at risk of leaving [1].
3.  **Automated Deployment**: Implementing a full CI/CD pipeline [1].
4.  **Model Management**: Tracking experiments and automatically selecting the best model based on **ROC-AUC** metrics using **MLflow** [1, 2].

## 🏗️ Architecture Workflow
The project follows a structured pipeline as seen in the repository's logic [2]:
*   **Data Layer**: Ingestion and Validation.
*   **Processing Layer**: Transformation and Model Training.
*   **MLOps Layer**: Evaluation and MLflow Tracking, followed by **Automatic Best Model Selection**.
*   **Deployment Layer**: Flask API, Docker Containerization, and Kubernetes Orchestration.



## 📂 Repository Structure
The project is organized to separate research from production-ready code [3]:
*   `src/mlProject/`: Core source code.
*   `research/`: Jupyter Notebooks for data exploration.
*   `config/` & `params.yaml`: Configuration and hyperparameters.
*   `templates/` & `static/`: Frontend files for the Flask web interface.
*   `tests/`: Scripts for quality assurance.
*   `Dockerfile` & `Jenkinsfile`: Infrastructure for containerization and CI/CD.

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/hannamhiri/MlopsProject.git
cd MlopsProject
2. Environment Configuration
(Standard practice recommendation)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
python setup.py install
4. Execute the Pipeline
To run the full training and evaluation workflow:
python main.py
5. Launch the Web API
To start the Flask application for real-time predictions:
python app.py
🚀 CI/CD & Deployment
The project leverages industry-standard tools for continuous integration and deployment:
• MLflow: For tracking experiments and model versions.
• Jenkins: Orchestrates the CI/CD pipeline via the Jenkinsfile.
• Docker: Packages the application via the Dockerfile.
• Kubernetes: Handles final deployment using deployment.yaml



