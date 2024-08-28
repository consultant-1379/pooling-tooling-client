package common_classes

/**
 * Class containing External groovy parameters
 */
class ExternalParameters {

    static List envName(String defaultValue='') {
        return ['ENV_NAME', defaultValue, 'Name of the test environment']
    }

    static List versionForComparison(String defaultValue='') {
        return ['version_for_comparison', defaultValue, 'This is the latest EIC version.']
    }

    static List envLabel(String defaultValue='') {
        return ['ENV_LABEL', defaultValue, 'Name of the Environment Label (Pool name) to search against']
    }

    static List flowUrlTag(String defaultValue='Spinnaker') {
        return ['FLOW_URL_TAG', defaultValue, 'Name for the Flow to be used for the URL to append to the Jenkins Job']
    }

    static List flowUrl(String defaultValue='') {
        return ['FLOW_URL', defaultValue, 'Pipeline URL']
    }

    static List requestTimeout(String defaultValue='7200000') {
        return ['REQUEST_TIMEOUT', defaultValue, 'The timeout for the Queued Requests (in ms). Default is 2 hours.']
    }

    static List fromState(String defaultValue='') {
        return ['fromState', defaultValue, 'The from state software of the environment.']
    }

    static List dmFromState(String defaultValue='') {
        return ['dmFromState', defaultValue, 'The Deployment Manager from state version to use for deployment operations.']
    }

    static List platformType(String defaultValue='') {
        return ['platformType', defaultValue, 'The platform type of this test environment, e.g.: RH, Azure, AWS.']
    }

    static List kubeconfigFile(String defaultValue='') {
        return ['kubeconfigFile', defaultValue, 'The kubeconfig file path for this test environment.']
    }

    static List pathToCertificatesFiles(String defaultValue='') {
        return ['pathToCertificatesFiles', defaultValue, 'The cert files path for this test environment.']
    }

    static List gasHostname(String defaultValue='') {
        return ['gasHostname', defaultValue, 'The GAS hostname for this test environment.']
    }

    static List iamHostname(String defaultValue='') {
        return ['iamHostname', defaultValue, 'The IAM hostname for this test environment.']
    }

    static List pfHostname(String defaultValue='') {
        return ['pfHostname', defaultValue, 'The PF hostname for this test environment.']
    }

    static List soHostname(String defaultValue='') {
        return ['soHostname', defaultValue, 'The SO hostname for this test environment.']
    }

    static List udsHostname(String defaultValue='') {
        return ['udsHostname', defaultValue, 'The UDS hostname for this test environment.']
    }

    static List vnfmHostname(String defaultValue='') {
        return ['vnfmHostname', defaultValue, 'The VNFM hostname for this test environment.']
    }

    static List adcHostname(String defaultValue='') {
        return ['adcHostname', defaultValue, 'The ADC hostname for this test environment.']
    }

    static List appmgrHostname(String defaultValue='') {
        return ['appmgrHostname', defaultValue, 'The APPMGR hostname for this test environment.']
    }

    static List kfBoHostname(String defaultValue='') {
        return ['kfBoHostname', defaultValue, 'The Kafka Bootstrap hostname for this test environment']
    }

    static List pathToCertificatesFilesIccr(String defaultValue='') {
        return ['pathToCertificatesFilesIccr', defaultValue, 'The path to ICCR cert files for this test environment.']
    }

    static List vnfmHostnameIccr(String defaultValue='') {
        return ['vnfmHostnameIccr', defaultValue, 'The VNFM hostname for ICCR.']
    }

    static List soHostnameIccr(String defaultValue='') {
        return ['soHostnameIccr', defaultValue, 'The SO hostname for ICCR.']
    }

    static List pfHostnameIccr(String defaultValue='') {
        return ['pfHostnameIccr', defaultValue, 'The PF hostname for ICCR.']
    }

    static List udsHostnameIccr(String defaultValue='') {
        return ['udsHostnameIccr', defaultValue, 'The UDS hostname for ICCR.']
    }

    static List vnfmRegistryHostnameIccr(String defaultValue='') {
        return ['vnfmRegistryHostnameIccr', defaultValue, 'The VNFM registry hostname for ICCR.']
    }

