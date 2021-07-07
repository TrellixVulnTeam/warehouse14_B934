from uuid import uuid4

import boto3
import pytest
from moto import mock_dynamodb2, mock_s3


@pytest.fixture
def bucket():
    """Pytest fixture that creates the bucket in
    the fake moto AWS account
    """
    with mock_s3():
        s3 = boto3.resource("s3", region_name="us-east-1")
        bucket = s3.Bucket(str(uuid4()))
        bucket.create()
        yield bucket


@pytest.fixture
def table():
    """Pytest fixture that creates the table in
    the fake moto AWS account
    """
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        yield dynamodb.create_table(
            TableName=str(uuid4()),
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "sk_gsi",
                    "KeySchema": [
                        {"AttributeName": "sk", "KeyType": "HASH"},
                        {"AttributeName": "pk", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                }
            ],
        )
