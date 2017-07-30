import re
import apache_beam as beam


# Run Dataflow pipeline
pipeline = beam.Pipeline('DirectRunner')

(pipeline
   | 'read file' >> beam.io.ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
   | 'get words' >> beam.FlatMap(lambda x: re.findall(r'\w+', x)).with_output_types(unicode)
   | 'count words' >> beam.combiners.Count.PerElement()
   | 'save' >> beam.io.WriteToText('./wordcount_output'))
pipeline.run()
