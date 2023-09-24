#!/usr/bin/env groovy

@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        REPO = 'lordot'
        CREDS = credentials('docker-hub')
        BRANCH = "k8s"
    }
    stages {
        stage('increment_version') {
            steps {
                script {
                    incrementPatchVersion "./airbot"
                }
            }
        }
        stage('build_docker') {
            steps {
                script {
                    buildImage("${REPO}/airbot:${env.CURRENT_VERSION}", './airbot')
                }
            }
        }
        stage('push_to_repo') {
//             when {
//                 branch 'main'
//             }
            steps {
                script {
                    sh "echo $CREDS_PSW | docker login -u $CREDS_USR --password-stdin"
                }
                script {
                    pushImage("${REPO}/airbot:${env.CURRENT_VERSION}")
                }
            }
        }
        stage('deploy') {
            steps {
                script {
                    echo 'deploying kubernetes pods...'
                    withKubeConfig([credentialsId: 'lke-configfile', restrictKubeConfigAccess: 'true', serverUrl: 'https://06689cbd-962c-42c5-bb54-8bef03b752ae.eu-central-1.linodelke.net']) {
                        sh 'kubectl get nodes'
                        sh 'helmfile apply -f ./helm/helmfile.yaml'
                    }
                }
            }
        }
        stage('commit version update') {
            steps {
                withCredentials([gitUsernamePassword(credentialsId: 'lordot-github', gitToolName: 'Default')]) {
//                     sh 'git config --global user.email "jenkins@example.com"'
//                     sh 'git config --global user.name "jenkins"'
                    sh 'git add .'
                    sh 'git commit -m "ci: version bump"'
                    sh "git push origin HEAD:${BRANCH}"
                }
            }
        }
    }
    post {
        success {
            sh "docker rmi ${REPO}/airbot:${env.CURRENT_VERSION}"
        }
    }
}