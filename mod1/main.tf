terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

variable "project" {}

provider "google" {
  credentials = file(var.project.key_file)

  project = var.project.name
}

resource "google_compute_network" "vpc_network" {
  name = "${var.project.resources.prefix}-network"
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "firewall" {
  name    = "${var.project.resources.prefix}-allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_tags = var.project.resources.firewall.source_tags
  source_ranges = var.project.resources.firewall.source_ranges
}

resource "google_compute_instance" "vm_instance" {
  name         = var.project.resources.compute_instances[0].name
  machine_type = var.project.resources.compute_instances[0].machine_type
  zone         = var.project.resources.compute_instances[0].zone

  boot_disk {
    initialize_params {
      size  = 10
      image = "debian-cloud/debian-10"
      type  = "pd-balanced"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }

  tags = [
    "http-server"
  ]
}

