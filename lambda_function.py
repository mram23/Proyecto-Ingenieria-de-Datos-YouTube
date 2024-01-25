
# Se importan las librerías
# En este caso, awswrangler permite leer y escribir datos en S3
import awswrangler as wr
import pandas as pd
import urllib.parse
# os, permite acceder a las variables del entorno
import os

os_input_s3_cleansed_layer = os.environ['s3_cleansed_layer']
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name']
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name']
os_input_write_data_operation = os.environ['write_data_operation']


def lambda_handler(event, context):
    # Para rescatar el bucket deseado
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:

        # A partir de dicho bucket, leemos su data
        df_raw = wr.s3.read_json('s3://{}/{}'.format(bucket, key))

        # Extraemos la parte requerida, que es la de items
        df_step_1 = pd.json_normalize(df_raw['items'])

        # Hacemos la transformacion de json a parquet
	# Y luego lo escribimos a la base de datos de Glue denominada cleaned_statistics_reference_data
        wr_response = wr.s3.to_parquet(
            df=df_step_1,
            path=os_input_s3_cleansed_layer,
            dataset=True,
            database=os_input_glue_catalog_db_name,
            table=os_input_glue_catalog_table_name,
            mode=os_input_write_data_operation
        )

        return wr_response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
