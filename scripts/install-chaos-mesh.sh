#!/usr/bin/env bash
set -euo pipefail

CHAOS_NAMESPACE="${CHAOS_NAMESPACE:-chaos-testing}"
CHAOS_VERSION="${CHAOS_VERSION:-2.7.2}"

helm repo add chaos-mesh https://charts.chaos-mesh.org >/dev/null 2>&1 || true
helm repo update
helm upgrade --install chaos-mesh chaos-mesh/chaos-mesh \
  --namespace "$CHAOS_NAMESPACE" \
  --create-namespace \
  --version "$CHAOS_VERSION" \
  --set chaosDaemon.runtime=containerd \
  --set controllerManager.replicaCount=1 \
  --set dashboard.create=true \
  --set dnsServer.create=true