    static List iamHostnameIccr(String defaultValue='') {
        return ['iamHostnameIccr', defaultValue, 'The IAM hostname for ICCR.']
    }

    static List gasHostnameIccr(String defaultValue='') {
        return ['gasHostnameIccr', defaultValue, 'The GAS hostname for ICCR.']
    }

    static List adcHostnameIccr(String defaultValue='') {
        return ['adcHostnameIccr', defaultValue, 'The ADC hostname for ICCR.']
    }

    static List iccrIp(String defaultValue='') {
        return ['iccrIp', defaultValue, 'The ICCR IP address']
    }

    static List version(String defaultValue='') {
        return ['version', defaultValue, 'Current Version of IDUN.']
    }

    static List dockerRegistry(String defaultValue='') {
        return ['dockerRegistry', defaultValue, 'Docker registry hostname.']
    }

    static List dockerRegistryCredentials(String defaultValue='') {
        return ['dockerRegistryCredentials', defaultValue, 'Credential ID for docker registry.']
    }

    static List namespace(String defaultValue='') {
        return ['namespace', defaultValue, 'The namespace in the cluster.']
    }

    static List serviceMeshLoadBalancerIp(String defaultValue='') {
        return ['serviceMeshLoadBalancerIp', defaultValue, 'Service Mesh load balancer IP address.']
    }

    static List k6TestwareVersion(String defaultValue='') {
        return ['k6TestwareVersion', defaultValue, 'K6 Testware Version.']
    }

    static List fromStateTags(String defaultValue='') {
        return ['fromStateTags', defaultValue, 'From state tags to be used with the fromState version.']
    }

    static List kubeConfig(String defaultValue='') {
        return ['kubeConfig', defaultValue, 'The kubeconfig file path for this test environment (for AAS).']
    }

    static List iamAuthenticator(String defaultValue='') {
        return ['iamAuthenticator', defaultValue, 'The IAM Authenticator (for AAS).']
    }

    static List isEcn(String defaultValue='') {
        return ['isEcn', defaultValue, 'Is the deployment Private or Public (for AAS).']
    }

    static List pathToAwsFiles(String defaultValue='') {
        return ['pathToAwsFiles', defaultValue, 'The file path for AWS (for AAS).']
    }

    static List pathToSiteValues(String defaultValue='') {
        return ['pathToSiteValues', defaultValue, 'The file path for site values (for AAS).']
    }

    static List pathToValues(String defaultValue='') {
        return ['pathToValues', defaultValue, 'The file path for values (for AAS).']
    }

    static List pathToEnmConfig(String defaultValue='') {
        return ['pathToEnmConfig', defaultValue, 'The file path for ENM Config (for AAS).']
    }

    static List pathToEocmConfig(String defaultValue='') {
        return ['pathToEocmConfig', defaultValue, 'The file path for EOCM Config (for AAS).']
    }

    static List eoSoHostname(String defaultValue='') {
        return ['eoSoHostname', defaultValue, 'The EO SO hostname (for AAS).']
    }

    static List eoPfHostname(String defaultValue='') {
        return ['eoPfHostname', defaultValue, 'The EO PF hostname (for AAS).']
    }

    static List eoUdsHostname(String defaultValue='') {
        return ['eoUdsHostname', defaultValue, 'The EO UDS hostname (for AAS).']
    }

    static List eoGasHostname(String defaultValue='') {
        return ['eoGasHostname', defaultValue, 'The EO GAS hostname (for AAS).']
    }

    static List eoHelmRegistryHostname(String defaultValue='') {
        return ['eoHelmRegistryHostname', defaultValue, 'The EO HELM REGISTRY hostname (for AAS).']
    }
    static List mlHostname(String defaultValue='') {
        return ['mlHostname', defaultValue, 'The ML hostname (for AAS).']
    }

    static List backupServer(String defaultValue='') {
        return ['backupServer', defaultValue, 'The Backup Server IP (for AAS).']
    }

    static List pathToWorkdir(String defaultValue='') {
        return ['pathToWorkdir', defaultValue, 'The path to the working directory (for AAS).']
    }

    static List awsEcrUrl(String defaultValue='') {
        return ['awsEcrUrl', defaultValue, 'The AWS ECR URL (for AAS).']
    }

