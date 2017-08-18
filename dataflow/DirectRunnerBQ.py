import re
import apache_beam as beam

from google.cloud import bigquery


projectID = 'your-project-ID'  # project name
datasetID = 'wordcount_dataset'# dataset name
tableID = 'wordcount_table'    # table name

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

# Run Dataflow pipeline
pipeline = beam.Pipeline('DirectRunner')
read = pipeline | 'read file' >> beam.io.ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
get_words = read | 'get words' >> beam.FlatMap(lambda x: re.findall(r'\w+', x))
count_words = get_words | 'count words' >> beam.combiners.Count.PerElement()
word = count_words.apply(beam.Keys('get keys'))
count = count_words.apply(beam.Values('get values'))
result = count_words | 'to dict' >> beam.Map(lambda (word, count): {'word': word, 'count': count})
save = result | 'save' >> beam.io.Write(sink)
pipeline.run()

# Query the table head sorted by count
query = """
        SELECT word, count
        FROM `wordcount_dataset.wordcount_table`
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
