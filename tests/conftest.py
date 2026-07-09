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
