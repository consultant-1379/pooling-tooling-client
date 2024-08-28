pipeline {
    agent {
        node {
            label SLAVE
        }
    }
    stages {
        stage('Pull RPT-RC image') {
            steps {
                sh '''
                docker pull armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest
                '''
            }
        }
        stage('Updating properties for test environment') {
            steps {
                script {
                    def exempt = ["SLAVE", "ENV_NAME", "SPINNAKER_PIPELINE_ID", "RETRY_TIMEOUT"];
                    params.each { key, value ->
                        if (!exempt.contains(key) && value != "") {
                            env[key] = value
                            if (key == "configFiles" || key == "fromConfigFiles") {
                                sh '''
                                #!/bin/bash -xe
                                docker run --user "$(id -u):$(id -g)" --rm -v \${PWD}:/usr/src/app/out \\
                                --name rpt-rc-"\${BUILD_TAG}" \\
                                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \\
                                store-test-environment-details --verbose \\
                                -t \${ENV_NAME} --request_body '{ "properties": { "''' + key + '''":''' + value + '''}}' \\
                                --retry_timeout ${RETRY_TIMEOUT}
                                '''
                            } else {
                                sh '''
                                #!/bin/bash -xe
                                docker run --user "$(id -u):$(id -g)" --rm -v \${PWD}:/usr/src/app/out \\
                                --name rpt-rc-"\${BUILD_TAG}" \\
                                armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \\
                                store-test-environment-details --verbose \\
                                -t \${ENV_NAME} --request_body '{ "properties": { "''' + key + '''":"''' + value + '''"}}' \\
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