pipeline {
    agent any

    stages {
        stage('Run Django with Docker Compose') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml up -d app"
                }
            }
            post {
                success {
                    echo "Django application is running"
                }
                failure {
                    error "Failed to start Django application"
                }
            }
        }

        stage('Run Prometheus') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml up -d prometheus"
                }
            }
            post {
                success {
                    echo "Prometheus is running"
                }
                failure {
                    error "Failed to start Prometheus"
                }
            }
        }
    }

    post {
        always {
            script {
                sh "docker-compose -f docker-compose.yml down"
            }
        }
    }
}
