# Telecom Pipeline Project

Este proyecto tiene como objetivo procesar y transformar datos relacionados con un sistema de telecomunicaciones, integrando diversas tecnologías como AWS Glue, S3, Redshift, DynamoDB y Athena. 

## Estructura del Proyecto

El proyecto contiene las siguientes carpetas y archivos importantes:

- **DynamoDB/**: Contiene scripts relacionados con la integración y la gestión de datos en DynamoDB.
- **data/**: Carpeta que contiene los archivos de datos, como `example_data.csv`, utilizados en el pipeline.
- **scripts/**: Contiene scripts de procesamiento de datos, como los que se usan para transformar los datos en AWS Glue.
- **README.md.txt**: Este archivo de documentación que describe el proyecto.

## Tecnologías Utilizadas

- **AWS Glue**: Para la orquestación de los trabajos ETL.
- **Amazon S3**: Para almacenar los datos de entrada y salida.
- **Amazon Redshift**: Para almacenar los datos procesados y realizar consultas.
- **Amazon Athena**: Para realizar consultas ad-hoc sobre los datos almacenados en S3.
- **DynamoDB**: Para gestionar configuraciones o registros clave del pipeline.

## Instalación

Para ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. Clona el repositorio:

    ```bash
    git clone https://github.com/LogxAcademy/telecom.git
    ```

2. Asegúrate de tener **AWS CLI** configurado con las credenciales de AWS:

    ```bash
    aws configure
    ```

3. Asegúrate de que tienes acceso a **AWS Glue**, **Amazon S3**, **Redshift**, y **Athena** en tu cuenta de AWS para ejecutar los scripts de este proyecto.

4. Si deseas ejecutar el pipeline localmente, asegúrate de tener instalado **Python 3.x** y **boto3**.

## Uso

1. Sube los archivos de datos a tu bucket de **S3**. Los archivos deben estar en formato CSV o JSON.
2. Ejecuta el **crawler** en AWS Glue para catalogar los datos en **S3**.
3. Configura y ejecuta los trabajos de **AWS Glue** para transformar los datos.
4. Utiliza **Amazon Athena** para realizar consultas ad-hoc sobre los datos en **S3**.
5. Los resultados procesados se almacenarán en **Amazon Redshift**.

## Contribuciones

1. Haz un fork de este repositorio.
2. Crea tu nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Empuja a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un pull request.

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
