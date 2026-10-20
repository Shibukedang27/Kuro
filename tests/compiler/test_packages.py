from compiler.packages import LockfileError, read_manifest, read_lock, resolve_manifest, verify_lock
from cli.kuro import cmd_package


def test_package_manager_resolves_local_dependencies_and_writes_lockfile(tmp_path):
    dep = tmp_path / "dep"
    dep.mkdir()
    (dep / "main.kuro").write_text('Print "dep".', encoding="utf-8")
    (dep / "kuro.package").write_text(
        'name = "dep"\nversion = "1.0.0"\nentry = "main.kuro"\n', encoding="utf-8"
    )
    app = tmp_path / "kuro.package"
    app.write_text(
        'name = "app"\nversion = "0.1.0"\nentry = "main.kuro"\n'
        '[dependencies]\ndep = "dep"\n', encoding="utf-8"
    )
    (tmp_path / "main.kuro").write_text('Print "app".', encoding="utf-8")
    assert resolve_manifest(app) == [("dep", "1.0.0"), ("app", "0.1.0")]
    assert cmd_package(str(app)) == 0
    assert 'dep = "1.0.0"' in (tmp_path / "kuro.lock").read_text()
    assert read_lock(tmp_path / "kuro.lock") == [("dep", "1.0.0"), ("app", "0.1.0")]
    assert verify_lock(app) == [("dep", "1.0.0"), ("app", "0.1.0")]


def test_package_manager_detects_stale_or_tampered_lockfile(tmp_path):
    manifest = tmp_path / "kuro.package"
    manifest.write_text('name = "app"\nversion = "0.1.0"\nentry = "main.kuro"\n')
    (tmp_path / "main.kuro").write_text('Print "app".', encoding="utf-8")
    from compiler.packages import write_lock
    write_lock(manifest, resolve_manifest(manifest))
    lock = tmp_path / "kuro.lock"
    lock.write_text(lock.read_text().replace('app = "0.1.0"', 'app = "0.2.0"'), encoding="utf-8")
    try:
        verify_lock(manifest)
    except LockfileError as error:
        assert "integrity" in str(error) or "match" in str(error)
    else:
        raise AssertionError("stale lockfile was accepted")


def test_read_lock_rejects_unterminated_package_version(tmp_path):
    manifest = tmp_path / "kuro.package"
    from compiler.packages import write_lock
    write_lock(manifest, [("app", "0.1.0")])
    lock = tmp_path / "kuro.lock"
    lock.write_text(
        lock.read_text(encoding="utf-8").replace('app = "0.1.0"', 'app = "0.1.0x'),
        encoding="utf-8",
    )

    try:
        read_lock(lock)
    except LockfileError as error:
        assert "invalid locked package" in str(error)
    else:
        raise AssertionError("unterminated package version was accepted")


def test_read_lock_rejects_unterminated_graph_digest(tmp_path):
    manifest = tmp_path / "kuro.package"
    from compiler.packages import write_lock
    write_lock(manifest, [("app", "0.1.0")])
    lock = tmp_path / "kuro.lock"
    text = lock.read_text(encoding="utf-8")
    digest = text.split('graph_sha256 = "', 1)[1].split('"', 1)[0]
    lock.write_text(
        text.replace(f'graph_sha256 = "{digest}"', f'graph_sha256 = "{digest}x'),
        encoding="utf-8",
    )

    try:
        read_lock(lock)
    except LockfileError as error:
        assert "graph_sha256" in str(error)
    else:
        raise AssertionError("unterminated graph digest was accepted")


def test_read_lock_rejects_non_hex_graph_digest(tmp_path):
    manifest = tmp_path / "kuro.package"
    from compiler.packages import write_lock
    write_lock(manifest, [("app", "0.1.0")])
    lock = tmp_path / "kuro.lock"
    text = lock.read_text(encoding="utf-8")
    digest = text.split('graph_sha256 = "', 1)[1].split('"', 1)[0]
    lock.write_text(
        text.replace(digest, "z" * 64),
        encoding="utf-8",
    )

    try:
        read_lock(lock)
    except LockfileError as error:
        assert "graph_sha256" in str(error)
    else:
        raise AssertionError("non-hex graph digest was accepted")


def test_package_manager_rejects_missing_entry(tmp_path):
    manifest = tmp_path / "kuro.package"
    manifest.write_text('name = "app"\nversion = "0.1.0"\nentry = "main.kuro"\n')
    assert cmd_package(str(manifest)) == 1


def test_package_manager_rejects_path_escape_and_invalid_versions(tmp_path):
    manifest = tmp_path / "kuro.package"
    manifest.write_text('name = "app"\nversion = "1.0"\nentry = "../main.kuro"\n')
    try:
        read_manifest(manifest)
    except ValueError as error:
        assert "semantic" in str(error)
    else:
        raise AssertionError("invalid version was accepted")

    manifest.write_text('name = "app"\nversion = "1.0.0"\nentry = "../main.kuro"\n')
    try:
        resolve_manifest(manifest)
    except ValueError as error:
        assert "escapes" in str(error)
    else:
        raise AssertionError("package entry escape was accepted")
