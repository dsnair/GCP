import apache_beam as beam
import re

from apache_beam.utils.pipeline_options import PipelineOptions
from google.cloud import bigquery


projectID = 'bamboo-magnet-166418'  # project name
datasetID = 'wordcount_dataset'     # dataset name
tableID = 'wordcount_table'         # table name

# Instantiate the BigQuery client
client = bigquery.Client(project = projectID)

# Create dataset
dataset = client.dataset(datasetID)
if not dataset.exists():
    dataset.create()

# Create table and set its schema
table = dataset.table(tableID)
table.schema = (bigquery.SchemaField('word', 'STRING'),
                bigquery.SchemaField('count', 'INTEGER'))
if not table.exists():
    table.create()

# Prepare BigQuery Sink
sink = beam.io.BigQuerySink(table = tableID,
                            dataset = datasetID,
                            project = projectID,
                            schema = 'word:STRING, count:INTEGER')

pipeline_args = [
    #1. DataflowRunner runs the pipeline on Google Cloud Dataflow
    '--runner=DataflowRunner',
    #2. Google Cloud Project ID
    '--project=bamboo-magnet-166418',
    #3. Google Cloud Storage path is required for staging local files
    '--staging_location=gs://word-count-bq/staging',
    #4. Google Cloud Storage path is required for temporary files
    '--temp_location=gs://word-count-bq/temp',
    #5. (Optional) Job name to be displayed in the logs
    '--job_name=word-count-bq-job'
]
pipeline_options = PipelineOptions(pipeline_args)
pipeline = beam.Pipeline(options = pipeline_options)

# Run Dataflow pipeline
read = pipeline | 'read file' >> beam.io.ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
get_words = read | 'get words' >> beam.FlatMap(lambda x: re.findall(r'\w+', x)).with_output_types(unicode)
count_words = get_words | 'count words' >> beam.combiners.Count.PerElement()
word = count_words.apply(beam.Keys('get keys'))
count = count_words.apply(beam.Values('get values'))
result = count_words | 'to dict' >> beam.Map(lambda (word, count): {'word': word, 'count': count})
save = result | 'save' >> beam.io.Write(sink)
pipeline.run().wait_until_finish()

# Query the table head sorted by count
query = """
        SELECT word, count
        FROM `bamboo-magnet-166418.wordcount_dataset.wordcount_table`
        ORDER BY count ASC
        LIMIT 10;
        """
results = client.run_sync_query(query)

# Use standard SQL syntax for queries
results.use_legacy_sql = False

results.run()

# Drain query results by requesting one page at a time
page_token = None
while True:
    rows, total_rows, page_token = results.fetch_data(max_results = 10,
                                                      page_token = page_token)
    for row in rows:
        print(row)
    if not page_token:
        break
