package common_classes

/**
 * Class containing Common groovy parameters
 */
class CommonParameters {

    static List slave(String defaultValue='GridEngine') {
        return ['SLAVE', defaultValue, 'Slave']
    }

    static List customerSlave(String defaultValue='RPT_GridEngine') {
        return ['SLAVE', defaultValue, 'Slave']
    }

    static String repo() {
        return 'OSS/com.ericsson.oss.ci/pooling-tooling-client'
    }
    static String repoUrl() {
        return '\${GERRIT_MIRROR}/'+repo()
    }

}
