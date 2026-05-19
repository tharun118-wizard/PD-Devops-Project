pipeline {
    agent any

    environment {
        DOCKER_HUB = "tharun118wizard"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/tharun118-wizard/PD-Devops-Project.git'
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                dir('backend') {
docker push $DOCKER_HUB/pd-backend:$BUILD_NUMBER
docker push $DOCKER_HUB/pd-backend:latest
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                dir('frontend') {
               docker build \
-t $DOCKER_HUB/pd-frontend:$BUILD_NUMBER \
-t $DOCKER_HUB/pd-frontend:latest .
                }
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Backend Image') {
            steps {
              docker build \
         docker push $DOCKER_HUB/pd-backend:$BUILD_NUMBER
         docker push $DOCKER_HUB/pd-backend:latest
            }
        }

        stage('Push Frontend Image') {
            steps {
            docker push $DOCKER_HUB/pd-frontend:$BUILD_NUMBER
           docker push $DOCKER_HUB/pd-frontend:latest
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/ --validate=false'
            }
        }
    }
}
