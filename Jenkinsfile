pipeline {
    agent any

    stages {
        stage('Whoami') {
            steps {
                sh'pwd'
                sh 'ls -a'
                sh 'whoami'
            }
        }

        stage('Docker Running') {
            steps {
                sh 'docker-compose -f docker-compose.yml up --build -d'
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
