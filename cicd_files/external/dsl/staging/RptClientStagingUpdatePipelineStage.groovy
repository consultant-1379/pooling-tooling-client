import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = "resource-pooling-tool-client_Staging_Update_PipelineStage"

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        "This Job implements a function to update the Pipeline Stage of test environment in RPT Staging.",
        "cicd_files/external/dsl/staging/RptClientStagingUpdatePipelineStage.groovy",
        "cicd_files/external/jenkins/staging/UpdatePipelineStage.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.slave())
        stringParam(externalParams.envName())
        stringParam(externalParams.flowUrl())
        stringParam(externalParams.spinnakerPipelineId())
        stringParam(externalParams.retryTimeout())
    }
    disabled(false)
    keepDependencies(false)
    logRotator(commonSteps.defaultLogRotatorValues())

    definition {
        cpsScm {
            scm {
                git {
                    branch('master')
                    remote {
                        url(commonParams.repoUrl())
                    }
                    extensions {
                        cleanBeforeCheckout()
                        localBranch 'master'
                    }
                }
            }
            scriptPath("cicd_files/external/jenkins/staging/UpdatePipelineStage.Jenkinsfile")
        }
    }
}
