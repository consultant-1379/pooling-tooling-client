import common_classes.CommonSteps
import common_classes.CommonParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()


def pipelineBeingGeneratedName = "resource-pooling-tool-client_Build_And_Publish"
pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
            """This pipeline builds the image for the Pooling Tooling Client. It then publishes the image to the armdocker JFrog artifactory.
            <br/>Artifact Published at <a href='https://armdocker.rnd.ericsson.se/artifactory/proj-eric-oss-dev-test-docker-global/proj-eric-oss-dev-test/pooling_tooling_client/'>proj-eric-oss-dev-test/pooling_tooling_client</a>""",
            "cicd_files/dsl/pipeline_jobs/BuildAndPublish.groovy",
            "cicd_files/jenkins/files/pipeline_jobs/BuildAndPublish.Jenkinsfile",
            "cicd_files/jenkins/rulesets/BuildAndPublish.yaml"
        ))
    keepDependencies(false)
    logRotator(commonSteps.defaultLogRotatorValues())
    parameters {
        stringParam(commonParams.slave())
    }
     blockOn("resource-pooling-tool-client_Pre_Code_Review", {
        blockLevel('GLOBAL')
        scanQueueFor('DISABLED')
    })

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
                        name('gcn')
                        url(commonParams.repoUrl())
                    }
                    extensions {
                        cleanBeforeCheckout()
                        localBranch 'master'
                    }
                }
            }
            scriptPath('cicd_files/jenkins/files/pipeline_jobs/BuildAndPublish.Jenkinsfile')
        }
    }
    quietPeriod(5)
    disabled(false)
}
