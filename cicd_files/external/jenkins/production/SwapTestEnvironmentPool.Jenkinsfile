pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Swapping test environment from and to a specified pool') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                --name rpt-rc-"${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                swap-test-environment-pool --verbose \
                -t ${ENV_NAME} -op ${POOL_TO_SWAP_ENVIRONMENT_FROM} -np ${POOL_TO_SWAP_ENVIRONMENT_TO} \
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