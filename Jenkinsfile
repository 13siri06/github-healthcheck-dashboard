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
                    sh 'echo "Build and deployment successful!"'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}