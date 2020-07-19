import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def register_nonProfit(id, name, email, category, tagline, mission, website):
    #For testing locally
    #dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    #For deployment
    dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    #Creates a new row in the CharityInfo table
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


#Generates the next ID for the next entry
def GetNextId(tableName):
    #For testing locally
    #dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    #For deployment
    dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    lastItem = dynamodb_client_cloud.scan(
        TableName=str(tableName)
    )

    try:
        nextIDNumber = len(lastItem["Items"]) + 1
        return nextIDNumber
        # Handle response
    except BaseException as error:
        print("Unknown error while putting item: " + error.response['Error']['Message'])


def query_if_already_exists(name):
    #For testing locally
    #dynamodb_client_local = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    #For Deployment
    dynamodb_client_cloud = boto3.client("dynamodb", region_name="us-east-2")

    try:
        response = dynamodb_client_cloud.scan(
            TableName="CharityInfo",
            FilterExpression='#n = :n',
            ExpressionAttributeNames={
                "#n": "Name"
            },
            ExpressionAttributeValues={
                ":n": {"S": name}
            }
        )

        count = 0
        for i in response["Items"]:
            count += 1

        if len(response["Items"]) > 0:
            return True
        else:
            return False
        # Handle response
    except BaseException as error:
        return "Unknown error while querying: " + error.response['Error']['Message']

