terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project     = "css-kohdynicholson-2023"
  region      = "europe-central2"
  zone        = "europe-central2-a"
}

variable "bucket_name" {
  type        = string
}

variable "folder_name" {
  type        = string
}

resource "google_storage_bucket" "empty_bucket" {
  name        = var.bucket_name
  location    = "EU"
  uniform_bucket_level_access = true
  force_destroy = true
}

resource "google_storage_bucket_object" "empty_folder" {
  name        = var.folder_name # folder name should end with '/'
  content     = "This content does not matter"
  bucket      = google_storage_bucket.empty_bucket.name
}