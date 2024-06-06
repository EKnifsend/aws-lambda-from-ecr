import subprocess
import json
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    Duration,
    aws_ecr,
    aws_ecr_assets,
    aws_iam,
    aws_lambda,
)
from constructs import Construct


class AwsCdkTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        account_id = "<your-aws-account>"
        region = "<your-region>"

        # 1. Create ECR repository
        # ecr_repository = aws_ecr.Repository(
        #     self, "EthanTestRepo", repository_name="ethan-test-repo"
        # )

        # 2. IAM role for Lambda
        with open("policy.json", "r") as policy_file:
            assume_role_policy_document = json.load(policy_file)

        lambda_role = aws_iam.Role(
            self,
            "LambdaBasicRole",
            role_name="lambda-basic-role",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "AssumeRolePolicy": aws_iam.PolicyDocument.from_json(
                    assume_role_policy_document
                )
            },
        )

        # Grant necessary permissions to the role
        lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        # Define the Docker image asset
        # docker_image_asset = aws_ecr_assets.DockerImageAsset(
        #     self,
        #     "EthanTestImage",
        #     directory="/Users/knify/Documents/AWS_CDK_Test/",
        # )

        # Get ECR login password and login to Docker
        # login_password = (
        #     subprocess.check_output(
        #         ["aws", "ecr", "get-login-password", "--region", region]
        #     )
        #     .decode("utf-8")
        #     .strip()
        # )

        # subprocess.run(
        #     [
        #         "docker",
        #         "login",
        #         "--username",
        #         "AWS",
        #         "--password-stdin",
        #         f"{account_id}.dkr.ecr.{region}.amazonaws.com",
        #     ],
        #     input=login_password,
        #     text=True,
        # )

        # # 3. Tag Docker image
        # subprocess.run(
        #     [
        #         "docker",
        #         "tag",
        #         "ethan-test-image:latest",
        #         f"{account_id}.dkr.ecr.{region}.amazonaws.com/ethan-test-repo:ethan-test-image",
        #     ]
        # )

        # # 4. Push Docker image to ECR
        # subprocess.run(
        #     [
        #         "docker",
        #         "push",
        #         f"{account_id}.dkr.ecr.{region}.amazonaws.com/ethan-test-repo:ethan-test-image",
        #     ]
        # )

        # 5. Create Lambda function
        # lambda_function = aws_lambda.DockerImageFunction(
        #     self,
        #     "MyLambdaFunction",
        #     function_name="my-lambda-function",
        #     code=aws_lambda.DockerImageCode.from_ecr(
        #         docker_image_asset.repository,
        #         tag="latest",
        #     ),
        #     timeout=Duration.seconds(900),
        #     memory_size=384,
        #     role=lambda_role,
        # )

        lambda_function = aws_lambda.DockerImageFunction(
            self,
            "MyLambdaFunction",
            function_name="my-lambda-function",
            code=aws_lambda.DockerImageCode.from_image_asset(
                "./", platform=aws_ecr_assets.Platform.LINUX_AMD64
            ),
            timeout=Duration.seconds(900),
            memory_size=384,
            role=lambda_role,
        )

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsCdkTestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
