from aws_cdk import Duration, Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as sfn_tasks
from aws_cdk import aws_iam as iam
from constructs import Construct
import os


class LambdaPdfStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3バケットの作成
        bucket = s3.Bucket(self, "MyFirstBucket", versioned=True)

        # Lambda関数の作成
        # サムネイル作成
        thumbnail_function = lambda_.Function(
            self,
            "ThumbnailFunctionLambda",
            code=lambda_.EcrImageCode.from_asset_image(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/thumbnail"),
            ),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            timeout=Duration.seconds(300),
            memory_size=3000,
        )
        # テキスト抽出
        extract_text_function = lambda_.Function(
            self,
            "ExtractTextFunctionLambda",
            code=lambda_.EcrImageCode.from_asset_image(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/extract_text"),
            ),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            timeout=Duration.seconds(300),
            memory_size=3000,
        )

        # Step Functionsの作成
        start_state = sfn.Pass(self, "StartState")
        thumbnail_lambda_state = sfn_tasks.LambdaInvoke(
            self, "InvokeThumbnailLambda", lambda_function=thumbnail_function
        )
        extract_text_lambda_state = sfn_tasks.LambdaInvoke(
            self, "InvokeExtractTextLambda", lambda_function=extract_text_function
        )
        # Parallelステートの作成
        parallel_state = sfn.Parallel(self, "ParallelState")
        parallel_state.branch(thumbnail_lambda_state)
        parallel_state.branch(extract_text_lambda_state)

        definition = sfn.Chain.start(start_state).next(parallel_state)
        state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
        )

        lambda_role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["states:StartExecution"],
                resources=[state_machine.state_machine_arn],
            )
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
        )

        # StepFunctionsの起動
        sfn_exec_function = lambda_.Function(
            self,
            "SFNExecFunction",
            code=lambda_.Code.from_inline(
                f"""
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn='{state_machine.state_machine_arn}',
        input=json.dumps(event),
    )
    """
            ),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            role=lambda_role,
        )
        # bucketの読み書き権限をfunctionsに付与する
        bucket.grant_read_write(thumbnail_function)
        bucket.grant_read_write(extract_text_function)

        # bucketにPDFファイルが保存されたらlambdaを呼び出すトリガーを作成する
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(sfn_exec_function),
            s3.NotificationKeyFilter(suffix=".pdf"),  # .pdfファイルのみをフィルタリング
        )
