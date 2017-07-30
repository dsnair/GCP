# README

## Project Summary

1. Implement the [MinimalWordCount](https://beam.apache.org/get-started/wordcount-example/) example using the Google Cloud Dataflow service.
2. Modify example to write to BigQuery or Datastore - create your own schema.
3. Implement WindowedWordCount example to understand how windowing works.

## Requirements

1. Install pip (version >= 7.0.0).
2. (_Optional, but recommended_) Install pyenv-virtualenv ([Instructions for macOS](http://akbaribrahim.com/)).
3. (_Optional, but recommended_) Create and activate a Python virtual environment in pyenv-virtualenv:

  ```shell
  pyenv virtualenv word_count_env
  pyenv activate word_count_env
  ```

4. Install the Apache Beam Python SDK:

  ```shell
  pip install apache-beam[gcp]
  ```

5. [Set-up](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python) your project to use Dataflow as instructed under 'Before you begin' section.
6. Install BigQuery:

  ```shell
  pip install google-cloud-bigquery==0.24.0
  ```

## Run

### 1\. (Basic) MinimalWordCount Example

- Run the script using cloud services:

  ```shell
  python DataflowRunner.py
  ```

  _Personal Experience/Possible Gotchas:_

  - You don't necessarily need to create the `staging` and `temp` folders under `your-bucket-name`. The script automatically creates them. You must, however, create `your-bucket-name` as you go through Step 5 above.
  - You may see the following warning<br>
    `No handlers could be found for logger "oauth2client.contrib.multistore_file"`.<br>
    This is a harmless warning and you may ignore it.
  - Even though you have apache-beam installed already, it tries to install it again (weird!). Specifically, you may see a `Successfully downloaded apache-beam` message. You may ignore this as well.
  - It may take a few minutes to generate the output files in `your-bucket-name`. You may [monitor](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf) this process as instructed under 'Accessing the Dataflow Monitoring Interface' section.

  **OUTPUT:** In your Google Cloud project, go to `your-bucket-name` folder. You'll see two folders named `staging` and `temp`, and, more interestingly, three text files, which contain all the unique words in the input file and their frequencies.

- Run the script locally:

  ```shell
  python DirectRunner.py
  ```

  **OUTPUT:** A text file whose name starts with `wordcount_output`.
- If you created a Python virtual environment, deactivate it:

  ```shell
  pyenv deactivate
  ```

### 2\. (Modified) Write MinimalWordCount Output to BigQuery

- Run the script using cloud services:

  ```shell
  python DataflowRunnerBQ.py
  ```

  **OUTPUT:** Prints ten table values.
- Run the script locally:

  ```shell
  python DirectRunnerBQ.py
  ```

  **OUTPUT:** Prints ten table values.
- If you created a Python virtual environment, deactivate it:

  ```shell
  pyenv deactivate
  ```

## Code Reference

- Apache-beam [GitHub repo](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount_minimal.py)
- Google Cloud Platform BigQuery [GitHub repo](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/bigquery/cloud-client/simple_app.py)
