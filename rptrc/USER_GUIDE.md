# RPT REST Client (RPT-RC)

[TOC]

## Introduction

The RPT REST Client is the companion to the Resource Pooling Tool (RPT).

RPT-RC is a tool meant to allow a user to interact with RPT manually or automatically via CLI.

RPT-RC runs REST calls against RPT in order to perform CRUD operations automatically.

RPT works with a concept of entities and the RPT-RC also follows this design pattern.

## Prerequisites

RPT-RC is meant to be ran inside a Docker container, however it can also be ran inside a python virtual environment.
* For running with docker, you need Docker installed on the system.
* For running without docker, you need to have Python Poetry installed.

## Running RPT-RC with Docker

To run RPT-RC with Docker, you can simply use "docker run" and point to the latest version of RPT-RC in the Ericsson Docker Images Repository:
* armdocker.rnd.ericsson.se/proj_openstack_tooling/pooling_tooling_client

Example Usage:

```shell
docker run --rm --name rpt-rc armdocker.rnd.ericsson.se/proj_openstack_tooling/pooling_tooling_client:latest --help
```

## Running RPT-RC without Docker

> Make sure to run commands at the root level of the RPT-RC repo.
> If you don't have the repo code yet, please go to [RPT-RC](https://gerrit-gamma.gic.ericsson.se/#/admin/projects/OSS/com.ericsson.oss.ci/pooling-tooling-client)

To run RPT-RC without Docker, make sure to have Python Poetry installed by running the following command:
```shell
pip install poetry
```

Then you must enable a Poetry virtual environment:

```shell
poetry shell
```

Install all the dependencies inside this virtual environment:

 ```shell
poetry install
```

Now run the tool. Example Usage:

```shell
python -m rptrc --help
```

## Contact

RPT-RC is developed by Team Thunderbee.

For any queries, bugs or improvement suggestions please contact:
* Thunderbee <PDLENMCOUN@pdl.internal.ericsson.com>
