from aws_cdk import (
    Duration,
    Stack,
    BundlingOptions,
)
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3_notifications as s3n
from constructs import Construct
import os


class LambdaPdfStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3バケットの作成
        bucket = s3.Bucket(self, "MyFirstBucket", versioned=True)

        thumbnail_function = lambda_.Function(
            self,
            "ThumbnailFunctionLambda",
            code=lambda_.EcrImageCode.from_asset_image(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/thumbnail"),
            ),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            timeout=Duration.seconds(300),
        )
        extract_text_function = lambda_.Function(
            self,
            "ExtractTextFunctionLambda",
            code=lambda_.EcrImageCode.from_asset_image(
                directory=os.path.join(os.path.dirname(__file__), "../lambda/extract_text"),
            ),
            handler=lambda_.Handler.FROM_IMAGE,
            runtime=lambda_.Runtime.FROM_IMAGE,
            timeout=Duration.seconds(300),
        )

        # bucketにファイルが保存されたらthumbnail_functionを呼び出すトリガーを作成する
        # bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(thumbnail_function))
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(extract_text_function))

        # bucketの読み書き権限をfunctionsに付与する
        bucket.grant_read_write(thumbnail_function)
        bucket.grant_read_write(extract_text_function)
