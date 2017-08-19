# README

## Project Summary

In this tutorial, we'll learn how to write pandas dataframe to [BigQuery](https://cloud.google.com/bigquery/) and how to query from BigQuery within pandas.

## Requirements

* If you haven't already, you may sign-up for the [free GCP trial credit](https://cloud.google.com/free/docs/frequently-asked-questions).   
[Set up your project](https://cloud.google.com/bigquery/quickstart-web-ui#before-you-begin) on GCP and enable the BigQuery API.
* (*optional, but recommended*) Set-up a Python virtual environment:
  * Install pyenv-virtualenv ([Instructions for macOS](http://akbaribrahim.com/)).
  * Create and activate an environment:
  ```shell
  pyenv virtualenv gcp_env
  pyenv activate gcp_env
  ```
* Install pandas and the pandas wrapper for BigQuery:
```shell
pip install -r requirements.txt
```

## Clean-up

[Delete the BigQuery dataset](https://cloud.google.com/bigquery/quickstart-web-ui#clean-up) to avoid incurring charges to your account.

## Reference

* [Pandas wrapper for BigQuery](https://pandas-gbq.readthedocs.io/en/latest/intro.html)
* [df.to_gbq](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_gbq.html)
* [pd.read_gbq](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_gbq.html)

## Additional tutorial

The `dataflow` and `datalab` directories within this repository have tutorials on how to write dataflow results to BigQuery and how to write BigQuery queries within Datalab.
