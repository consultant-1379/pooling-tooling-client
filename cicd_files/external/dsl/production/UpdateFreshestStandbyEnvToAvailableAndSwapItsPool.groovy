import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = 'RPT-RC_Update_Freshest_Standby_Environment_To_Available_And_Swap_Pool'

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        "This Job is to update the freshest standby environment in a pool to available and swap it into a new pool.",
        "cicd_files/external/dsl/production/UpdateFreshestStandbyEnvToAvailableAndSwapItsPool.groovy",
        "cicd_files/external/jenkins/production/UpdateFreshestStandbyEnvToAvailableAndSwapItsPool.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.customerSlave())
        stringParam(externalParams.poolContainingStandbyEnv())
        stringParam(externalParams.poolToSwapFreshestEnvTo())
        stringParam(externalParams.spinnakerPipelineId())
        stringParam(externalParams.retryTimeout())
    }
    disabled(false)
    keepDependencies(false)
    logRotator(commonSteps.defaultLogRotatorValues())
    properties {
        disableConcurrentBuilds {
            abortPrevious(false)
        }
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
            scriptPath('cicd_files/external/jenkins/production/UpdateFreshestStandbyEnvToAvailableAndSwapItsPool.Jenkinsfile')
        }
    }
}
