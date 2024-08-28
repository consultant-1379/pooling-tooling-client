pipeline {
  agent {
    label SLAVE
  }
  stages {
    stage('Reserve Environment') {
      steps {
          sh """ \
          docker run --user "\$(id -u):\$(id -g)" --rm -v \${PWD}:/usr/src/app/out --name rpt-rc-${BUILD_TAG} \
          armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
          create-queued-request \
              --verbose \
              --generate_artifact_properties \
              --request_body '{
                  "poolName": "${ENV_LABEL}",
                  "requestorDetails": { \
                      "name": "${FLOW_URL_TAG}",
                      "area": "IDUN",
                      "executionId": "${FLOW_URL}"
                  },
                  "status": "Queued",
                  "requestTimeout": ${REQUEST_TIMEOUT}
              }' \
              --pipeline_stage "${FLOW_URL}" \
              --logging_identifier "${FLOW_URL_TAG}" \
              --retry_timeout ${RETRY_TIMEOUT} || exit 1
          """
      }
    }
    stage('Archive artifact properties file') {
        steps {
            archiveArtifacts artifacts: 'artifact.properties', onlyIfSuccessful: true
        }
    }
  }
  post {
    aborted {
      sh '''
      docker run --user "$(id -u):$(id -g)" --rm -v ${PWD}:/usr/src/app/in --name rpt-rc-cleanup-"${BUILD_TAG}" \
      armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest \
      abort-queued-request --verbose --dev_mode \
      --retry_timeout ${RETRY_TIMEOUT}
      '''
    }
    cleanup {
      sh 'docker rmi -f armdocker.rnd.ericsson.se/proj-eric-oss-dev-test/pooling_tooling_client:latest || true'
    }
    always {
      cleanWs()
    }
  }
}