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

        stage('🔧 Install Dependencies') {
            steps {
                script {
                    echo '🔧 Installing system dependencies...'

                    // Skip sudo entirely if we can’t use it
                    if (sh(script: 'command -v sudo >/dev/null 2>&1', returnStatus: true) != 0) {
                        echo '⚠️ Skipping sudo (not available on this Jenkins agent).'
                    } else {
                        sh '''
                        set +e
                        if command -v apt-get >/dev/null; then
                            echo "Using apt-get to install dependencies..."
                            sudo -S apt-get update -y < /dev/null || true
                            sudo -S apt-get install -y python3-venv python3-pip python3-tk < /dev/null || true
                        else
                            echo "apt-get not found, skipping system package installation."
                        fi
                        '''
                    }

                    echo '📦 Creating virtual environment...'
                    sh '''
                    python3 -m venv venv || {
                        echo "⚠️ Virtual env creation failed. ensurepip might be missing."
                        echo "Try preinstalling python3-venv manually on Jenkins node."
                        exit 1
                    }
                    . venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                    '''
                }
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
                withSonarQubeEnv('SonarQube-Jenkins') {
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
                    docker build -t ${DOCKER_IMAGE} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_HUB_TOKEN')]) {
                    sh '''
                        echo $DOCKER_HUB_TOKEN | docker login -u himanshug619 --password-stdin
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "🚀 Deploying to Kubernetes..."
                    kubectl apply -f k8s/deployment.yaml || echo "⚠️ Skipping deploy (no k8s folder found)"
                '''
            }
        }
    }

    post {
        success { echo '✅ Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed!' }
    }
}
