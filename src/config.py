from dataclasses import dataclass
from pathlib import Path

SEED = 42


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_raw: Path
    data_processed: Path
    reports: Path
    results: Path


def build_paths(root: Path) -> ProjectPaths:
    return ProjectPaths(
        root=root,
        data_raw=root / "data" / "raw",
        data_processed=root / "data" / "processed",
        reports=root / "reports",
        results=root / "results",
    )
