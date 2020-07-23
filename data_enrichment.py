from __future__ import absolute_import
import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions
from scikit_learn_predictor import predict as sk_predict

logging.getLogger().setLevel(logging.INFO)

"""
record: the input raw data from input table, column value could be got by record['column_name']
return: input value + predicting result in a dictionary
"""


def model_predict(record):
    result = record
    logging.info('record: ' + str(result))
    # just use the feature1,2,3 columns as the input value, and passed as a two dimensional array
    input_features = [[record['feature1'], record['feature3'], record['feature3']]]
    # convert the return predicting result to int type
    predict = int(sk_predict(input_features))
    # add the predict value to the return dictionary
    result['predict'] = predict
    logging.info('predict: ' + str(result))
    return [result]


def run(argv=None):
    """Constructs and runs the pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        help='BigQuery table to read from.',
        default='dataflow-example-282410:samples.input_tbl')
    parser.add_argument(
        '--output', help='BigQuery table to write to.',
        default='dataflow-example-282410:samples.output_tbl')
    known_args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'dataflow-example-282410'
    with beam.Pipeline(argv=pipeline_args, options=google_cloud_options) as p:
        p | 'Read from input_tbl' >> beam.io.Read(
            beam.io.BigQuerySource(known_args.input)) \
        | 'model predict' >> beam.ParDo(model_predict) \
        | 'SaveToBQ' >> beam.io.WriteToBigQuery(
            known_args.output,
            schema='id:INTEGER,text:STRING,feature1:INTEGER,feature2:INTEGER'
                   ',feature3:INTEGER,create_date:DATE,predict:INTEGER',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)


if __name__ == '__main__':
    run()
