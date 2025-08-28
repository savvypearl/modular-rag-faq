
resource "aws_s3_bucket" "faq_upload" {
  bucket = var.bucket_name
}

output "bucket_id" {
  value = aws_s3_bucket.faq_upload.id
}
