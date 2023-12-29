from aws_cdk import (
    Duration,
    Stack,
)
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3_notifications as s3n
from constructs import Construct


class LambdaPdfStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3バケットの作成
        bucket = s3.Bucket(self, "MyFirstBucket", versioned=True)

        # lambda/thumbnail.handlerからlambda関数を作成する
        thumbnail_function = lambda_.Function(
            self,
            "MyFirstLambda",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="thumbnail.handler",
            timeout=Duration.seconds(300),
            code=lambda_.Code.from_asset('lambda'),
        )

        # bucketにファイルが保存されたらthumbnail_functionを呼び出すトリガーを作成する
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(thumbnail_function)
        )

        # bucketの読み書き権限をthumbnail_functionに付与する
        bucket.grant_read_write(thumbnail_function)
