from __future__ import annotations

import json
import os
import subprocess
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Dict, Generator, Mapping, MutableMapping

Manifest = Dict[str, Any]
ManifestFactory = Callable[..., Manifest]


def build_network_chaos_manifest(
    *,
    name: str,
    namespace: str,
    action: str,
    mode: str,
    selector: Mapping[str, Any],
    duration: str | None = None,
    target: Mapping[str, Any] | None = None,
    external_targets: list[str] | None = None,
    delay: Mapping[str, str] | None = None,
    loss: Mapping[str, str] | None = None,
    labels: Mapping[str, str] | None = None,
    annotations: Mapping[str, str] | None = None,
    direction: str | None = None,
) -> Manifest:
    manifest: MutableMapping[str, Any] = {
        "apiVersion": "chaos-mesh.org/v1alpha1",
        "kind": "NetworkChaos",
        "metadata": {
            "name": name,
            "namespace": namespace,
        },
        "spec": {
            "action": action,
            "mode": mode,
            "selector": dict(selector),
        },
    }

    if labels:
        manifest["metadata"]["labels"] = dict(labels)
    if annotations:
        manifest["metadata"]["annotations"] = dict(annotations)
    if duration:
        manifest["spec"]["duration"] = duration
    if target:
        manifest["spec"]["target"] = dict(target)
    if external_targets:
        manifest["spec"]["externalTargets"] = list(external_targets)
    if delay:
        manifest["spec"]["delay"] = dict(delay)
    if loss:
        manifest["spec"]["loss"] = dict(loss)
    if direction:
        manifest["spec"]["direction"] = direction

    return dict(manifest)


class ChaosMeshClient:
    def __init__(self, kubectl: str = "kubectl", dry_run: bool | None = None) -> None:
        self.kubectl = kubectl
        self.dry_run = dry_run if dry_run is not None else os.getenv("CHAOS_MESH_DRY_RUN", "0") == "1"

    def apply_network_chaos(self, manifest: Manifest) -> Manifest:
        if self.dry_run:
            return manifest

        subprocess.run(
            [self.kubectl, "apply", "-f", "-"],
            input=json.dumps(manifest).encode("utf-8"),
            check=True,
        )
        return manifest

    def remove_network_chaos(self, name: str, namespace: str) -> None:
        if self.dry_run:
            return

        subprocess.run(
            [
                self.kubectl,
                "delete",
                "networkchaos",
                name,
                "--namespace",
                namespace,
                "--ignore-not-found=true",
            ],
            check=True,
        )


def apply_network_chaos(manifest: Manifest, *, client: ChaosMeshClient | None = None) -> Manifest:
    return (client or ChaosMeshClient()).apply_network_chaos(manifest)


def remove_network_chaos(name: str, namespace: str, *, client: ChaosMeshClient | None = None) -> None:
    (client or ChaosMeshClient()).remove_network_chaos(name, namespace)


@contextmanager
def temporary_network_chaos(
    manifest: Manifest,
    *,
    client: ChaosMeshClient | None = None,
) -> Generator[Manifest, None, None]:
    active_client = client or ChaosMeshClient()
    applied_manifest = active_client.apply_network_chaos(manifest)
    try:
        yield applied_manifest
    finally:
        metadata = manifest["metadata"]
        active_client.remove_network_chaos(metadata["name"], metadata["namespace"])


def network_chaos(manifest_or_factory: Manifest | ManifestFactory, *, client: ChaosMeshClient | None = None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            manifest = manifest_or_factory(*args, **kwargs) if callable(manifest_or_factory) else manifest_or_factory
            with temporary_network_chaos(manifest, client=client):
                return func(*args, **kwargs)

        return wrapper

    return decorator
