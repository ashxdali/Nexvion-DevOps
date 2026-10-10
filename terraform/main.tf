terraform {
  required_version = ">= 1.0"
}

resource "local_file" "project_info" {
  filename = "${path.module}/project-info.txt"

  content = <<-EOT
    Project: Nexvion E-Commerce
    Purpose: DevOps and Cloud-Native Delivery Platform
    Infrastructure as Code: Terraform
    Environment: Local Development
  EOT
}
