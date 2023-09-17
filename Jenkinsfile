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
                buildImage 'airbot:1.0' $REPO './airbot'
                buildImage 'airnginx:1.0' $REPO './infra/nginx'
            }
        }
        stage('push_to_repo') {
            when {
                branch 'main'
            }
            steps {
                pushImage $REPO 'airbot:1.0'
                pushImage $REPO 'airnginx:1.0'
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