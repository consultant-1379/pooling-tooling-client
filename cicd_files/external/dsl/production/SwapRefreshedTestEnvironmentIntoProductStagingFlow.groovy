import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = 'RPT-RC_Swap_Refreshed_Test_Environment_into_Product_Staging_Flow'

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        """This Job is to swap a refreshed test environment into the Product Staging flow. It does this by first updating the freshest
        <br/>'Standby' test environment to 'Available', then swapping it into the Product Staging flow pool and swapping out the
        <br/>former current test environment to the 'Standby' pool.""",
        "cicd_files/external/dsl/production/SwapRefreshedTestEnvironmentIntoProductStagingFlow.groovy",
        "cicd_files/external/jenkins/production/SwapRefreshedTestEnvironmentIntoProductStagingFlow.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.customerSlave())
        stringParam(externalParams.currentEnvName())
        stringParam(externalParams.standbyPoolName())
        stringParam(externalParams.psoFlowPoolName())
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
            scriptPath('cicd_files/external/jenkins/production/SwapRefreshedTestEnvironmentIntoProductStagingFlow.Jenkinsfile')
        }
    }
}
