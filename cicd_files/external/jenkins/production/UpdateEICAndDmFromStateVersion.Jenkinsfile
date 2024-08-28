pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Updating EIC and DM FromState version for test environment') {
            steps {
                script {
                    def exempt = ["SLAVE", "ENV_NAME", "RETRY_TIMEOUT"];
                    params.each { key, value ->
                        node(SLAVE) {
                            if (!exempt.contains(key) && value != "") {
                                env[key] = value
                                sh '''
                                #!/bin/bash -xe
                                docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/out \
                                --name rpt-rc-"${BUILD_TAG}" \
                                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
                                store-test-environment-details --verbose \
                                -t ${ENV_NAME} --request_body '{ "properties": { "''' + key + '''":"''' + value + '''"}}' \
                                --retry_timeout ${RETRY_TIMEOUT}
                                '''
                            }
                        }
                    }
                }
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