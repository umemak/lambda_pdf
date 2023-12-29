# S3にアップロードされたPDFファイルのテキストを抽出して保存するLambda関数

import boto3
import io
import os
from pdfminer.high_level import extract_text

def handler(event, context):
    # S3からPDFファイルを取得
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = file_obj['Body'].read()
    file_like_object = io.BytesIO(file_content)

    # PDFファイルのテキストを抽出
    text = extract_text(file_like_object)

    # 抽出したテキストをS3に保存
    base = os.path.splitext(os.path.basename(key))[0]
    s3.put_object(Body=text,Bucket=bucket,Key=base+'.txt')
