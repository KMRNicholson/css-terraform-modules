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

variable "vm_name_input" {
  type        = string
}

resource "google_compute_network" "vpc_network" {
  name = "tf-mod2"
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "firewall" {
  name    = "tf-mod2-allow-ssh-and-http"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22", "80"]
  }

  source_tags = ["css-tf"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name_input
  machine_type = "f1-micro"
  zone         = "europe-central2-a"

  boot_disk {
    initialize_params {
      size  = 10
      image = "debian-cloud/debian-11"
      type  = "pd-balanced"
    }
  }

  labels = {
    course = "css-gcp"
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }

  metadata_startup_script = "apt update && apt -y install apache2"

  tags = [
    "http-server"
  ]
}

output "vm_name" {
  value = google_compute_instance.vm_instance.name
}

output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip
}