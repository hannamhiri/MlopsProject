# Customer Churn Prediction - MLOps Project





## **Présentation**
Ce projet implémente un modèle de prédiction du **churn client** avec une architecture **MLOps complète**, incluant :  

- Suivi des expériences avec **MLflow**  
- Modèle ML pour prédire le churn des clients  
- API **Flask** pour la prédiction en temps réel  
- Pipeline CI/CD avec **Jenkins**, **Docker** et **Kubernetes**  
- Sélection automatique du **meilleur modèle** basé sur le **ROC-AUC**

---

## **Objectifs**
1. Collecte et préparation des données clients  
2. Prédiction du churn client  
3. Déploiement automatisé avec CI/CD  
4. Suivi des modèles et sélection du meilleur avec MLflow  

---

## **Architecture du projet**
```mermaid
flowchart LR
    A[Data Source] --> B[Data Ingestion]
    B --> C[Data Validation]
    C --> D[Data Transformation]
    D --> E[Model Training]
    E --> F[Model Evaluation & MLflow Tracking]
    F --> G[Best Model Selection]
    G --> H[Flask API]
    H --> I[Docker Container]
    I --> J[Kubernetes Deployment]
