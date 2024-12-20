import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pipeline-config-telecom')

table.put_item(
    Item={
        'id_pipeline': 'pipeline_001',
        'status': 'Success',
        'timestamp': datetime.utcnow().isoformat()
    }
)

