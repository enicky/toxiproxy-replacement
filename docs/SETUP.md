# Setup Guide

## 5-minute deployment

1. Build and publish the sniproxy image:
   ```bash
   docker build -t ghcr.io/enicky/toxiproxy-replacement/sniproxy:latest .
   docker push ghcr.io/enicky/toxiproxy-replacement/sniproxy:latest
   ```
2. Install Chaos Mesh once per cluster:
   ```bash
   ./scripts/install-chaos-mesh.sh
   ```
3. Deploy one sniproxy instance per environment:
   ```bash
   kubectl apply -f k8s/sniproxy/namespace.yaml
   kubectl apply -f k8s/sniproxy/configmap.yaml
   kubectl apply -f k8s/sniproxy/deployment.yaml
   kubectl apply -f k8s/sniproxy/service.yaml
   ```
4. Point your per-environment DNS records at the Service `EXTERNAL-IP`.
5. Run chaos tests with `pytest tests/test_chaos_examples.py -q`.

## Adding multiple DNS records

Every proxied hostname is a single line in the appropriate sniproxy table:

```text
table https_hosts {
    config-service.example.com config-service.example.com:443
    web-gateway.example.com web-gateway.example.com:443
    internal-api.local 10.40.4.8:443
    partner-api.example.com partner-api.example.com:443
}

table mqtt_hosts {
    mqtt-hub.azure.example.com mqtt-hub.azure.example.com:8883
}
```

Use the left side for the SNI hostname clients connect to and the right side for the upstream destination. IP-based upstreams are supported exactly like `internal-api.local 10.40.4.8:443`.

## Local test loop

```bash
docker compose up --build -d
openssl s_client -connect 127.0.0.1:443 -servername config-service.example.com
openssl s_client -connect 127.0.0.1:8883 -servername mqtt-hub.azure.example.com
```
