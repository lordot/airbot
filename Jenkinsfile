#!/usr/bin/env groovy

@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        REPO = 'lordot'
        CREDS = credentials('docker-hub')
        BRANCH = 'k8s'
        REGION = 'eu-north-1'
        CLUSTER_NAME = 'dev-cluster'
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
        stage('provision') {
            environment {
                AWS_ACCESS_KEY_ID=credentials('aws_access_key_id')
                AWS_SECRET_ACCESS_KEY=credentials('aws_secret_key')
                AWS_DEFAULT_REGION="$REGION"
                TF_VAR_region="$REGION"
                TF_VAR_cluster_name="$CLUSTER_NAME"
            }
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform init'
                        sh 'terraform apply --auto-approve' // TODO add to wait until all up
                    }
                }
            }
        }
        stage('deploy') {
            steps {
                script {
                    echo 'deploying kubernetes pods...'

                    sh "aws eks --region ${REGION} update-kubeconfig --name ${CLUSTER_NAME}"
                    sh 'kubectl get nodes'
                    sh 'helmfile apply -f ./helm/helmfile.yaml'
                }
            }
        }
//         stage('commit version update') {
//             steps {
//                 withCredentials([gitUsernamePassword(credentialsId: 'lordot-github', gitToolName: 'Default')]) {
//                     sh 'git add .'
//                     sh 'git commit -m "ci: version bump"'
//                     sh "git push origin HEAD:${BRANCH}"
//                 }
//             }
//         }
    }
    post {
        success {
            sh "docker rmi ${REPO}/airbot:${env.CURRENT_VERSION}"
        }
    }
}