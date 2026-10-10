#!/usr/bin/env bash

set -u

NAMESPACE="${1:-nexvion}"

echo "=========================================="
echo " Nexvion Kubernetes Troubleshooting"
echo " Namespace: ${NAMESPACE}"
echo " Timestamp: $(date)"
echo "=========================================="

if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
    echo "ERROR: Namespace '$NAMESPACE' does not exist or is inaccessible."
    exit 1
fi

echo
echo "1. POD STATUS"
echo "------------------------------------------"
kubectl get pods -n "$NAMESPACE" -o wide

echo
echo "2. DEPLOYMENT STATUS"
echo "------------------------------------------"
kubectl get deployments -n "$NAMESPACE"

echo
echo "3. SERVICE STATUS"
echo "------------------------------------------"
kubectl get services -n "$NAMESPACE"

echo
echo "4. PODS WITH RESTARTS"
echo "------------------------------------------"
kubectl get pods -n "$NAMESPACE" \
    -o custom-columns='NAME:.metadata.name,READY:.status.containerStatuses[*].ready,RESTARTS:.status.containerStatuses[*].restartCount,STATUS:.status.phase'

echo
echo "5. RECENT NAMESPACE EVENTS"
echo "------------------------------------------"
kubectl get events -n "$NAMESPACE" \
    --sort-by='.lastTimestamp'

echo
echo "=========================================="
echo " Troubleshooting summary complete"
echo "=========================================="



