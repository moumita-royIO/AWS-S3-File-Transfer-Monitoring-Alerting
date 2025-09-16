variable "bucket_name" {
  description = "S3 bucket to monitor"
  type        = string
}

variable "owner_email" {
  description = "Verified SES email to receive alerts"
  type        = string
}
