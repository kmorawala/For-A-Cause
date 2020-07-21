import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import json
from keys import CarKeys
import logging

car = CarKeys()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 1. Assume the AWS resource role using STS AssumeRole Action
sts_client = boto3.client('sts')
assumed_role_object = sts_client.assume_role(RoleArn=car.get_role_creds(),
                                             RoleSessionName="AssumeRoleSession1")
credentials = assumed_role_object['Credentials']

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=credentials['AccessKeyId'],
                          aws_secret_access_key=credentials['SecretAccessKey'],
                          aws_session_token=credentials['SessionToken'],
                          region_name='us-east-2'
                          )


def get_item_count(tableName):
    # Access table attribute
    table = dynamodb.Table(tableName)
    logger.info("In get_item_count")
    logger.info(tableName)
    logger.info("item_count")
    logger.info(table.item_count)
    # return table's item count
    return table.item_count


def query_next_item(id, tableName):
    table = dynamodb.Table(tableName)
    logger.info("In query_next_item")
    logger.info("ID")
    logger.info(id)
    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    if len(queryResponse['Items']) <= 0:
        return 'unavailable at this moment', 'Please try again later. '
    return queryResponse['Items'][0]['Name'], queryResponse['Items'][0]['Mission']


def get_total_contribution(id, tableName):
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    return queryResponse['Items'][0]['TotalContribution']


def get_website(id, tableName):
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    return queryResponse['Items'][0]['Website']


def get_tagline(id, tableName):
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    return queryResponse['Items'][0]['Tagline']


def update_total_contribution(id, tableName, updated_contribution):
    table = dynamodb.Table(tableName)
    queryResponse = table.update_item(
        Key={'ID': id},
        UpdateExpression="set #TotalContribution = :c",
        ExpressionAttributeNames={"#TotalContribution": "TotalContribution"},
        ExpressionAttributeValues={":c": updated_contribution},
        ReturnValues="UPDATED_NEW"
    )
    return queryResponse
