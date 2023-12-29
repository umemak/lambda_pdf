# S3にアップロードされたPDFファイルの1ページ目をサムネイル化して保存するLambda関数

import boto3
import io
import os
from PIL import Image

def handler(event, context):
    # S3からPDFファイルを取得
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = file_obj['Body'].read()

    # PDFファイルから1ページ目を取得
    pdf = Image.open(io.BytesIO(file_content))
    page = pdf.pages[0]

    # 1ページ目をサムネイル化
    thumbnail = page.resize((256, 256))

    # サムネイルをS3に保存
    thumbnail_key = f'{key}_thumbnail.png'
    s3.put_object(Bucket=bucket, Key=thumbnail_key, Body=io.BytesIO(thumbnail.tobytes()))

    print(f'サムネイルを保存しました: {thumbnail_key}')
