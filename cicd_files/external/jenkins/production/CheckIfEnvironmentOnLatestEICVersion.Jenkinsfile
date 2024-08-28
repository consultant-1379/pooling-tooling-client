pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Check version on test environment') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                --name rpt-rc-"${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                check-if-version-specified-equals-version-on-test-environment -t ${ENV_NAME} \
                --version_for_comparison ${version_for_comparison} --verbose \
                --retry_timeout ${RETRY_TIMEOUT} \
                --generate_artifact_properties
                '''
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
            sh 'docker rmi -f armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest || true'
            cleanWs()
        }
    }
}