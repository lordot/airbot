#!/usr/bin/env groovy

@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        REPO = '165.22.80.137:8083'
        CREDS = credentials('nexus-user')
    }
    stages {
        stage('increment_version') {
            steps {
                script {
                    incrementVersion "./airbot"
                }
            }
        }
        stage('build_docker') {
            steps {
                script {
                    buildImage("${REPO}/airbot:${env.CURRENT_VERSION}", './airbot')
                }
                script {
                    buildImage("${REPO}/airnginx:${env.CURRENT_VERSION}", './infra/nginx')
                }
            }
        }
        stage('push_to_repo') {
//             when {
//                 branch 'main'
//             }
            steps {
                script {
                    loginDocker REPO
                }
                script {
                    pushImage("${REPO}/airbot:${env.CURRENT_VERSION}")
                }
                script {
                    pushImage("${REPO}/airnginx:${env.CURRENT_VERSION}")
                }
            }
        }
    }
    post {
        success {
            sh "docker rmi ${REPO}/airbot:${env.CURRENT_VERSION}"
            sh "docker rmi ${REPO}/airnginx:${env.CURRENT_VERSION}"
        }
    }
}