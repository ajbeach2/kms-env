import json
import os

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name='us-east-1'):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        return {}


def secrets_config(key, secret_name, default=None, region_name='us-east-1'):
    secrets = get_secret(secret_name, region_name)

    def inner(key, secret_name):
        return os.getenv(key, secrets.get(key, default))

    return inner


def get_database_config(default,
                        secret_name=None,
                        region_name='us-east-1',
                        engine="django.db.backends.postgresql"):
    if secret_name:
        db_secets = get_secret(secret_name, region_name=region_name)

        return {
            'ENGINE': engine,
            'NAME': db_secets['dbname'],
            'USER': db_secets['username'],
            'PASSWORD': db_secets['password'],
            'HOST': db_secets['host'],
            'PORT': db_secets['port']
        }

    return default
