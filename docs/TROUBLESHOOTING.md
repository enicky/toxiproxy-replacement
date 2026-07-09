# Troubleshooting

## sniproxy routes to the fallback backend
- Confirm the client is sending the expected SNI hostname.
- Check the relevant `table` entry in `/etc/sniproxy.conf` for typos.
- Verify the upstream endpoint is reachable from the cluster.

## The Service has no external IP
- Confirm your cluster supports `LoadBalancer` Services.
- On local clusters, use MetalLB or change the Service type to `NodePort` for development.

## Chaos Mesh experiments do not start
- Confirm Chaos Mesh is installed in the namespace defined by `CHAOS_NAMESPACE`.
- Verify the target application pods match the selectors in `k8s/chaos-mesh/*.yaml`.
- Run `kubectl get networkchaos -n chaos-testing` and `kubectl describe networkchaos <name> -n chaos-testing`.

## .NET clients fail during tests
- Keep TLS passthrough enabled; do not terminate TLS in sniproxy.
- Make sure the client still resolves the original hostname to the sniproxy Service IP.
- For timeout simulations, ensure the client's configured timeout is shorter than the injected delay.
