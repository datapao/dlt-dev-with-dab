This repository contains a demo of the development lifecycle with  [Databricks Delta Live Tables (DLT)](https://docs.databricks.com/workflows/delta-live-tables/index.html) to perform unit & integration testing of DLT pipelines using [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html).  The repository also includes a sample of CI/CD pipeline using [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) (ADO) to automate the testing and deployment of DLT pipelines.

* [The development workflow](#the-development-workflow)
* [Setup instructions](#setup-instructions)
   * [Create necessary Databricks Repos checkouts](#create-necessary-databricks-repos-checkouts)
   * [Create DLT pipelines](#create-dlt-pipelines)
   * [Create Databricks cluster](#create-databricks-cluster)
   * [Create ADO build pipeline](#create-ado-build-pipeline)
   * [Create ADO release pipeline](#create-ado-release-pipeline)
   
# The development workflow

The development workflow is organized as on following image:

![DLT development workflow](images/cicd-process.png)

More detailed description is available in the blog post [Applying software development & DevOps best practices to Delta Live Table pipelines](https://www.databricks.com/blog/applying-software-development-devops-best-practices-delta-live-table-pipelines). 


# Setup instructions

:construction: Work in progress...

:warning: Setup instructions describe process of performing CI/CD using Azure DevOps (ADO), but similar thing could be implemented with any CI/CD technology.

There are two ways of setting up everything:

1. using Terraform - it's the easiest way of getting everything configured in a short time.  Just follow instructions in [terraform/azuredevops/](terraform/azuredevops/) folder.  :warning: This doesn't include creation of release pipeline as there is no REST API and Terraform resource for it.
2. manually - follow instructions below to create all necessary objects.


## Create necessary Databricks Repos checkouts

In this example we're using three [checkouts of our sample repository](https://docs.databricks.com/repos/git-operations-with-repos.html#add-a-repo-connected-to-a-remote-repo):

1. Development: is used for actual development of the new code, running tests before committing the code, etc.
1. Staging: will be used to run tests on commits to branches and/or pull requests.  This checkout will be updated to the actual branch to which commit happened.  We're using one checkout just for simplicity, but in real-life we'll need to create such checkouts automatically to allow multiple tests to run in parallel. 
1. Production: is used to keep the production code - this checkout always will be on the `releases` branch, and will be updated only when commit happens to that branch and all tests are passed.

Here is an example of repos created with Terraform:

![Databricks repos](images/repos.png)

## Create DLT pipelines

We need to create a few DLT pipelines for our work:

1. for main code that is used for development - use only `pipelines/DLT-Pipeline.py` notebook from the development repository.
1. (optional) for integration test that could be run as part of development - from the development repository use main code notebook (`pipelines/DLT-Pipeline.py`) together with integration test notebook (`tests/integration/DLT-Pipeline-Test.py`).
1. for integration test running as part of CI/CD pipeline - similar to the previous item, but use the staging repository.
1. for production pipeline - use only `pipelines/DLT-Pipeline.py` notebook from the production repository.

Here is an example of pipelines created with Terraform:

![Databricks repos](images/dlt-pipelines.png)

## Create Databricks cluster

If you decide to run notebooks with tests located in `tests/unit-notebooks` directory, you will need to [create a Databricks cluster](https://docs.databricks.com/clusters/configure.html) that will be used by the Nutter library.  To speedup tests, attach the `nutter` & `chispa` libraries to the created cluster.

If you don't want to run these tests, comment out in the `azure-pipelines.yml` the block with `displayName` "Execute Nutter tests".

## Create ADO build pipeline

:construction: Work in progress...

The ADO build pipeline consists of the two stages:

- `onPush` is executed on push to any Git branch except `releases` branch and version tags.  This stage only runs & reports unit tests results (both local & notebooks).
- `onRelease` is executed only on commits to the `releases` branch, and in addition to the unit tests it will execute a DLT pipeline with integration test (see image).

![Stages of ADO build pipeline](images/cicd-stages.png)



## Create ADO release pipeline

:construction: Work in progress...

