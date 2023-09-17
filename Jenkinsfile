pipeline {
    agent any
    stages {
        stage('build_docker') {
            steps {
                sh 'docker build ./airbot/ -t 165.22.80.137:8083/airbot:1.0'
                sh 'docker build ./infra/nginx/ -t 165.22.80.137:8083/air-nginx:1.0'
            }
        }
        stage('push_to_nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-user', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin 165.22.80.137:8083'
                    sh 'docker push 165.22.80.137:8083/airbot:1.0'
                    sh 'docker push 165.22.80.137:8083/air-nginx:1.0'
                }
            }
        }
    }
}