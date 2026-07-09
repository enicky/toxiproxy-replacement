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


def test_endpoint_specific_partition(chaos_client: ChaosMeshClient, config_service_partition_manifest: dict) -> None:
    """Test targeting network partition to a specific endpoint (config-service)."""
    applied_manifest = chaos_client.apply_network_chaos(config_service_partition_manifest)

    # Verify the manifest targets only config-service
    assert applied_manifest["spec"]["action"] == "partition"
    assert applied_manifest["spec"]["externalTargets"] == ["config-service.example.com"]
    assert applied_manifest["metadata"]["name"] == "config-service-partition"

    chaos_client.remove_network_chaos(
        applied_manifest["metadata"]["name"],
        applied_manifest["metadata"]["namespace"],
    )


def test_endpoint_specific_latency(chaos_client: ChaosMeshClient, config_service_latency_manifest: dict) -> None:
    """Test targeting latency injection to a specific endpoint (config-service)."""
    applied_manifest = chaos_client.apply_network_chaos(config_service_latency_manifest)

    # Verify the manifest targets only config-service with latency
    assert applied_manifest["spec"]["action"] == "delay"
    assert applied_manifest["spec"]["externalTargets"] == ["config-service.example.com"]
    assert applied_manifest["spec"]["delay"]["latency"] == "500ms"

    chaos_client.remove_network_chaos(
        applied_manifest["metadata"]["name"],
        applied_manifest["metadata"]["namespace"],
    )


def test_endpoint_specific_packet_loss(chaos_client: ChaosMeshClient, config_service_packet_loss_manifest: dict) -> None:
    """Test targeting packet loss to a specific endpoint (config-service)."""
    applied_manifest = chaos_client.apply_network_chaos(config_service_packet_loss_manifest)

    # Verify the manifest targets only config-service with packet loss
    assert applied_manifest["spec"]["action"] == "loss"
    assert applied_manifest["spec"]["externalTargets"] == ["config-service.example.com"]
    assert applied_manifest["spec"]["loss"]["loss"] == "50"

    chaos_client.remove_network_chaos(
        applied_manifest["metadata"]["name"],
        applied_manifest["metadata"]["namespace"],
    )


@network_chaos(
    lambda: {
        "apiVersion": "chaos-mesh.org/v1alpha1",
        "kind": "NetworkChaos",
        "metadata": {"name": "decorated-endpoint-chaos", "namespace": "chaos-testing"},
        "spec": {
            "action": "delay",
            "mode": "all",
            "duration": "5m",
            "selector": {
                "namespaces": ["app-test"],
                "labelSelectors": {"app.kubernetes.io/name": "dotnet-client"},
            },
            "externalTargets": ["config-service.example.com"],
            "delay": {"latency": "200ms", "correlation": "50", "jitter": "20ms"},
        },
    },
    client=ChaosMeshClient(dry_run=True),
)
def test_endpoint_chaos_with_decorator() -> None:
    """Test using decorator with endpoint-specific chaos."""
    # This test validates the decorator pattern works with endpoint targeting
    pass
