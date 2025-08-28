
import boto3, json, os
from requests_aws4auth import AWS4Auth
import requests

region = os.environ["REGION"]
index = os.environ["INDEX"]
os_endpoint = os.environ["OPENSEARCH_ENDPOINT"]

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, "es", session_token=credentials.token)

bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):
    question = event["question"]
    embed_payload = { "inputText": question }
    resp = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps(embed_payload),
        contentType="application/json",
        accept="application/json"
    )
    q_vector = json.loads(resp["body"].read())["embedding"]

    knn_query = {
      "size": 3,
      "query": {
        "knn": {
          "vector": {
            "vector": q_vector,
            "k": 3
          }
        }
      }
    }

    search_url = f"https://{os_endpoint}/{index}/_search"
    r = requests.post(search_url, json=knn_query, auth=awsauth)
    docs = [hit["_source"]["text"] for hit in r.json()["hits"]["hits"]]

    prompt = f"Answer this question: '{question}' using context:\n" + "\n".join(docs)
    bedrock_resp = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({ "prompt": prompt, "max_tokens_to_sample": 300 }),
        contentType="application/json",
        accept="application/json"
    )
    answer = json.loads(bedrock_resp["body"].read())["completion"]
    return {"answer": answer}
