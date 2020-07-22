
# The following creates an AWS IAM Policy to Grant AWS Lambda Access to an Amazon DynamoDB Table
# See below for further details:
# https://aws.amazon.com/blogs/security/how-to-create-an-aws-iam-policy-to-grant-aws-lambda-access-to-an-amazon-dynamodb-table/


class CarKeys:
    def __init__(self):
        self.__role_creds = "YourLambdaPolicyID"

    def get_role_creds(self):
        return self.__role_creds
