pipeline {
    agent any

    stages {
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose -f docker-compose.yml build'
            }
        }
        stage('Docker Running Django App') {
            steps {
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }
    }
}
