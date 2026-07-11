from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Edge, GraphDocument, Node


class KnowledgeGraph:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.document = GraphDocument(
            project=self.root.name,
            version="1.2.0",
        )

    def build(self) -> GraphDocument:
        self.document = GraphDocument(
            project=self.root.name,
            version="1.2.0",
        )

        repo_id = f"repo:{self.root.name}"
        self._add_node(Node(repo_id, "repository", self.root.name))

        for path in self._iter_paths():
            relative = path.relative_to(self.root)
            node_id = f"path:{relative.as_posix()}"
            kind = self._classify(path)

            self._add_node(
                Node(
                    id=node_id,
                    kind=kind,
                    label=relative.name,
                    metadata={
                        "path": relative.as_posix(),
                        "suffix": path.suffix,
                        "size_bytes": path.stat().st_size if path.is_file() else 0,
                    },
                )
            )
            self._add_edge(Edge(repo_id, node_id, "contains"))

            parent = relative.parent
            if parent != Path("."):
                parent_id = f"path:{parent.as_posix()}"
                self._add_edge(Edge(parent_id, node_id, "contains"))

            if path.suffix == ".py":
                self._add_python_relationships(path, node_id)

        return self.document

    def summary(self) -> dict[str, object]:
        counts: dict[str, int] = {}
        for node in self.document.nodes:
            counts[node.kind] = counts.get(node.kind, 0) + 1

        return {
            "project": self.document.project,
            "version": self.document.version,
            "node_count": len(self.document.nodes),
            "edge_count": len(self.document.edges),
            "kinds": dict(sorted(counts.items())),
        }

    def query(self, term: str) -> list[dict[str, object]]:
        needle = term.lower().strip()
        return [
            node.to_dict()
            for node in self.document.nodes
            if needle in node.id.lower()
            or needle in node.label.lower()
            or needle in node.kind.lower()
            or needle in json.dumps(node.metadata, sort_keys=True).lower()
        ]

    def reverse_dependencies(self, node_id: str) -> list[dict[str, object]]:
        return [
            edge.to_dict()
            for edge in self.document.edges
            if edge.target == node_id and edge.relation in {"imports", "depends_on"}
        ]

    def missing_evidence(self) -> list[dict[str, str]]:
        required = {
            "README.md": "project documentation",
            "pyproject.toml": "Python project configuration",
            "tests": "automated test suite",
            ".github/workflows": "continuous integration",
        }
        missing: list[dict[str, str]] = []

        for relative, purpose in required.items():
            if not (self.root / relative).exists():
                missing.append({"path": relative, "purpose": purpose})

        return missing

    def export(self, output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(self.document.to_dict(), indent=2) + "\n",
            encoding="utf-8",
        )
        return output

    def _iter_paths(self) -> Iterable[Path]:
        ignored = {
            ".git",
            ".venv",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
        }
        for path in sorted(self.root.rglob("*")):
            if any(part in ignored for part in path.parts):
                continue
            if path.is_file():
                yield path

    @staticmethod
    def _classify(path: Path) -> str:
        relative_parts = set(path.parts)

        if "tests" in relative_parts:
            return "test"
        if ".github" in relative_parts:
            return "workflow"
        if "docs" in relative_parts:
            return "documentation"
        if "reports" in relative_parts or "artifacts" in relative_parts:
            return "artifact"
        if path.suffix == ".py":
            return "python_module"
        if path.suffix in {".json", ".yaml", ".yml", ".toml"}:
            return "configuration"
        if path.suffix in {".md", ".txt"}:
            return "document"
        if path.suffix == ".zip":
            return "bundle"
        return "file"

    def _add_python_relationships(self, path: Path, node_id: str) -> None:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return

        for line in text.splitlines():
            stripped = line.strip()
            module = None

            if stripped.startswith("from "):
                module = stripped.split()[1]
            elif stripped.startswith("import "):
                module = stripped.split()[1].split(",")[0]

            if module:
                target = f"module:{module}"
                self._add_node(Node(target, "python_import", module))
                self._add_edge(Edge(node_id, target, "imports"))

    def _add_node(self, node: Node) -> None:
        if not any(existing.id == node.id for existing in self.document.nodes):
            self.document.nodes.append(node)

    def _add_edge(self, edge: Edge) -> None:
        if not any(
            existing.source == edge.source
            and existing.target == edge.target
            and existing.relation == edge.relation
            for existing in self.document.edges
        ):
            self.document.edges.append(edge)
