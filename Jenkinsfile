pipeline {
    agent any

    environment {
        // MLflow distant
        MLFLOW_TRACKING_URI = credentials('https://dagshub.com/hannamhiri/MlopsProject.mlflow') // ajouter dans Jenkins
        MLFLOW_TOKEN = credentials('d818c76624661ed3e44ed5cd15bb08d17cd94c4d') // ajouter dans Jenkins

        // Variables Docker (optionnel)
        DOCKER_IMAGE = "customer-churn-app:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/hannamhiri/MlopsProject'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running Pytest for UC..."
                sh '. venv/bin/activate && pytest tests/ --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Run ML Pipeline') {
            steps {
                echo "Running ML pipeline..."
                sh '. venv/bin/activate && python main.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Deploy Flask App') {
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
