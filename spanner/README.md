# README

## Project Summary

In this tutorial, we'll learn how to use [Google Cloud Spanner](https://cloud.google.com/spanner/) by following the [examples](https://cloud.google.com/spanner/docs/schema-and-data-model#schema_examples) provided in the documentation.

## Requirements

* If you haven't already, you may sign-up for the [free GCP trial credit](https://cloud.google.com/free/docs/frequently-asked-questions).   
[Before you begin](https://cloud.google.com/spanner/docs/quickstart-console#before-you-begin), set-up your project and enable billing.
* (*optional, but recommended*) Set-up a Python virtual environment:
  * Install pyenv-virtualenv ([Instructions for macOS](http://akbaribrahim.com/)).
  * Create and activate an environment:
  ```shell
  $ pyenv virtualenv gcp_env
  $ pyenv activate gcp_env
  ```
* Install the Spanner Python API:
```shell
$ pip install -r requirements.txt
```

## Run Code

1. Create a Spanner instance and create a Singers table in the UI as shown [here](https://cloud.google.com/spanner/docs/quickstart-console#create_an_instance).
(You may also run the `spanner-setup.sh` script to take care of this step.
  ```shell
  $ chmod +x spanner-setup.sh
  $ ./spanner-setup.sh
  ```
  )  
2. Write to the Singers table.
```shell
$ python write-to-table.py
```
These values are now visible in the UI.

## Clean-up

* [Delete both the database and the instance](https://cloud.google.com/spanner/docs/quickstart-console#delete_the_database) to avoid incurring charges to your account.
* If you created a Python virtual environment, deactivate it:
```shell
$ pyenv deactivate
```

## Reference

[GCP Spanner repo](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/spanner/cloud-client/snippets.py)
