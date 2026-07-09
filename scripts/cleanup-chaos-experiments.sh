#!/usr/bin/env bash
set -euo pipefail

CHAOS_NAMESPACE="${CHAOS_NAMESPACE:-chaos-testing}"
kubectl delete networkchaos --all --namespace "$CHAOS_NAMESPACE" --ignore-not-found=true
