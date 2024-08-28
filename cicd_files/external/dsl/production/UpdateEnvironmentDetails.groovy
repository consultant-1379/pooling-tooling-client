import common_classes.CommonSteps
import common_classes.CommonParameters
import common_classes.ExternalParameters

CommonSteps commonSteps = new CommonSteps()
CommonParameters commonParams = new CommonParameters()
ExternalParameters externalParams = new ExternalParameters()

def pipelineBeingGeneratedName = 'RPT-RC_Update-Environment-Details'

pipelineJob(pipelineBeingGeneratedName) {
    description(commonSteps.defaultJobDescription(pipelineBeingGeneratedName,
        "This Job is to update the properties of a test environment in RPT.",
        "cicd_files/external/dsl/production/UpdateEnvironmentDetails.groovy",
        "cicd_files/external/jenkins/production/UpdateEnvironmentDetails.Jenkinsfile"
    ))

    parameters {
        stringParam(commonParams.customerSlave())
        stringParam(externalParams.envName())
        stringParam(externalParams.spinnakerPipelineId())
        stringParam(externalParams.platformType())
        stringParam(externalParams.kubeconfigFile())
        stringParam(externalParams.pathToCertificatesFiles())
        stringParam(externalParams.eicHostname())
        stringParam(externalParams.gasHostname())
        stringParam(externalParams.iamHostname())
        stringParam(externalParams.pfHostname())
        stringParam(externalParams.soHostname())
        stringParam(externalParams.udsHostname())
        stringParam(externalParams.vnfmHostname())
        stringParam(externalParams.adcHostname())
        stringParam(externalParams.mlHostname())
        stringParam(externalParams.appmgrHostname())
        stringParam(externalParams.kfBoHostname())
        stringParam(externalParams.pathToCertificatesFilesIccr())
        stringParam(externalParams.vnfmHostnameIccr())
        stringParam(externalParams.soHostnameIccr())
        stringParam(externalParams.pfHostnameIccr())
        stringParam(externalParams.udsHostnameIccr())
        stringParam(externalParams.vnfmRegistryHostnameIccr())
        stringParam(externalParams.iamHostnameIccr())
        stringParam(externalParams.gasHostnameIccr())
        stringParam(externalParams.adcHostnameIccr())
        stringParam(externalParams.iccrIp())
        stringParam(externalParams.version())
        stringParam(externalParams.dockerRegistry())
        stringParam(externalParams.dockerRegistryCredentials())
        stringParam(externalParams.namespace())
        stringParam(externalParams.serviceMeshLoadBalancerIp())
        stringParam(externalParams.k6TestwareVersion())
        stringParam(externalParams.fromStateTags())
        stringParam(externalParams.kubeConfig())
        stringParam(externalParams.iamAuthenticator())
        stringParam(externalParams.isEcn())
        stringParam(externalParams.pathToAwsFiles())
        stringParam(externalParams.pathToSiteValues())
        stringParam(externalParams.pathToValues())
        stringParam(externalParams.pathToEnmConfig())
        stringParam(externalParams.pathToEocmConfig())
        stringParam(externalParams.eoSoHostname())
        stringParam(externalParams.eoPfHostname())
        stringParam(externalParams.eoUdsHostname())
        stringParam(externalParams.eoGasHostname())
        stringParam(externalParams.eoHelmRegistryHostname())
        stringParam(externalParams.backupServer())
        stringParam(externalParams.pathToWorkdir())
        stringParam(externalParams.awsEcrUrl())
        stringParam(externalParams.awsRegion())
        stringParam(externalParams.tags())
        stringParam(externalParams.osHostname())
        stringParam(externalParams.taHostname())
        stringParam(externalParams.thHostname())
        stringParam(externalParams.broPvcSize())
        stringParam(externalParams.dataSearchEnginePvcSize())
        stringParam(externalParams.sysGasSoPfUdsCpsCtsDmiRtaFaA1CredentialId())
        stringParam(externalParams.kubeconfigFileCredentialId())
        stringParam(externalParams.awsConfigFileCredentialId())
        stringParam(externalParams.awsCredsFileCredentialId())
        stringParam(externalParams.aaSCloudProviderType())
        stringParam(externalParams.pathToFromStateSiteValuesOverrideFile())
        stringParam(externalParams.pathToToStateSiteValuesOverrideFile())
        stringParam(externalParams.pathToFromStateSiteValuesFile())
        stringParam(externalParams.pathToToStateSiteValuesFile())
        stringParam(externalParams.enmHostname())
        stringParam(externalParams.ecmHostname())
        stringParam(externalParams.skipTests())
        stringParam(externalParams.fromSkipTests())
        stringParam(externalParams.runTests())
        stringParam(externalParams.configFiles())
        stringParam(externalParams.fromConfigFiles())
        stringParam(externalParams.fhSnmpAlarmIp())
        stringParam(externalParams.laHostname())
        stringParam(externalParams.bdrHostname())
        stringParam(externalParams.envConfigFile())
        stringParam(externalParams.backupServerCredential())
        stringParam(externalParams.backupServerRemotePath())
        stringParam(externalParams.restsimHost())
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
            scriptPath('cicd_files/external/jenkins/production/UpdateEnvironmentDetails.Jenkinsfile')
        }
    }
}
