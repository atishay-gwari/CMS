pipeline {
    agent any

    stages {
        stage('Cleanup Previous Docker Artifacts') {
            steps {
                script {
                    // Remove existing containers
                    sh 'docker rm -f $(docker ps -a -q) || true'
                    // Remove existing images
                    sh 'docker rmi -f $(docker images -a -q) || true'
                }
            }
        }

        stage('Docker Running') {
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
