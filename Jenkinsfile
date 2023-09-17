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
                    buildImage("${REPO}/airbot:1.0", './airbot')
                }
                script {
                   buildImage("${REPO}/airnginx:1.0", './infra/nginx')
                }
            }
        }
        stage('push_to_repo') {
            when {
                branch 'main'
            }
            steps {
                script {
                    loginDocker REPO
                }
                script {
                    pushImage("${REPO}/airbot:1.0")
                }
                script {
                    pushImage("${REPO}/airnginx:1.0")
                }
            }
        }
    }
    post {
        success {
            sh "docker rmi ${REPO}/airbot:1.0"
            sh "docker rmi ${REPO}/airnginx:1.0"
        }
    }
}