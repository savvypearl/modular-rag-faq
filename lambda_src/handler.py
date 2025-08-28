
import boto3, json, os
from requests_aws4auth import AWS4Auth
import requests

region = os.environ["REGION"]
bucket = os.environ["BUCKET"]
index = os.environ["INDEX"]
os_endpoint = os.environ["OPENSEARCH_ENDPOINT"]

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, "es", session_token=credentials.token)

bedrock = boto3.client("bedrock-runtime")
s3 = boto3.client("s3")

def lambda_handler(event, context):
    key = event["Records"][0]["s3"]["object"]["key"]
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8")
    chunks = [text[i:i+300] for i in range(0, len(text), 300)]

    for i, chunk in enumerate(chunks):
        payload = { "inputText": chunk }
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )
        vec = json.loads(response["body"].read())["embedding"]
        doc = {"text": chunk, "vector": vec}
        r = requests.put(f"https://{os_endpoint}/{index}/_doc/{key}-{i}", json=doc, auth=awsauth)

    return {"status": "indexed", "chunks": len(chunks)}
