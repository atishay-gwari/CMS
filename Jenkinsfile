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
        stage('Docker Pushing to Registry') {
            steps {
                sh 'doctl login registry'
                sh 'docker tag cicd_cms_app registry.digitalocean.com/customcms/cicd_cms_app'
                sh 'docker push registry.digitalocean.com/customcms/cicd_cms_app'

            }
        }
    }
}
