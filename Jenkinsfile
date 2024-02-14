pipeline {

    agent any

 

    stages 

    {

        stage('STart') 

        {

            steps 
            {
                echo "Starting"
            }
 


        }
    
        stage('Docker Running Django App') 

        {

            
            steps 

            {

                sh 'docker-compose -f docker-compose.yml up -d app'

            }
            

        }
        stage('Docker Running Prometheus App') 

        {

            
            steps 

            {

                sh 'docker-compose -f docker-compose.yml up -d prometheus'

            }
            

        }

    

    }

}