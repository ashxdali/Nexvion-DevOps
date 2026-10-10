# Nexvion — AI-Powered E-Commerce DevOps Platform

Nexvion is an e-commerce application project demonstrating DevOps practices, CI/CD automation, containerization, Kubernetes deployment, monitoring, and security.

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Web Server: NGINX
- Containerization: Docker and Docker Compose
- CI/CD: Jenkins
- Security Scanning: Trivy
- Container Orchestration: Kubernetes and Helm
- Infrastructure as Code: Terraform
- Configuration Management: Ansible
- Monitoring: Prometheus and Grafana
- Log Analysis: Python
- Incident Analysis: Rule-based Python analyzer
- Version Control: Git and GitHub

## Architecture

Developer → GitHub → Jenkins Pipeline → Docker Build → Trivy Security Scan → Docker Compose Deployment → Health Check

A separate Kubernetes deployment demonstrates container orchestration using Kubernetes manifests and Helm.

Prometheus collects NGINX exporter metrics, and Grafana provides a monitoring dashboard.

Terraform manages local project configuration resources, while Ansible automates configuration and deployment tasks.

## Repository Structure

- `application/` — E-commerce frontend application
- `docker/` — Dockerfiles, NGINX configuration, and Compose files
- `jenkins/` — Jenkins pipeline configuration
- `terraform/` — Terraform configuration
- `ansible/` — Ansible inventory and playbooks
- `kubernetes/` — Kubernetes manifests
- `helm/` — Helm chart
- `monitoring/prometheus/` — Prometheus configuration
- `monitoring/grafana/` — Grafana dashboard
- `logging/` — Log analysis scripts and reports
- `ai/incident-analysis/` — Rule-based incident analysis
- `security/` — Security-related resources
- `scripts/` — Automation scripts
- `docs/` — Implementation and troubleshooting documentation

## Docker Deployment

The original application is available at:

http://localhost:8086/

The hardened Docker deployment is available at:

http://localhost:18086/

The hardened deployment uses a non-root container user, a read-only root filesystem, dropped Linux capabilities, and a health check.

## Kubernetes Deployment

The project includes Kubernetes deployments and services, a Helm chart, and a dedicated namespace.

Prometheus and Grafana are configured for local-cluster monitoring.

## CI/CD Pipeline

The Jenkins pipeline performs the following steps:

1. Verify the project.
2. Validate the hardened Docker Compose configuration.
3. Build the hardened Docker image.
4. Scan the image with Trivy.
5. Deploy the application using Docker Compose.
6. Verify the application response and container health.

## Validation

The following checks have been performed:

- Terraform configuration validation
- Ansible playbook syntax checks
- Helm chart linting
- Kubernetes rollout verification
- Python script syntax checks
- Prometheus metrics verification
- Docker health checks and HTTP response verification
- Trivy image security scanning

## Log and Incident Analysis

Python scripts analyze application logs and sample incident logs.

The incident analyzer uses predefined rules and keywords to identify possible issues and suggest investigation steps. Its findings are preliminary and require human verification.

## Project Scope

This is a DevOps learning project. The frontend currently demonstrates e-commerce functionality; production database integration, real payment processing, and a verified cloud deployment are not claimed as completed.

## Author

Ashhad Ali M P

GitHub: https://github.com/ashxdali
