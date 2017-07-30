import apache_beam as beam
import re

from apache_beam.utils.pipeline_options import PipelineOptions


pipeline_args = [
    #1. DataflowRunner runs the pipeline on Google Cloud Dataflow
    '--runner=DataflowRunner',
    #2. Google Cloud Project ID
    '--project=your-project-ID',
    #3. Google Cloud Storage path is required for staging local files
    '--staging_location=gs://your-bucket-name/staging',
    #4. Google Cloud Storage path is required for temporary files
    '--temp_location=gs://your-bucket-name/temp',
    #5. (Optional) Job name to be displayed in the logs
    '--job_name=word-count-job'
]
pipeline_options = PipelineOptions(pipeline_args)
pipeline = beam.Pipeline(options = pipeline_options)

# Data Transforms
(pipeline
 | 'read file' >> beam.io.ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
 | 'get words' >> beam.FlatMap(lambda x: re.findall(r'\w+', x))
 | 'count words' >> beam.combiners.Count.PerElement()
 | 'save' >> beam.io.WriteToText('gs://your-bucket-name/wordcount-output.txt'))
pipeline.run()
