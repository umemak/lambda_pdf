# S3にアップロードされたPDFファイルのテキストを抽出して保存するLambda関数

import boto3
import io
import os
from pdfminer.high_level import extract_text
import pymysql


def handler(event, context):
    # S3からPDFファイルを取得
    s3 = boto3.client("s3")
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = file_obj["Body"].read()
    file_like_object = io.BytesIO(file_content)

    # PDFファイルのテキストを抽出
    text = extract_text(file_like_object)

    # 抽出したテキストをS3に保存
    base = os.path.splitext(os.path.basename(key))[0]
    s3.put_object(Body=text, Bucket=bucket, Key=base + ".txt")

    # 抽出したテキストをMySQLに保存
    # RDSのMySQLインスタンスに接続
    rds_client = boto3.client("rds")
    db_instances = rds_client.describe_db_instances()
    db_instance = db_instances["DBInstances"][0]
    endpoint = db_instance["Endpoint"]["Address"]

    # MySQLデータベースに接続
    connection = pymysql.connect(
        host=endpoint,
        user=os.environ["DB_USER"],
        passwd=os.environ["DB_PASSWORD"],
        db=os.environ["DB_NAME"],
    )
    cursor = connection.cursor()

    # テキストデータを保存するSQL文を実行
    insert_query = "INSERT INTO text_table (file_name, text_data) VALUES (%s, %s)"
    cursor.execute(insert_query, (base, text))
    connection.commit()

    # データベース接続を閉じる
    cursor.close()
    connection.close()
