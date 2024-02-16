pipeline {
    agent any

    stages {
        stage('Deleting old docker Images') {
            steps {
                sh 'docker rm -vf $(docker ps -aq)'
                sh 'docker rmi -f $(docker images -aq)'
            }
        }

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
        stage('Whoami') {
            steps {
                sh 'whoami'
            }
        }
        stage('Docker Pushing to Registry') {
            steps {
                sh 'sudo doctl registry login'
                sh 'sudo docker tag cicd_cms_app registry.digitalocean.com/customcms/cicd_cms_app'
                sh 'sudo docker push registry.digitalocean.com/customcms/cicd_cms_app'

            }
        }
    }
}
