pipeline {

    agent any

 

    stages 

    {

        stage('Ingestion') 

        {

            steps 
            {
                echo "Starting Ingestion"
            }
 


        }
    
        stage('Docker Running Django App') 

        {

            
            steps 

            {

                sh 'docker-compose -f docker-compose.yml up -d app'

            }
            

        }

        stage('Ready Testing') 

        {

            steps 
            {
                echo "Test it now"
            }
 


        }
    

    }

}