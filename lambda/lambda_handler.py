import json


def lambda_handler(event, context):
    # TODO implement
    message = "Hello from lambda using an ecr image!"
    return {"statusCode": 200, "body": json.dumps(message)}
