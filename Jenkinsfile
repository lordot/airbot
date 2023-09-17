pipeline {
    agent any
    environment {
        REPO = '165.22.80.137:8083'
    }
    stages {
        stage('build_docker') {
            steps {
                sh 'docker build ./airbot/ -t $REPO/airbot:1.0'
                sh 'docker build ./infra/nginx/ -t $REPO/air-nginx:1.0'
            }
        }
        stage('push_to_nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-user', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin $REPO'
                    sh 'docker push $REPO/airbot:1.0'
                    sh 'docker push $REPO/air-nginx:1.0'
                }
            }
        }
    }
}