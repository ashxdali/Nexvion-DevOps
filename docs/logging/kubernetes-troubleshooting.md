# Nexvion Kubernetes Logging and Troubleshooting

## Overview

Nexvion uses Kubernetes to deploy its e-commerce application
and monitoring components. The troubleshooting script collects
pod status, deployment status, service details, restart counts,
and recent Kubernetes events.

## Requirements

- Kubernetes cluster access
- kubectl installed and configured
- Permission to read resources in the target namespace

## Run the Diagnostic Script

Run the script against the Nexvion namespace:

```bash
./scripts/k8s-troubleshoot.sh
