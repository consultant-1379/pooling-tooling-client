#!/usr/bin/env groovy

def bob = "bob/bob -r \${WORKSPACE}/cicd_files/jenkins/rulesets/BuildAndPublish.yaml"

pipeline {
    agent {
        node {
            label SLAVE
        }
    }

    stages {
        stage('Cleaning Git Repo') {
            steps {
                sh 'git clean -xdff'
                sh 'git submodule sync'
                sh 'git submodule update --init --recursive'
            }
        }
        stage('Bump Pooling Tooling Client Tool Version') {
            steps {
                sh "${bob} set-pooling-tooling-client-env-variables bump-service-version"
                script {
                    env.IMAGE_VERSION = readFile('artifact.properties').trim()
                }
            }
        }
        stage('Build Pooling Tooling Client Tool') {
            steps {
                sh "${bob} build-docker-image"
            }
        }
        stage('Publish Pooling Tooling Client Tool') {
            steps {
                sh "${bob} publish-docker-image clean-up-docker-image"
            }
        }
        stage('Add changes to Version file of Pooling Tooling Client Tool') {
            steps {
                sh "${bob} add-changes-to-version-file"
            }
        }
        stage('Bump Python Precode Review Image Version') {
            steps {
                sh "${bob} set-python-precode-env-variables bump-service-version"
                script {
                    env.IMAGE_VERSION = readFile('artifact.properties').trim()
                }
            }
        }
        stage('Build Python Precode Review Image') {
            steps {
                sh "${bob} build-docker-image"
            }
        }
        stage('Publish Python Precode Review Image') {
            steps {
                sh "${bob} publish-docker-image clean-up-docker-image"
            }
        }
        stage('Add changes to Version file of Python Precode Review Image') {
            steps {
                sh "${bob} add-changes-to-version-file"
            }
        }
        stage('Push up changes to version files') {
            steps {
                sh "${bob} push-changes-to-version-files"
            }
        }
        stage('Archive artifact properties file') {
            steps {
                archiveArtifacts artifacts: 'artifact.properties', onlyIfSuccessful: true
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