    static List awsRegion(String defaultValue='') {
        return ['awsRegion', defaultValue, 'The AWS Region (for AAS).']
    }

    static List tags(String defaultValue='') {
        return ['tags', defaultValue, 'The Retrieved tag value from site values.']
    }

    static List osHostname(String defaultValue='') {
        return ['osHostname', defaultValue, 'OS hostname (for AAS).']
    }

    static List taHostname(String defaultValue='') {
        return ['taHostname', defaultValue, 'The TA hostname (for AAS).']
    }

    static List thHostname(String defaultValue='') {
        return ['thHostname', defaultValue, 'The TH hostname (for AAS).']
    }

    static List broPvcSize(String defaultValue='') {
        return ['broPvcSize', defaultValue, 'The size of the pvc for erci-ctrl-bro (for AAS).']
    }

    static List dataSearchEnginePvcSize(String defaultValue='') {
        return ['dataSearchEnginePvcSize', defaultValue, 'The size of the pvc for data-search-engine (for AAS).']
    }

    static List sysGasSoPfUdsCpsCtsDmiRtaFaA1CredentialId(String defaultValue='') {
        return ['sysGasSoPfUdsCpsCtsDmiRtaFaA1CredentialId', defaultValue, 'Jenkins Credential id for sys, gas, so, pf, uds, cps, cts, dmi, fa, rta, a1 user (for AAS)']
    }

    static List kubeconfigFileCredentialId(String defaultValue='') {
        return ['kubeconfigFileCredentialId', defaultValue, 'Jenkins Credential id for kubeconfig file (for AAS).']
    }

    static List awsConfigFileCredentialId(String defaultValue='') {
        return ['awsConfigFileCredentialId', defaultValue, 'Jenkins Credential id for aws config file (for AAS).']
    }

    static List awsCredsFileCredentialId(String defaultValue='') {
        return ['awsCredsFileCredentialId', defaultValue, 'Jenkins Credential id for aws creds file (for AAS).']
    }

    static List aaSCloudProviderType(String defaultValue='') {
        return ['aaSCloudProviderType ', defaultValue, 'The type of cloud provider (for AAS).']
    }

    static List pathToFromStateSiteValuesOverrideFile(String defaultValue='') {
        return ['pathToFromStateSiteValuesOverrideFile', defaultValue, 'Path within the Repo to the location of the site values override file associated to the from state value.  The content of this file will be added or will override the content in the FULL_PATH_TO_SITE_VALUES_FILE']
    }

    static List pathToToStateSiteValuesOverrideFile(String defaultValue='') {
        return ['pathToToStateSiteValuesOverrideFile', defaultValue, 'Path within the Repo to the location of the site values override file associated to the to state value.  The content of this file will be added or will override the content in the FULL_PATH_TO_SITE_VALUES_FILE']
    }

    static List pathToFromStateSiteValuesFile(String defaultValue='') {
        return ['pathToFromStateSiteValuesFile', defaultValue, 'Path within the Repo to the location of the site values file associated to the from state value. The content of this file will be added or will override the content in the FULL_PATH_TO_SITE_VALUES_FILE']
    }

    static List pathToToStateSiteValuesFile(String defaultValue='') {
        return ['pathToToStateSiteValuesFile', defaultValue, 'Path within the Repo to the location of the site values file associated to the to state value. The content of this file will be added or will override the content in the FULL_PATH_TO_SITE_VALUES_FILE']
    }

    static List enmHostname(String defaultValue='') {
        return ['enmHostname', defaultValue, 'The ENM hostname for this test environment.']
    }

    static List ecmHostname(String defaultValue='') {
        return ['ecmHostname', defaultValue, 'The ECM hostname for this test environment.']
    }

    static List skipTests(String defaultValue='') {
        return ['skipTests', defaultValue, 'Skips given test scenarios e.g. CANARY_UPGRADE_01, CANARY_UPGRADE_03']
    }

    static List fromSkipTests(String defaultValue='') {
        return ['fromSkipTests', defaultValue, 'Skips given test scenarios for the from state e.g. CANARY_UPGRADE_01, CANARY_UPGRADE_03']
    }

