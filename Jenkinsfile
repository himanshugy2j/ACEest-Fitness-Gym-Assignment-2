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
                sh 'pip install --upgrade pip pytest'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Code Quality - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh 'sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=app -Dsonar.python.coverage.reportPaths=coverage.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_HUB_TOKEN')]) {
                    sh 'echo $DOCKER_HUB_TOKEN | docker login -u your-dockerhub-username --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
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
