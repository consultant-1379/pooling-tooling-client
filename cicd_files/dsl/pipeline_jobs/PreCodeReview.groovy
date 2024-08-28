import common_classes.CommonSteps
import common_classes.CommonParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()

def pipelineBeingGeneratedName = 'resource-pooling-tool-client_Pre_Code_Review'
pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
            "This pipeline is to run the precode Review for Pooling Tooling Client.",
            "cicd_files/dsl/pipeline_jobs/PreCodeReview.groovy",
            "cicd_files/jenkins/files/pipeline_jobs/PreCodeReview.Jenkinsfile",
            "cicd_files/jenkins/rulesets/PreCodeReview.yaml"
        ))
    disabled(false)
    keepDependencies(false)
    logRotator(commonSteps.defaultLogRotatorValues())
    parameters {
        stringParam(commonParams.slave())
    }

    triggers {
        gerrit {
            project(commonParams.repo(), 'master')
            events {
                patchsetCreated()
            }
        }
    }

    definition {
        cpsScm {
            scm {
                git {
                    branch('\${GERRIT_PATCHSET_REVISION}')
                    remote {
                        name('gcn')
                        url(commonParams.repoUrl())
                        refspec('\${GERRIT_REFSPEC}')
                    }
                    extensions {
                        choosingStrategy {
                            gerritTrigger()
                        }
                        cleanBeforeCheckout()
                    }
                }
            }
            scriptPath('cicd_files/jenkins/files/pipeline_jobs/PreCodeReview.Jenkinsfile')
        }
    }
    quietPeriod(5)
}