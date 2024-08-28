import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = 'RPT-RC_Unreserve-Environment'

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        "This Job implements a function to unreserve a test environment in RPT.",
        "cicd_files/external/dsl/production/UnreserveEnvironment.groovy",
        "cicd_files/external/jenkins/production/UnreserveEnvironment.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.customerSlave())
        stringParam(externalParams.envName())
        stringParam(externalParams.spinnakerPipelineId())
        stringParam(externalParams.retryTimeout())
    }

    logRotator{
        daysToKeep(25)
        numToKeep(100)
    }

    disabled(false)

    keepDependencies(false)

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
            scriptPath('cicd_files/external/jenkins/production/UnreserveEnvironment.Jenkinsfile')
        }
    }
}
