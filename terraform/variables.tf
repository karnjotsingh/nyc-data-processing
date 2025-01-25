variable "credentials" {
  description = "My Credentials"
  default     = "/path/to/credentials"
}

variable "project" {
  description = "Project"
  default     = "<Project-ID>"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "nyc_taxi_bq_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "nyc-taxi-gcs-bucket-448900"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}