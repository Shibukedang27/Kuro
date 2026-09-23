"""Minimal Kuro-native package manifest and lockfile support."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from pathlib import Path


@dataclass(frozen=True)
class PackageManifest:
    name: str
    version: str
    entry: str
    dependencies: dict[str, str]


class LockfileError(ValueError):
    """Raised when a Kuro lockfile is malformed or stale."""


_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")


def read_manifest(path: str | Path) -> PackageManifest:
    values: dict[str, str] = {}
    deps: dict[str, str] = {}
    section = ""
    for number, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line == "[dependencies]":
            section = "dependencies"
            continue
        if "=" not in line:
            raise ValueError(f"line {number}: expected key = \"value\"")
        key, value = (part.strip() for part in line.split("=", 1))
        if not (len(value) >= 2 and value[0] == value[-1] == '"'):
            raise ValueError(f"line {number}: values must be quoted")
        if section == "dependencies":
            deps[key] = value[1:-1]
        else:
            values[key] = value[1:-1]
    missing = [key for key in ("name", "version", "entry") if key not in values]
    if missing:
        raise ValueError("missing required fields: " + ", ".join(missing))
    if not values["name"]:
        raise ValueError("package name cannot be empty")
    if not _SEMVER.fullmatch(values["version"]):
        raise ValueError("version must use semantic versioning (for example 1.2.3)")
    return PackageManifest(values["name"], values["version"], values["entry"], deps)


def resolve_manifest(path: str | Path) -> list[tuple[str, str]]:
    root = Path(path).resolve()
    seen: set[Path] = set()
    active: set[Path] = set()
    resolved: list[tuple[str, str]] = []

    def visit(manifest_path: Path):
        if manifest_path in active:
            raise ValueError(f"package dependency cycle at {manifest_path}")
        if manifest_path in seen:
            return
        manifest = read_manifest(manifest_path)
        active.add(manifest_path)
        entry = (manifest_path.parent / manifest.entry).resolve()
        try:
            entry.relative_to(manifest_path.parent)
            entry_inside = True
        except ValueError:
            entry_inside = False
        if not entry_inside:
            raise ValueError(f"entry escapes package root: {manifest.entry}")
        if not entry.is_file():
            raise ValueError(f"entry source not found: {manifest.entry}")
        for name, relative in sorted(manifest.dependencies.items()):
            dep_manifest = (manifest_path.parent / relative / "kuro.package").resolve()
            try:
                dep_manifest.relative_to(manifest_path.parent)
                dependency_inside = True
            except ValueError:
                dependency_inside = False
            if not dependency_inside:
                raise ValueError(f"dependency {name!r} escapes package root: {relative}")
            if not dep_manifest.is_file():
                raise ValueError(f"dependency {name!r} not found at {relative}")
            visit(dep_manifest)
        active.remove(manifest_path)
        seen.add(manifest_path)
        resolved.append((manifest.name, manifest.version))

    visit(root)
    return resolved


def write_lock(path: str | Path, packages: list[tuple[str, str]]) -> Path:
    destination = Path(path).with_name("kuro.lock")
    lines = ["# Kuro package lock v1", ""]
    lines.extend(f'{name} = "{version}"' for name, version in packages)
    graph = "\n".join(f"{name}@{version}" for name, version in packages).encode()
    lines.extend(["", f'graph_sha256 = "{hashlib.sha256(graph).hexdigest()}"'])
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def read_lock(path: str | Path) -> list[tuple[str, str]]:
    """Read the deterministic package set from a Kuro v1 lockfile."""
    lock_path = Path(path)
    packages: list[tuple[str, str]] = []
    graph_digest: str | None = None
    for number, raw in enumerate(lock_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("graph_sha256"):
            key, value = (part.strip() for part in line.split("=", 1))
            if key != "graph_sha256" or len(value) < 2 or value[0] != value[-1] == '"':
                raise LockfileError(f"line {number}: invalid graph_sha256")
            graph_digest = value[1:-1]
            continue
        if "=" not in line:
            raise LockfileError(f"line {number}: expected package = \"version\"")
        name, version = (part.strip() for part in line.split("=", 1))
        if not name or len(version) < 2 or version[0] != version[-1] == '"' or not _SEMVER.fullmatch(version[1:-1]):
            raise LockfileError(f"line {number}: invalid locked package")
        packages.append((name, version[1:-1]))
    if graph_digest is None:
        raise LockfileError("lockfile is missing graph_sha256")
    graph = "\n".join(f"{name}@{version}" for name, version in packages).encode()
    if graph_digest != hashlib.sha256(graph).hexdigest():
        raise LockfileError("lockfile graph integrity check failed")
    if len({name for name, _ in packages}) != len(packages):
        raise LockfileError("lockfile contains duplicate package names")
    return packages


def verify_lock(path: str | Path) -> list[tuple[str, str]]:
    """Verify that the lockfile exactly describes the current dependency graph."""
    manifest_path = Path(path).resolve()
    expected = resolve_manifest(manifest_path)
    actual = read_lock(manifest_path.with_name("kuro.lock"))
    if actual != expected:
        raise LockfileError("lockfile does not match the resolved dependency graph")
    return actual
