pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Updating status for freshest Standby Test Environment to Available') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                --name rpt-rc-"${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                update-freshest-standby-test-environment-to-available --verbose \
                -pl ${STANDBY_POOL_NAME} --generate_artifact_properties \
                --retry_timeout ${RETRY_TIMEOUT}
                '''
            }
        }
        stage('Archive artifact properties file') {
            steps {
                archiveArtifacts artifacts: 'artifact.properties', onlyIfSuccessful: true
            }
        }
        stage('Swapping in Available Test Environment') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/in \
                --name rpt-rc-"${BUILD_TAG}"-swap \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                swap-in-available-environment-swap-out-current-environment --verbose \
                -t ${CURRENT_ENV_NAME} -op ${STANDBY_POOL_NAME} -np ${PSO_FLOW_POOL_NAME} \
                --retry_timeout ${RETRY_TIMEOUT}
                '''
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