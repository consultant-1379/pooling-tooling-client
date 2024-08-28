#!/bin/bash

function bump_version() {
    WORKSPACE=$1
    old_version=$(cat "${WORKSPACE}"/VERSION)
    version_as_list=( ${old_version//./ } )
    path_to_artifact_properties=${WORKSPACE}'/artifact.properties'
    patch_version=$((version_as_list[2] + 1 ))
    if [[ "${patch_version:${#patch_version}-1}" == "0" ]]; then
        patch_version=${patch_version::1}
    fi
    new_version=${version_as_list[0]}'.'${version_as_list[1]}'.'$patch_version
    echo "$new_version" > "$path_to_artifact_properties"
}


bump_version "$1"
