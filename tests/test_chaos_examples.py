from chaos_client import ChaosMeshClient, network_chaos, temporary_network_chaos


LATENCY_MANIFEST = {
    "apiVersion": "chaos-mesh.org/v1alpha1",
    "kind": "NetworkChaos",
    "metadata": {"name": "decorated-latency", "namespace": "chaos-testing"},
    "spec": {
        "action": "delay",
        "mode": "all",
        "duration": "5m",
        "selector": {
            "namespaces": ["app-test"],
            "labelSelectors": {"app.kubernetes.io/name": "dotnet-client"},
        },
        "delay": {"latency": "100ms", "correlation": "25", "jitter": "10ms"},
    },
}


@network_chaos(LATENCY_MANIFEST, client=ChaosMeshClient(dry_run=True))
def test_latency_injection_decorator() -> None:
    assert LATENCY_MANIFEST["spec"]["delay"]["latency"] == "100ms"


def test_network_partition_context_manager(chaos_client: ChaosMeshClient, partition_manifest: dict) -> None:
    with temporary_network_chaos(partition_manifest, client=chaos_client) as applied_manifest:
        assert applied_manifest["spec"]["action"] == "partition"
        assert applied_manifest["spec"]["target"]["selector"]["namespaces"] == ["sniproxy"]


def test_packet_loss_apply_and_remove(chaos_client: ChaosMeshClient, packet_loss_manifest: dict) -> None:
    applied_manifest = chaos_client.apply_network_chaos(packet_loss_manifest)

    assert applied_manifest["spec"]["loss"]["loss"] == "30"

    chaos_client.remove_network_chaos(
        applied_manifest["metadata"]["name"],
        applied_manifest["metadata"]["namespace"],
    )
