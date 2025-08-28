
resource "aws_opensearch_domain" "faq" {
  domain_name     = var.domain_name
  engine_version  = "OpenSearch_2.11"
  cluster_config {
    instance_type = "t3.small.search"
    instance_count = 1
  }
  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }
  access_policies = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = "*",
      Action = "es:*",
      Resource = "*"
    }]
  })
  advanced_options = {
    "rest.action.multi.allow_explicit_index" = "true"
  }
}

output "opensearch_endpoint" {
  value = aws_opensearch_domain.faq.endpoint
}
