
# Paso a Paso del Proyecto Telecom Pipeline

Este documento describe paso a paso cómo configurar y ejecutar el pipeline de datos en el proyecto de telecomunicaciones utilizando **AWS Glue**, **S3**, **Redshift**, **Athena**, y **DynamoDB**.

## 1. Preparativos Iniciales

### 1.1 Clonar el repositorio

Clona el repositorio del proyecto desde GitHub:

```bash
git clone https://github.com/LogxAcademy/telecom.git
```

### 1.2 Configuración de AWS CLI

Asegúrate de tener configurado **AWS CLI** con las credenciales de tu cuenta de AWS:

```bash
aws configure
```

Proporciona tu **Access Key**, **Secret Key**, la **región** y el **formato de salida** (`json` es una opción recomendada).

### 1.3 Verificación de permisos

Verifica que tengas los permisos necesarios para acceder a **AWS Glue**, **Amazon S3**, **Redshift**, **Athena**, y **DynamoDB** en tu cuenta de AWS. Asegúrate de que el rol de IAM que utilizarás tenga los permisos correctos.

---

## 2. Subir los Archivos de Datos a S3

### 2.1 Preparar los datos

Los archivos de datos de ejemplo se encuentran en la carpeta `example_data.csv`. Puedes agregar más archivos en formato CSV o JSON en la misma carpeta para ser utilizados por el pipeline.

### 2.2 Crear un Bucket en S3

1. Inicia sesión en la consola de **Amazon S3**.
2. Crea un **nuevo bucket** en S3 (por ejemplo, `telecom-datalake`).
3. Sube los archivos de datos que deseas procesar dentro de este bucket.

---

## 3. Configurar AWS Glue

### 3.1 Crear un Crawler en AWS Glue

1. Dirígete a la consola de **AWS Glue**.
2. En **Crawlers**, haz clic en **Add crawler**.
3. Proporciona un nombre para el Crawler, por ejemplo, `telecom-data-crawler`.
4. En **Data store**, selecciona **S3** y elige el bucket que creaste previamente (`telecom-datalake`).
5. Configura el **IAM role** para que tenga permisos para acceder a **S3** y **Glue**.
6. Ejecuta el Crawler para que cataloge los datos en el Glue Data Catalog.

### 3.2 Verificar la Catalogación en Glue

1. En **AWS Glue**, ve a **Data Catalog** y selecciona **Tables**.
2. Verifica que la tabla de los datos catalogados (por ejemplo, `telecom_datalake`) esté presente en el catálogo.

---

## 4. Configurar y Ejecutar el Job de AWS Glue

### 4.1 Crear un Job de Glue

1. Ve a **Jobs** en la consola de **AWS Glue** y haz clic en **Add job**.
2. Asocia un nombre como `telecom-etl-job` para el trabajo.
3. Selecciona el rol de **IAM** con permisos de acceso a **S3**, **Redshift**, y **Glue**.
4. Usa el siguiente script ETL para realizar las transformaciones de los datos.

#### Script ETL

```python
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
    database="telecom_database",
    table_name="telecom_datalake",
)

# Limpiar y transformar
transformed = datasource.toDF()     .dropDuplicates()     .withColumn("total_ventas", col("monto") * col("cantidad"))

# Escribir los datos transformados a Redshift
transformed.write     .format("com.databricks.spark.redshift")     .option("url", "jdbc:redshift://telecom-cluster.redshift.amazonaws.com:5439/telecomdb")     .option("dbtable", "telecom_transformed")     .option("tempdir", "s3://telecom-datalake/temp/")     .save()
```

5. Ejecuta el Job para que procese los datos.

---

## 5. Configurar Amazon Redshift

### 5.1 Crear un Clúster de Redshift Serverless

1. En la consola de **Amazon Redshift**, crea un **clúster Serverless**.
2. Define la base de datos como `telecomdb`.
3. Asegúrate de que el clúster tenga acceso al bucket de S3 donde los datos procesados se almacenarán.

### 5.2 Crear las Tablas en Redshift

Una vez que los datos sean procesados y transformados, crea una tabla en Redshift para almacenar los datos:

```sql
CREATE TABLE telecom_transformed (
    id_cliente INT,
    nombre_cliente VARCHAR(255),
    plan VARCHAR(255),
    monto DECIMAL(10, 2),
    cantidad INT,
    total_ventas DECIMAL(10, 2)
);
```

---

## 6. Configurar Amazon Athena

### 6.1 Configurar el Catálogo de Athena

1. En **Amazon Athena**, configura el catálogo de **AWS Glue** como fuente de datos.
2. Selecciona la base de datos **telecom_database**.
3. Asegúrate de que la tabla `telecom_datalake` esté disponible en Athena.

### 6.2 Realizar Consultas en Athena

Puedes realizar consultas ad-hoc sobre los datos procesados en **S3** con Athena. Por ejemplo:

```sql
SELECT * 
FROM "AwsDataCatalog"."telecom_database"."telecom_datalake"
LIMIT 10;
```

---

## 7. Configurar DynamoDB

### 7.1 Crear una Tabla en DynamoDB

1. En **Amazon DynamoDB**, crea una tabla llamada `pipeline-config` para registrar configuraciones o logs del pipeline.
2. La tabla debe tener una clave primaria como `id_pipeline`.

### 7.2 Registrar Logs de Ejecución

Para registrar logs o configuraciones del pipeline en DynamoDB, usa el siguiente script:

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pipeline-config')

table.put_item(
    Item={
        'id_pipeline': 'pipeline_001',
        'status': 'Success',
        'timestamp': datetime.utcnow().isoformat()
    }
)
```

---

## 8. Finalización

Una vez completados estos pasos, el pipeline de datos estará completamente configurado y funcionando. Los datos se procesarán y almacenarán en **Redshift**, y podrás realizar consultas ad-hoc sobre los datos usando **Athena**. También se registrarán logs y configuraciones en **DynamoDB**.

---

Este archivo proporciona una guía completa para configurar y ejecutar cada parte del pipeline de datos en el proyecto de telecomunicaciones. Asegúrate de seguir los pasos cuidadosamente para configurar todos los servicios necesarios de AWS.
