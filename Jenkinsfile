#!/usr/bin/env groovy

@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        REPO = '165.22.80.137:8083'
        CREDS = credentials('nexus-user')
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
        stage('deploy') {
            steps {
                script {
                    echo 'deploying kubernetes pods...'
                    withKubeConfig([credentialsId: 'lke-configfile', serverUrl: 'https://06689cbd-962c-42c5-bb54-8bef03b752ae.eu-central-1.linodelke.net']) {
                        sh 'kubectl get nodes'
                        sh 'helmfile sync -f ./helm/helmfile.yaml'
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
            sh "docker rmi ${REPO}/airnginx:${env.CURRENT_VERSION}"
        }
    }
}