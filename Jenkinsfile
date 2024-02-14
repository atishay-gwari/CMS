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
    
        stage('Docker done') 

        {

            
            steps 

            {

                bash 'docker-compose up --build -d'

            }
            

        }

    

    }

}