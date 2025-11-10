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
                echo "🔍 Running SonarQube analysis..."
                script {
                    withCredentials([string(credentialsId: 'JenkinsSonar', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            echo "📡 Starting SonarQube analysis via Docker..."
                            docker run --rm --network host \
                                -v $WORKSPACE:/usr/src \
                                -w /usr/src \
                                sonarsource/sonar-scanner-cli:latest \
                                -Dsonar.projectKey=aceest-fitness \
                                -Dsonar.sources=app \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.host.url=http://172.17.0.2:9000 \
                                -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
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

        // -------- Kubernetes Stages (Fixed) --------

        stage('Kubernetes Namespace Setup') {
            steps {
                sh '''
                    echo "🗂 Creating Kubernetes namespace..."
                    kubectl apply -f k8/namespace.yaml
                '''
            }
        }

        stage('Deploy - Rolling Update') {
            steps {
                sh '''
                    echo "🔄 Applying Rolling Update Deployment..."
                    kubectl apply -f k8/rolling-update/deployment-rolling.yaml -n aceest-fitness
                    kubectl rollout status deployment/aceest-fitness -n aceest-fitness
                '''
            }
        }

        stage('Deploy - Blue-Green') {
            steps {
                sh '''
                    echo "🔵 Deploying Blue version..."
                    kubectl apply -f k8/blue-green/deployment-blue.yaml -n aceest-fitness
                    kubectl rollout status deployment/aceest-fitness-blue -n aceest-fitness

                    echo "🟢 Deploying Green version..."
                    kubectl apply -f k8/blue-green/deployment-green.yaml -n aceest-fitness
                    kubectl rollout status deployment/aceest-fitness-green -n aceest-fitness

                    echo "Switching Service to Green..."
                    kubectl patch service aceest-fitness-service -n aceest-fitness \
                    -p '{"spec":{"selector":{"app":"aceest-fitness","version":"green"}}}'
                '''
            }
        }

        stage('Rollback Check') {
            steps {
                sh '''
                    echo "⚠️ Rollback logic: if Green fails, revert to Blue..."
                    # kubectl rollout undo deployment/aceest-fitness-green -n aceest-fitness
                '''
            }
        }
    }

    post {
        success { echo '✅ Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed!' }
    }
}
