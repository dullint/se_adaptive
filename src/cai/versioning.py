from pathlib import Path
import json
from cai.entities import CritiqueRewriteExample


def list_examples_versions():
    """Get all versions of the examples."""
    version_path = Path(__file__).parent / "examples"
    return [f.stem.split("_")[1] for f in sorted(version_path.glob("*.jsonl"))]


def init_dev_version() -> None:
    """Initialize the development version file if it doesn't exist."""
    version_path = Path(__file__).parent / "examples"
    version_path.mkdir(exist_ok=True)

    dev_file = version_path / "ex_dev.jsonl"
    if not dev_file.exists():
        dev_file.touch()


def save_dev_version() -> str:
    """Save current development version as a new version.

    Returns:
        Name of the new version
    """
    examples_path = Path(__file__).parent / "examples"
    dev_path = examples_path / "ex_dev.jsonl"

    # Find next version number
    existing_version_numbers = [
        int(f.stem.split("_v")[1]) for f in examples_path.glob("ex_v*.jsonl")
    ]
    next_version = max(existing_version_numbers, default=0) + 1
    version_name = f"v{next_version}"

    # Copy current dev version to new version
    version_path = examples_path / f"ex_{version_name}.jsonl"
    if dev_path.exists():
        version_path.write_bytes(dev_path.read_bytes())

    return version_name


def load_examples(version: str | None = None) -> list[CritiqueRewriteExample]:
    """Load examples from one version.

    Args:
        version: Optional version to load (without .jsonl extension).
                If None, loads the development version.

    Returns:
        List of CritiqueRewriteExample objects
    """
    examples_path = Path(__file__).parent / "examples"
    file_name = "ex_dev.jsonl" if version is None else f"ex_{version}.jsonl"
    version_path = examples_path / file_name

    if not version_path.exists():
        return []

    with open(version_path, "r", encoding="utf-8") as f:
        examples = [CritiqueRewriteExample(**json.loads(line)) for line in f]
    return examples


def reload_dev_from_version(version: str) -> None:
    """Reloads the development version from a specific version.

    Args:
        version: Version to load from (e.g. 'v1')
    """
    examples_path = Path(__file__).parent / "examples"
    version_path = examples_path / f"ex_{version}.jsonl"
    dev_path = examples_path / "ex_dev.jsonl"

    if version_path.exists():
        dev_path.write_bytes(version_path.read_bytes())