    static List runTests(String defaultValue='') {
        return ['runTests', defaultValue, 'Run given tests scenarios and nothing else e.g. CANARY_UPGRADE_01, CANARY_UPGRADE_03']
    }

    static List configFiles(String defaultValue='') {
        return ['configFiles', defaultValue, 'By default these tests will run e.g., ["main_multiple_iterations.json", "main_single_iteration.json", "main_CU2.json"] Override it if needed']
    }

    static List fromConfigFiles(String defaultValue='') {
        return ['fromConfigFiles', defaultValue, 'By default these tests will run for the from state e.g., ["main_multiple_iterations.json", "main_single_iteration.json", "main_CU2.json"] Override it if needed']
    }

    static List poolName(String defaultValue='') {
        return ['POOL_NAME', defaultValue, 'Name of the Pool in RPT.']
    }

    static List status(String defaultValue='') {
        return ['status', defaultValue, 'The status of the environment.']
    }

    static List currentEnvName(String defaultValue='') {
        return ['CURRENT_ENV_NAME', defaultValue, 'Name of the current environment in the Product Staging pipeline (at the time of failure).']
    }

    static List standbyPoolName(String defaultValue='') {
        return ['STANDBY_POOL_NAME', defaultValue, 'Name of the pool containing \'Standby\' test environments, from which \'Available\' environment will be selected.']
    }

    static List psoFlowPoolName(String defaultValue='') {
        return ['PSO_FLOW_POOL_NAME', defaultValue, 'Name of the pool containing current environment being used in the Product Staging pipeline.']
    }

    static List poolToSwapEnvironmentFrom(String defaultValue='') {
        return ['POOL_TO_SWAP_ENVIRONMENT_FROM', defaultValue, 'Name of the pool containing the test environment.']
    }

    static List poolToSwapEnvironmentTo(String defaultValue='') {
        return ['POOL_TO_SWAP_ENVIRONMENT_TO', defaultValue, 'Name of the pool which the environment will be swapped to.']
    }

    static List poolContainingStandbyEnv(String defaultValue='') {
        return ['POOL_CONTAINING_STANDBY_ENV', defaultValue, 'Name of the pool containing the \'Standby\' test environment from which the freshest \'Available\' environment will be selected from.']
    }

    static List poolToSwapFreshestEnvTo(String defaultValue='') {
        return ['POOL_TO_SWAP_FRESHEST_ENV_TO', defaultValue, 'Name of the pool to swap the freshest \'Standby\' environment to.']
    }

    static List fhSnmpAlarmIp(String defaultValue='') {
        return ['fhSnmpAlarmIp', defaultValue, 'External IP address to be passed in to the site-values file.']
    }
    static List laHostname(String defaultValue='') {
        return ['laHostname', defaultValue, 'The Log Aggregator Hostname.']
    }

    static List bdrHostname(String defaultValue='') {
        return ['bdrHostname', defaultValue, 'The Bulk Data Repository Hostname.']
    }

    static List envConfigFile(String defaultValue='') {
        return ['envConfigFile', defaultValue, 'Can be used to specify the environment configuration file which has specific details only for the environment under test']
    }

    static List backupServerCredential(String defaultValue='') {
        return ['backupServerCredential', defaultValue, 'Jenkins Credentials for SFTP Backup Server (for AAS)']
    }

    static List backupServerRemotePath(String defaultValue='') {
        return ['backupServerRemotePath', defaultValue, 'Remote path on SFTP Backup server for storing backups (for AAS)']
    }

    static List eicHostname(String defaultValue='') {
        return ['eicHostname', defaultValue, 'The EIC Hostname.']
    }

    static List restsimHost(String defaultValue='') {
        return ['restsimHost', defaultValue, 'The RESTSIM Hostname.']
    }

    static List spinnakerPipelineId(String defaultValue='123456') {
        return ['SPINNAKER_PIPELINE_ID', defaultValue, 'ID for Spinnaker pipeline. Used as a placeholder to migitage Jenkins 404 build errors.']
    }

    static List retryTimeout(String defaultValue='7200') {
        return ['RETRY_TIMEOUT', defaultValue, 'The timeout in seconds between retry requests if the target host is not found']
    }
}
