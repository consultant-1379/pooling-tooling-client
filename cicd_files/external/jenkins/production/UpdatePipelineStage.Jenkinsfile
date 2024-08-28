pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Update Pipeline Stage') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v \${PWD}:/usr/src/app/out \
                --name rpt-rc-"\${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                update-test-environment-stage --verbose \
                -t "\${ENV_NAME}" -ps "\${FLOW_URL}" \
                --retry_timeout ${RETRY_TIMEOUT} || exit 1
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