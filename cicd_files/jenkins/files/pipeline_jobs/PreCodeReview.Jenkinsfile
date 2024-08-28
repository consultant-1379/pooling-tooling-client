#!/usr/bin/env groovy

def bob = "bob/bob -r \${WORKSPACE}/cicd_files/jenkins/rulesets/PreCodeReview.yaml"

pipeline {
    agent {
        label SLAVE
    }
    environment {
        CHANGED_PYTHON_FILES = sh(returnStdout: true, script: "git diff-tree --diff-filter=ACM --no-commit-id --name-only -r $GIT_COMMIT -- 'rptrc/*.py'").replaceAll("\\n", " ")
    }
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage('Clean Workspace') {
            steps {
                sh 'git clean -xdff'
                sh 'git submodule sync'
                sh 'git submodule update --init --recursive'
            }
        }
        stage('Python changed files linting'){
            when {
                expression
                    { env.CHANGED_PYTHON_FILES != null }
            }
            steps {
                script {
                    try {
                        sh "${bob} run-python-linting"
                        echo "======================"
                        echo "Python linting passed!"
                        echo "======================"
                    } catch(error) {
                        echo "+++++++++++++++++++++++++++++++++++++++++++"
                        echo "Linting errors detected. Please check above"
                        echo "+++++++++++++++++++++++++++++++++++++++++++"
                        currentBuild.result = "FAILURE"
                    }
                }
                sh 'echo -e "\n"'
            }
        }
        stage('Python unit testing') {
            steps {
                script {
                    try {
                        sh "${bob} run-python-unit-tests"
                        sh '''
                        echo "========================="
                        echo "Python unit tests passed!"
                        echo "========================="
                        '''
                    } catch(error) {
                        sh '''
                        echo "++++++++++++++++++++++++++++++++++++++++++++"
                        echo "Python unit tests failed. Please check above"
                        echo "++++++++++++++++++++++++++++++++++++++++++++"
                        '''
                        currentBuild.result = "FAILURE"
                    }
                }
                sh 'echo -e "\n"'
            }
        }
        stage('Python SonarQube analysis') {
            environment {
                SONARQUBE_TOKEN = credentials('TB_SONAR_NEW')
            }
            steps {
                script {
                    try {
                        withSonarQubeEnv('SonarQubeNew') {
                            sh "${bob} run-python-sonarqube-analysis"
                        }
                        echo "====================================="
                        echo "Python SonarQube analysis successful!"
                        echo "====================================="

                    } catch(error) {
                        echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                        echo "Python SonarQube analysis has failed. Please check above"
                        echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                        currentBuild.result = "FAILURE"
                    }
                }
                sh 'echo -e "\n"'
            }
        }
        stage('Python SonarQube Quality Gate') {
            options {
                retry(5)
            }
            steps {
                timeout(time: 30, unit: 'SECONDS') {
                    script {
                        if (waitForQualityGate().status != "OK") {
                            currentBuild.result = "FAILURE"
                        } else {
                            currentBuild.result = "SUCCESS"
                        }
                        sleep(5)
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
