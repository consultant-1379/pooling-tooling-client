pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Unreserve Environment') {
            steps {
                sh '''
                docker run --user "$(id -u):$(id -g)" --rm --name rpt-rc-"\${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                unreserve-environment -t \${ENV_NAME} --verbose \
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