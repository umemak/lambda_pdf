# S3にアップロードされたPDFファイルの1ページ目をサムネイル化して保存するLambda関数

import boto3
import io
import os
from PIL import Image
from pdf2image import convert_from_bytes

def handler(event, context):
    # S3からPDFファイルを取得
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = file_obj['Body'].read()

    pages = convert_from_bytes(file_content)

    # pagesはPILのImageリストなのでbyteに変換
    img_bytes = io.BytesIO()
    pages[0].save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    base = os.path.splitext(os.path.basename(key))[0]
    s3.put_object(Body=img_bytes,Bucket=bucket,Key=base+'.png')
