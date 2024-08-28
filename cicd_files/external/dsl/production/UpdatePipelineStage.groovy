import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = 'RPT-RC_Update-PipelineStage'

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        "This Job implements a function to update the Pipeline Stage of test environment in RPT.",
        "cicd_files/external/dsl/production/UpdatePipelineStage.groovy",
        "cicd_files/external/jenkins/production/UpdatePipelineStage.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.customerSlave())
        stringParam(externalParams.envName())
        stringParam(externalParams.flowUrl())
        stringParam(externalParams.spinnakerPipelineId())
        stringParam(externalParams.retryTimeout())
    }
    disabled(false)
    keepDependencies(false)
    logRotator{
        daysToKeep(25)
        numToKeep(100)
    }

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
            scriptPath('cicd_files/external/jenkins/production/UpdatePipelineStage.Jenkinsfile')
        }
    }
}
