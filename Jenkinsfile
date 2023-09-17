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
                    env.CURRENT_VERSION = sh(script: 'cat ./airbot/Dockerfile | grep "LABEL version" | cut -d "=" -f2', returnStdout: true).trim()
                    echo "Old version from Dockerfile: ${env.CURRENT_VERSION}"

                    def changeType = 'patch'
                    if (BRANCH_NAME == 'main') {
                        changeType = 'minor'
                    } else {
                        changeType = 'patch'
                    }

                    if (changeType == 'minor') {
                        def versionParts = env.CURRENT_VERSION.tokenize('.')
                        def newMinorVersion = versionParts[1].toInteger() + 1
                        env.CURRENT_VERSION = "${versionParts[0]}.${newMinorVersion}.${versionParts[2]}"
                    } else if (changeType == 'patch') {
                        def versionParts = env.CURRENT_VERSION.tokenize('.')
                        def newPatchVersion = versionParts[2].toInteger() + 1
                        env.CURRENT_VERSION = "${versionParts[0]}.${versionParts[1]}.${newPatchVersion}"
                    }
                    echo "New version: ${env.CURRENT_VERSION}"
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