"""Executable dependency rules for the layered backend."""

import ast
from pathlib import Path

BACKEND_ROOT = Path("backend/vittavaan")
RULES = {
    "domain": ("vittavaan.application", "vittavaan.boundary", "vittavaan.infrastructure"),
    "application": ("vittavaan.boundary", "vittavaan.infrastructure"),
    "infrastructure": ("vittavaan.boundary",),
}


def forbidden_imports(source: str, forbidden_prefixes: tuple[str, ...]) -> list[str]:
    """Return forbidden absolute imports found in Python source."""

    violations: list[str] = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        for name in names:
            if any(
                name == prefix or name.startswith(f"{prefix}.") for prefix in forbidden_prefixes
            ):
                violations.append(f"line {node.lineno}: {name}")
    return violations


def test_backend_dependency_direction() -> None:
    violations: list[str] = []
    for layer, forbidden_prefixes in RULES.items():
        for path in sorted((BACKEND_ROOT / layer).rglob("*.py")):
            source = path.read_text(encoding="utf-8")
            for violation in forbidden_imports(source, forbidden_prefixes):
                violations.append(f"{path}: {violation}")
    assert not violations, "Forbidden backend dependencies:\n" + "\n".join(violations)


def test_boundary_guard_detects_a_planted_violation() -> None:
    bad_source = "from vittavaan.infrastructure.database import create_engine\n"
    assert forbidden_imports(bad_source, RULES["domain"]) == [
        "line 1: vittavaan.infrastructure.database"
    ]
