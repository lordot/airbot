#!/usr/bin/env groovy

@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        REPO = '165.22.80.137:8083'
        CREDS = credentials('nexus-user')
    }
    stages {
        stage('build_docker') {
            steps {
                script {
                    buildImage('airbot:1.0', ${REPO}, './airbot')
                }
                script {
                   buildImage('airnginx:1.0', ${REPO}, './infra/nginx')
                }
            }
        }
        stage('push_to_repo') {
            when {
                branch 'main'
            }
            steps {
                script {
                    pushImage(${REPO}, 'airbot:1.0')
                }
                script {
                    pushImage(${REPO}, 'airnginx:1.0')
                }
            }
        }
    }
    post {
        always {
            sh 'docker rmi $REPO/airbot:1.0'
            sh 'docker rmi $REPO/air-nginx:1.0'
        }
    }
}