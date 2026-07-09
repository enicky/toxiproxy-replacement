import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chaos_client import ChaosMeshClient, build_network_chaos_manifest


@pytest.fixture
def chaos_client() -> ChaosMeshClient:
    return ChaosMeshClient(dry_run=True)


@pytest.fixture
def workload_selector() -> dict:
    return {
        "namespaces": ["app-test"],
        "labelSelectors": {"app.kubernetes.io/name": "dotnet-client"},
    }


@pytest.fixture
def partition_manifest(workload_selector: dict) -> dict:
    return build_network_chaos_manifest(
        name="sniproxy-partition",
        namespace="chaos-testing",
        action="partition",
        mode="all",
        duration="5m",
        selector=workload_selector,
        direction="to",
        target={
            "mode": "all",
            "selector": {
                "namespaces": ["sniproxy"],
                "labelSelectors": {"app.kubernetes.io/name": "sniproxy"},
            },
        },
    )


@pytest.fixture
def latency_manifest(workload_selector: dict) -> dict:
    return build_network_chaos_manifest(
        name="sniproxy-latency",
        namespace="chaos-testing",
        action="delay",
        mode="all",
        duration="5m",
        selector=workload_selector,
        delay={"latency": "100ms", "correlation": "25", "jitter": "10ms"},
    )


@pytest.fixture
def packet_loss_manifest(workload_selector: dict) -> dict:
    return build_network_chaos_manifest(
        name="sniproxy-packet-loss",
        namespace="chaos-testing",
        action="loss",
        mode="all",
        duration="5m",
        selector=workload_selector,
        loss={"loss": "30", "correlation": "25"},
    )


@pytest.fixture
def config_service_partition_manifest(workload_selector: dict) -> dict:
    """Chaos targeting only config-service.example.com endpoint."""
    return build_network_chaos_manifest(
        name="config-service-partition",
        namespace="chaos-testing",
        action="partition",
        mode="all",
        duration="5m",
        selector=workload_selector,
        direction="to",
        external_targets=["config-service.example.com"],
    )


@pytest.fixture
def config_service_latency_manifest(workload_selector: dict) -> dict:
    """Latency injection targeting only config-service.example.com endpoint."""
    return build_network_chaos_manifest(
        name="config-service-latency",
        namespace="chaos-testing",
        action="delay",
        mode="all",
        duration="5m",
        selector=workload_selector,
        direction="to",
        external_targets=["config-service.example.com"],
        delay={"latency": "500ms", "correlation": "25", "jitter": "50ms"},
    )


@pytest.fixture
def config_service_packet_loss_manifest(workload_selector: dict) -> dict:
    """Packet loss targeting only config-service.example.com endpoint."""
    return build_network_chaos_manifest(
        name="config-service-packet-loss",
        namespace="chaos-testing",
        action="loss",
        mode="all",
        duration="5m",
        selector=workload_selector,
        direction="to",
        external_targets=["config-service.example.com"],
        loss={"loss": "50", "correlation": "25"},
    )
