sectionedView('Resource Pooling Tool Client CICD') {
    description('''<div style="padding:1em;border-radius:1em;text-align:center;background:#fbf6e1;box-shadow:0 0.1em 0.3em #525000">
        <b>Resource Pooling Tool Rest Client</b><br>
       CICD Pipelines, Source Control Jobs as well as Customer Production and Staging jobs.<br><br>
        Team: <b>Thunderbee &#x26A1</b><br>
    </div>''')
    sections {
        listView {
            name('RPT-RC Production Jobs')
            jobs {
                name('RPT-RC_Check_if_Environment_on_Latest_EIC_Version')
                name('RPT-RC_Quarantine-Environment')
                name('RPT-RC_Reserve-Environment')
                name('RPT-RC_Retrieve-Environment-Details')
                name('RPT-RC_Unreserve-Environment')
                name('RPT-RC_Update-Environment-Details')
                name('RPT-RC_Update-EIC-and-DM-From-State-Version')
                name('RPT-RC_Update-From-State-By-Pool')
                name('RPT-RC_Update-PipelineStage')
                name('RPT-RC_Update-Test-Environment-Status')
                name('RPT-RC_Swap_Refreshed_Test_Environment_into_Product_Staging_Flow')
                name('RPT-RC_Swap_Test_Environment_Pool')
                name('RPT-RC_Update_Freshest_Standby_Environment_To_Available_And_Swap_Pool')
            }
            columns setViewColumns()
        }
        listView {
            name('RPT-RC Staging Jobs')
            jobs {
                name('resource-pooling-tool-client_Staging_Quarantine')
                name('resource-pooling-tool-client_Staging_Reserve')
                name('resource-pooling-tool-client_Staging_Unreserve')
                name('resource-pooling-tool-client_Staging_Update_PipelineStage')
            }
            columns setViewColumns()
        }
        listView {
            name('RPT-RC CICD Pipelines')
            jobs {
                name('resource-pooling-tool-client_Pre_Code_Review')
                name('resource-pooling-tool-client_Build_And_Publish')
            }
            columns setViewColumns()
        }
        listView {
            name('RPT-RC CICD Pipeline Source Control')
            jobs {
                name("resource-pooling-tool-client_Pipeline_Generator")
                name("resource-pooling-tool-client_Pipeline_Updater")
            }
            columns setViewColumns()
        }
    }
}

static Object setViewColumns() {
    return {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}
