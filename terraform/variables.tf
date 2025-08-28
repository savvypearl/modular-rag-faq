
variable "region" { default = "us-east-1" }
variable "bucket_name" { default = "faq-upload-savvypearl" }
variable "lambda_name" { default = "faqEmbedLambda" }
variable "lambda_role_name" { default = "rag_lambda_exec_role" }
variable "domain_name" { default = "faq-rag-domain" }
variable "index_name" { default = "faq-knn-index" }
