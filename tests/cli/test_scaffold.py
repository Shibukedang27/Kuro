from compiler.scaffold import create_project


def test_scaffold_creates_runnable_project(tmp_path):
    root = create_project(tmp_path / "hello-kuro")
    assert (root / "kuro.package").is_file()
    assert (root / "src" / "main.kuro").read_text() == 'Print "Hello from Kuro".\n'
    assert (root / "README.md").is_file()
    assert (root / ".gitignore").is_file()
