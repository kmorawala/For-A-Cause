import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def register_nonProfit(id, name, email, category, tagline, mission, website):
    #dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    companyInfo = {
        "TableName": "CharityInfo",
        "Item": {
            "ID": {"N": "{id}".format(id=id)},
            "Name": {"S": name},
            "Email": {"S": email},
            "Tagline": {"S": tagline},
            "Category": {"S":category},
            "Mission": {"S": mission},
            "Website": {"S": website},
            "TotalContribution": {"N": "0"}
        }
    }

    try:
        response = dynamodb_client_cloud.put_item(**companyInfo)
        print("Successfully put item.")
        print(response)
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])


def GetNextId(tableName):
    #dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    lastItem = dynamodb_client_cloud.scan(
        TableName=str(tableName)
    )

    try:
        print(len(lastItem["Items"]))
        nextIDNumber = len(lastItem["Items"]) + 1
        return nextIDNumber
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])

