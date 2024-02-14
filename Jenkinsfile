pipeline {
    agent any

    stages {
        stage('Run Django with Docker Compose') {
            steps {
                
                bash "docker-compose -f docker-compose.yml up -d app"
                
            }
        }

        stage('Run Prometheus') {
            steps {
                    bash "docker-compose -f docker-compose.yml up -d prometheus"
                }
            }
            
        }
    }



