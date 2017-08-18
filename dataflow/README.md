# README

## Project Summary

In this tutorial, we'll learn how to use [Google Cloud Dataflow](https://cloud.google.com/dataflow/) to

1. implement the [MinimalWordCount](https://beam.apache.org/get-started/wordcount-example/#minimalwordcount) example, and then
2. modify the example to write the results to BigQuery by creating our own schema

## Requirements

1. Install pip (version >= 7.0.0).
2. (*Optional, but recommended*) Install pyenv-virtualenv ([Instructions for macOS](http://akbaribrahim.com/)).
3. (*Optional, but recommended*) Create and activate a Python virtual environment in pyenv-virtualenv:

  ```shell
  pyenv virtualenv gcp_env
  pyenv activate gcp_env
  ```

4. Install BigQuery and Apache Beam Python SDK:

  ```shell
  pip install -r requirements.txt
  ```
6. [Set-up your project](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python) as instructed under the 'Before you begin' section. If you haven't already, you may sign-up for the [free GCP trial credit](https://cloud.google.com/free/docs/frequently-asked-questions)


## Run Scripts

### 1\. (Basic) MinimalWordCount Example

* First, let's test our code locally on our laptop.
  ```shell
  python DirectRunner.py
  ```
  **Output:** A text file whose name starts with `wordcount_output-*`.

  You may see the following warning<br>
  `No handlers could be found for logger "oauth2client.contrib.multistore_file"`.<br> This is a harmless warning and you may ignore it.

* Now that the code works locally, let's test it on the cloud.  

  Edit `DataflowRunner.py` with your values for `your-project-ID` and `your-bucket-name`. You don't need to create the `your-bucket-name/staging` and `your-bucket-name/temp` sub-directories; the script automatically creates them.
  ```shell
  python DataflowRunner.py
  ```
  It may take a few minutes to generate the output files in `your-bucket-name`. You may [monitor](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf#accessing-the-dataflow-monitoring-interface) this process in your project on the cloud. The job name is `word-count-job`.

  **Output:** [Go to `your-bucket-name`](https://console.cloud.google.com/storage/browser). You'll see two folders named `staging/` and `temp/`, and three text files who names start with `wordcount_output-*`. These text files contain all the unique words in the input file and their frequencies.

### 2\. (Modified) Write MinimalWordCount Output to BigQuery

* Again, let's first test our code locally.

  Edit `DirectRunnerBQ.py` with your values for `your-project-ID`.

  ```shell
  python DirectRunnerBQ.py
  ```
  **Output:** Prints ten table values on the shell.

* Now, let's run the script on the cloud.

  Edit `DataflowRunnerBQ.py` with your values for `your-project-ID` and `your-bucket-name`.

  ```shell
  python DataflowRunnerBQ.py
  ```
  **Output:** Prints ten table values on the shell.

  Again, you may [monitor](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf#accessing-the-dataflow-monitoring-interface) the dataflow process. The job name is `word-count-bq-job`.


## Clean-up

To avoid incurring charges to your account,
* [delete your BigQuery dataset](https://cloud.google.com/bigquery/quickstart-web-ui#clean-up). The dataset is named `wordcount_dataset`.
* [delete your buckets](https://cloud.google.com/storage/docs/quickstart-console#clean-up)

If you created a Python virtual environment, deactivate it:
```shell
pyenv deactivate
```

## Code Reference

* Apache-beam [GitHub repo](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount_minimal.py)
* Google Cloud Platform BigQuery [GitHub repo](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/bigquery/cloud-client/simple_app.py)
