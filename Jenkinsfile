pipeline {
    agent any

    environment {
        APP_NAME = "aceest-fitness"
        VERSION = "v1.3"
        DOCKER_IMAGE = "himanshug619/${APP_NAME}:${VERSION}"
        SONARQUBE = "SonarQubeServer"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/himanshugy2j/ACEest-Fitness-Gym-Assignment-2.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "🔧 Installing system dependencies..."
                    apt-get update
                    apt-get install -y python3-tk python3-venv python3-pip

                    echo "📦 Creating virtual environment..."
                    python3 -m venv venv
                    . venv/bin/activate

                    echo "📦 Installing Python dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt || pip install flask pytest
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "🧪 Running unit tests..."
                    python3 -m pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Code Quality - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
                        echo "🔍 Running SonarQube analysis..."
                        sonar-scanner \
                          -Dsonar.projectKey=aceest-fitness \
                          -Dsonar.sources=app \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "🐳 Building Docker image..."
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_HUB_TOKEN')]) {
                    sh '''
                        echo $DOCKER_HUB_TOKEN | docker login -u himanshug619 --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "🚀 Deploying to Kubernetes..."
                    kubectl apply -f k8s/deployment.yaml
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
