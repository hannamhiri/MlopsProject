pipeline {
    agent none

    environment {
        MLFLOW_TRACKING_URI = "https://dagshub.com/hannamhiri/MlopsProject.mlflow"
        MLFLOW_TRACKING_USERNAME = "hannamhiri"
        MLFLOW_TRACKING_PASSWORD = "d818c76624661ed3e44ed5cd15bb08d17cd94c4d"

        APP_NAME = "customer-churn-app"
        DOCKER_REGISTRY = "hana367"
        IMAGE_TAG = "${BUILD_NUMBER}"
        FULL_IMAGE = "${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
    }

    stages {

        /* ===================== */
        stage('Checkout') {
            agent any
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/hannamhiri/MlopsProject'
            }
        }

        /* ===================== */
        stage('ML Pipeline & Training') {
            agent { docker { image 'python:3.11' } }
            steps {
                sh '''
                apt-get update
                apt-get install -y libgomp1 build-essential
                python -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                python main.py
                '''
            }
        }

        /* ===================== */
        stage('Run Unit Tests') {
            agent { docker { image 'python:3.11' } }
            steps {
                sh '''
                python -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest tests/ --maxfail=1 --disable-warnings -q
                '''
            }
        }

        /* ===================== */
        stage('Build Docker Image') {
            agent any
            steps {
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }

        /* ===================== */
        stage('Push Docker Image') {
            agent any
            steps {
                withDockerRegistry(
                    credentialsId: 'DOCKER_HUB',
                    url: 'https://index.docker.io/v1/'
                ) {
                    sh "docker push ${FULL_IMAGE}"
                }
            }
        }

        /* ===================== */
        stage('Deploy to Kubernetes') {
            agent {
                docker {
                    image 'bitnami/kubectl:latest'
                    args '--entrypoint=""'
                    reuseNode true
                }
            }
            steps {
                withKubeConfig([credentialsId: 'k8s-config']) {
                    sh """
                    sed -i "s|image: ${DOCKER_REGISTRY}/${APP_NAME}:.*|image: ${FULL_IMAGE}|g" deployment.yaml
                    kubectl apply -f deployment.yaml
                    kubectl rollout status deployment/${APP_NAME}
                    """
                }
            }
        }
    }

    }

    post {
        success {
            echo "✅ Déploiement Kubernetes réussi"
        }
        failure {
            echo "❌ Pipeline échoué"
        }
    }
}
