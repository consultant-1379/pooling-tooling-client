def getDslParamaters() {
    return [SLAVE: env.SLAVE]
}

def getPipelineJobList() {
    def pipelineJobList = []

    pipelineJobList.add("cicd_files/dsl/pipeline_jobs/BuildAndPublish.groovy")
    pipelineJobList.add("cicd_files/dsl/pipeline_jobs/PreCodeReview.groovy")

    pipelineJobList.add('cicd_files/external/dsl/production/CheckIfEnvironmentOnLatestEICVersion.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/QuarantineEnvironment.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/ReserveEnvironment.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UnreserveEnvironment.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdatePipelineStage.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdateTestEnvironmentStatus.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdateEICAndDmFromStateVersion.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdateFromStateByPool.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/RetrieveEnvironmentDetails.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/SwapRefreshedTestEnvironmentIntoProductStagingFlow.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdateEnvironmentDetails.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/SwapTestEnvironmentPool.groovy')
    pipelineJobList.add('cicd_files/external/dsl/production/UpdateFreshestStandbyEnvToAvailableAndSwapItsPool.groovy')

    pipelineJobList.add('cicd_files/external/dsl/staging/RptClientStagingQuarantine.groovy')
    pipelineJobList.add('cicd_files/external/dsl/staging/RptClientStagingReserve.groovy')
    pipelineJobList.add('cicd_files/external/dsl/staging/RptClientStagingUnreserve.groovy')
    pipelineJobList.add('cicd_files/external/dsl/staging/RptClientStagingUpdatePipelineStage.groovy')

    pipelineJobList.add('cicd_files/dsl/pipeline_operations/PipelineGenerator.groovy')
    pipelineJobList.add('cicd_files/dsl/pipeline_operations/PipelineUpdater.groovy')

    return pipelineJobList.join('\n')
}

pipeline {
    agent {
        node {
            label SLAVE
        }
    }

    environment {
        DSL_CLASSPATH = 'cicd_files/dsl'
    }
    stages {
        stage ('Validate required parameters set') {
            when {
                expression {
                    env.SLAVE == null
                }
            }
            steps {
                error('Required parameter(s) not set. Please provide a value for all required parameters')
            }
        }

        stage ('Generate RPT Client Pipeline Jobs') {
            steps {
                jobDsl targets: getPipelineJobList(),
                additionalParameters: getDslParamaters(),
                additionalClasspath: env.DSL_CLASSPATH
            }
        }

        stage ('Update RPT Client List View') {
            steps {
                jobDsl targets: 'cicd_files/dsl/pipeline_views/View.groovy'
            }
        }
    }

    post {
        success {
            build propagate: true, wait: true, job: 'resource-pooling-tool-client_Build_And_Publish'
        }
        always {
            cleanWs()
        }
    }
}
