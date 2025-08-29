
provider "aws" {
  region = var.region
}

module "s3" {
  source = "./modules/s3"
  bucket_name = var.bucket_name
}

module "iam" {
  source = "./modules/iam"
  role_name = var.lambda_role_name
}

module "opensearch" {
  source = "./modules/opensearch"
  domain_name = var.domain_name
}

module "lambda" {
  source = "./modules/lambda"
  lambda_name        = var.lambda_name
  lambda_role_arn    = module.iam.role_arn
  bucket_name        = var.bucket_name
  opensearch_endpoint = module.opensearch.opensearch_endpoint
  index_name         = var.index_name
}
