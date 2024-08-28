pipeline {
  agent {
      node {
            label SLAVE
        }
    }
    parameters {
        string(name: 'SLAVE',
               defaultValue: 'RPT_CICD',
               description: 'Name of the slave to use.')
        string(name: 'ENV_NAME',
               defaultValue: '',
               description: 'Name of the test environment to update the Pipeline Stage of.')
        string(name: 'FLOW_URL',
               defaultValue: '',
               description: 'Pipeline URL')
    }
    stages {
        stage('Update Pipeline Stage') {
            steps {
                sh '''
                #!/bin/bash -xe
                docker run --user "$(id -u):$(id -g)" --rm -v \${PWD}:/usr/src/app/out \
                --name rpt-rc-"\${BUILD_TAG}" \
                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                update-test-environment-stage --verbose  --dev_mode \
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