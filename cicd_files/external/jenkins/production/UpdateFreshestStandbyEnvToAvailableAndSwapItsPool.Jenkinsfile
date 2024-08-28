pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Updating status for freshest Standby Test Environment to Available and swapping its pool') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                --name rpt-rc-"${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                update-freshest-standby-env-to-available-and-swap-its-pool --verbose --generate_artifact_properties\
                -op ${POOL_CONTAINING_STANDBY_ENV} -np ${POOL_TO_SWAP_FRESHEST_ENV_TO} \
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