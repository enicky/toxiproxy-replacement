#!/usr/bin/env bash
set -euo pipefail

CHAOS_NAMESPACE="${CHAOS_NAMESPACE:-chaos-testing}"
helm uninstall chaos-mesh --namespace "$CHAOS_NAMESPACE"
kubectl delete namespace "$CHAOS_NAMESPACE" --ignore-not-found=true
