import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Cargar datos del catálogo
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="telecom_database",  # Cambié 'default' por 'telecom_database'
    table_name="telecom_datalake",  # Cambié 'sales_datalake' por 'telecom_datalake'
)


# Limpiar y transformar
# Limpiar y transformar
transformed = datasource.toDF() \
    .dropDuplicates() \
    .withColumn("total_ventas", col("monto") * col("cantidad"))  # Usé 'monto' en lugar de 'precio'


# Escribir los datos transformados a Redshift
transformed.write \
    .format("com.databricks.spark.redshift") \
    .option("url", "jdbc:redshift://telecom-cluster.442426888225.us-east-1.redshift-serverless.amazonaws.com:5439/dev")  # URL de tu clúster de Redshift
    .option("dbtable", "telecom_transformed")  # Cambié 'sales_transformed' por 'telecom_transformed'
    .option("tempdir", "s3://telecom-datalake/temp/")  # Asegúrate de que este directorio en S3 esté configurado correctamente
    .save()

