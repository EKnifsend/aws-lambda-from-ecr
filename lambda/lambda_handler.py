import json


def lambda_handler(event, context):
    # TODO implement
    message = "Hello from Lambda using the aws CDK via DockerImageCode!"
    return {"statusCode": 200, "body": json.dumps(message)}
