# Migration Guide

## Before
- 5 Toxiproxy Deployments or Pods per environment
- One container per upstream dependency
- Per-proxy configuration and Service management

## After
- 1 sniproxy Deployment per environment
- 1 LoadBalancer Service exposing ports 443 and 8883
- 1 shared Chaos Mesh installation per cluster for fault injection

## Migration steps
1. Export the list of current Toxiproxy upstream targets.
2. Convert each upstream into a sniproxy table entry in `config/sniproxy.conf` and `k8s/sniproxy/configmap.yaml`.
3. Deploy sniproxy alongside the existing proxies.
4. Update environment-specific DNS so clients resolve the original hostnames to the new sniproxy Service IP.
5. Validate steady-state traffic, then run the provided Chaos Mesh examples.
6. Remove old Toxiproxy workloads after cutover.
