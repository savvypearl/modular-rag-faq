
resource "aws_lambda_function" "faq_embed_lambda" {
  function_name = var.lambda_name
  role          = var.lambda_role_arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60
  memory_size   = 512
  filename      = "lambda_src.zip"
  source_code_hash = filebase64sha256("lambda_src.zip")

  environment {
    variables = {
      REGION               = "us-east-1"
      BUCKET               = var.bucket_name
      INDEX                = var.index_name
      OPENSEARCH_ENDPOINT  = var.opensearch_endpoint
    }
  }
}
