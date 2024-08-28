pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Retrieve Environment Details') {
            steps {
                sh '''
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                --name rpt-rc-"${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                retrieve-test-environment-details --verbose --generate_artifact_properties \
                -t "${ENV_NAME}" \
                --retry_timeout ${RETRY_TIMEOUT}
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