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
                    def currentVersion = sh(script: 'cat ./airbot/Dockerfile | grep "LABEL version" | cut -d "=" -f2', returnStdout: true).trim()
                    echo "Old version from Dockerfile: ${currentVersion}"

                    def changeType = 'patch'
                    if (BRANCH_NAME == 'main') {
                        changeType = 'minor'
                    } else {
                        changeType = 'patch'
                    }

                    if (changeType == 'minor') {
                        def versionParts = currentVersion.tokenize('.')
                        def newMinorVersion = versionParts[1].toInteger() + 1
                        currentVersion = "${versionParts[0]}.${newMinorVersion}.${versionParts[2]}"
                    } else if (changeType == 'patch') {
                        def versionParts = currentVersion.tokenize('.')
                        def newPatchVersion = versionParts[2].toInteger() + 1
                        currentVersion = "${versionParts[0]}.${versionParts[1]}.${newPatchVersion}"
                    }
                    echo "New version: ${currentVersion}"
                }
            }
        }
            }
        }
        stage('build_docker') {
            steps {
                script {
                    buildImage("${REPO}/airbot:${currentVersion}", './airbot')
                }
                script {
                   buildImage("${REPO}/airnginx:${currentVersion}", './infra/nginx')
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
                    pushImage("${REPO}/airbot:${currentVersion}")
                }
                script {
                    pushImage("${REPO}/airnginx:${currentVersion}")
                }
            }
        }
    }
    post {
        success {
            sh "docker rmi ${REPO}/airbot:${currentVersion}"
            sh "docker rmi ${REPO}/airnginx:${currentVersion}"
        }
    }
}