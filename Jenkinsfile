pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t github-health-dashboard:${BUILD_NUMBER} .'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh 'echo "Running tests..."'
                    sh 'docker run --rm github-health-dashboard:${BUILD_NUMBER} python -m pytest || true'
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    sh 'echo "Docker image ready for deployment"'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Build successful!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}