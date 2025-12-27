pipeline {
    agent none

    environment {
        // MLflow distant
        MLFLOW_TRACKING_URI = "https://dagshub.com/hannamhiri/MlopsProject.mlflow"
        MLFLOW_TRACKING_USERNAME = "hannamhiri"
        MLFLOW_TRACKING_PASSWORD = "d818c76624661ed3e44ed5cd15bb08d94c4d"
        DOCKER_IMAGE = "customer-churn-app:latest"
        PATH = "/usr/bin:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            agent any
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/hannamhiri/MlopsProject'
            }
        }

        stage('Install Dependencies') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                echo "Installing system dependencies..."
                sh 'apt-get update && apt-get install -y libgomp1'

                echo "Setting up Python virtual environment..."
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }


        stage('Run ML Pipeline') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                echo "Running ML pipeline..."
                sh '. venv/bin/activate && python main.py'
            }
        }

        

        stage('Run Unit Tests') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                echo "Running Pytest for UC..."
                sh '. venv/bin/activate && pytest tests/ --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Deploy Flask App') {
            agent any
            steps {
                echo "Deploying Flask app..."
                // Arrêter conteneur existant (si présent)
                sh "docker rm -f customer-churn-app || true"
                // Lancer le nouveau conteneur
                sh "docker run -d --name customer-churn-app -p 8080:8080 ${DOCKER_IMAGE}"
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
            // Optionnel : notification Slack ou email
        }
        failure {
            echo 'Pipeline failed!'
            // Optionnel : notification Slack ou email
        }
    }
}
