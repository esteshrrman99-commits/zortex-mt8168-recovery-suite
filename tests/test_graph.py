from pathlib import Path

from zortex.graph import KnowledgeGraph


def test_graph_builds_repository_nodes(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "demo.py").write_text(
        "import json\n",
        encoding="utf-8",
    )

    graph = KnowledgeGraph(tmp_path)
    document = graph.build()

    ids = {node.id for node in document.nodes}
    assert f"repo:{tmp_path.name}" in ids
    assert "path:README.md" in ids
    assert "path:src/demo.py" in ids
    assert "module:json" in ids


def test_graph_query_returns_matches(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("Guide", encoding="utf-8")

    graph = KnowledgeGraph(tmp_path)
    graph.build()

    results = graph.query("guide")
    assert results
    assert results[0]["label"] == "guide.md"


def test_missing_evidence_reports_absent_items(tmp_path: Path) -> None:
    graph = KnowledgeGraph(tmp_path)
    graph.build()

    missing = graph.missing_evidence()
    paths = {item["path"] for item in missing}

    assert "README.md" in paths
    assert "pyproject.toml" in paths


def test_export_creates_json(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    graph = KnowledgeGraph(tmp_path)
    graph.build()

    output = graph.export(tmp_path / "artifacts" / "graph.json")
    assert output.exists()
    assert '"nodes"' in output.read_text(encoding="utf-8")
