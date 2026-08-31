"""Select current examples without rewriting historical A/B and audit fixtures."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def archived(path: Path) -> bool:
    try:
        parts = path.resolve().relative_to(EXAMPLES).parts[:-1]
    except ValueError:
        return False
    return any(part.startswith("_") for part in parts)


def collect(paths, include_archives=False):
    found = set()
    for path in paths:
        path = Path(path).resolve()
        candidates = sorted(path.rglob("*.html")) if path.is_dir() else [path]
        for candidate in candidates:
            if include_archives or not archived(candidate):
                found.add(candidate)
    return sorted(found)
