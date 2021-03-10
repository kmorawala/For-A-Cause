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
    try:
        if table.item_count == None:
            logger.info("Table item count is None in get_item_count")
            return 0
        else:
            return table.item_count
    except:
        logger.info("Error occured in get_item_count")
        return 0


def query_next_item(id, tableName):
    table = dynamodb.Table(tableName)
    logger.info("In query_next_item")
    logger.info("ID")
    logger.info(id)
    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    try:
        if len(queryResponse['Items']) <= 0:
            logger.info(
                "Invalid number of items in the DynamoDB databse per In query_next_item")
            return 'unavailable at this moment', 'Please try again later. '
        else:
            return queryResponse['Items'][0]['Name'], queryResponse['Items'][0]['Mission']
    except:
        logger.info("Error occured in query_next_item")
        return 'unavailable at this moment', 'Please try again later. '


def get_total_contribution(id, tableName):
    logger.info("In get_total_contribution")
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    try:
        if queryResponse:
            return queryResponse['Items'][0]['TotalContribution']
        else:
            logger.info(
                "get_total_contribution is None in get_total_contribution")
            return -1
    except:
        logger.info("Error occured in get_total_contribution")
        return -1


def get_website(id, tableName):
    logger.info("In get_website")
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    try:
        if queryResponse:
            return queryResponse['Items'][0]['Website']
        else:
            logger.info("website is None in get_website")
            return 'Not available at the moment'
    except:
        logger.info("Error occured in get_total_contribution")
        return 'Not available at the moment'


def get_tagline(id, tableName):
    table = dynamodb.Table(tableName)

    queryResponse = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    try:
        if queryResponse:
            return queryResponse['Items'][0]['Tagline']
        else:
            logger.info("Tagline is None in get_tagline")
            return 'Not available at the moment'
    except:
        logger.info("Error occured in get_tagline")
        return 'Not available at the moment'


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
