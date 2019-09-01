import json
import os

import boto3
from botocore.exceptions import ClientError


def get_secret_string(secret_name, region_name='us-east-1'):
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
        print(secret_name, "could not be loadded:", e)
        return None
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']

    return None


def get_secret_json(secret_name, region_name='us-east-1'):
    try:
        return json.loads(get_secret_string(secret_name, region_name))
    except json.decoder.JSONDecodeError:
        return {}


def secrets_config_key(secret_name, region_name='us-east-1'):
    secrets = get_secret_json(secret_name, region_name)

    def inner(key, default=None):
        return os.getenv(key, secrets.get(key, default))

    return inner


def secrets_config(env, secret_name, region_name='us-east-1'):
    try:
        secret = os.getenv(env, None)
        if secret:
            return json.loads(secret)
        else:
            return json.loads(get_secret_string(secret_name, region_name))
    except (json.decoder.JSONDecodeError, TypeError) as e:
        print(e)
        raise Exception('ENV or Secret is invalid json or None!')


def get_database_config(default,
                        secret_name=None,
                        region_name='us-east-1',
                        engine="django.db.backends.postgresql"):
    if secret_name:
        db_secets = get_secret_json(secret_name, region_name=region_name)

        return {
            'ENGINE': engine,
            'NAME': db_secets['dbname'],
            'USER': db_secets['username'],
            'PASSWORD': db_secets['password'],
            'HOST': db_secets['host'],
            'PORT': db_secets['port']
        }

    return default
