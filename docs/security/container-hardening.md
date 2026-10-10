# Nexvion Container Security Hardening

## Objective

Harden the Nexvion static e-commerce application container while
preserving application functionality.

## Security Controls Implemented

The hardened test image uses the following controls:

- Runs as a non-root user (`101:101`).
- Uses a read-only root filesystem.
- Provides temporary writable storage through `/tmp`.
- Enables `no-new-privileges`.
- Drops all Linux capabilities.
- Uses a custom NGINX configuration listening on port 8080.

## Validation Results

| Test | Result |
|---|---|
| NGINX configuration validation | Passed |
| Non-root execution | Passed |
| Read-only filesystem | Passed |
| Linux capabilities dropped | Passed |
| no-new-privileges | Passed |
| HTTP request to the website | HTTP 200 |

## Test Environment

The hardened test container was exposed on host port 18086.

The existing application container on host port 8086 was not modified
during these tests.

## Limitations

These results validate the tested local Docker configuration. They do
not constitute a complete security audit.

The hardened configuration must be integrated into the main Compose
deployment only after reviewing the Jenkins pipeline and deployment
requirements.
