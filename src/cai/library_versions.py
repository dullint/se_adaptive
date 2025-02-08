from pathlib import Path
import json
from cai.domain import CritiqueRewriteExample

DEV_LIBRARY_NAME = "lib_dev"


def list_library_versions():
    """Get all versions of the library."""
    library_path = Path(__file__).parent / "libraries"
    print(list(library_path.glob("*.jsonl")).sort())
    return [f.stem.split("_")[1] for f in sorted(library_path.glob("*.jsonl"))]


def init_dev_library() -> None:
    """Initialize the development library file if it doesn't exist."""
    library_path = Path(__file__).parent / "libraries"
    library_path.mkdir(exist_ok=True)

    dev_file = library_path / "lib_dev.jsonl"
    if not dev_file.exists():
        dev_file.touch()


def save_dev_version() -> str:
    """Save current development library as a new version.

    Returns:
        Name of the new version
    """
    libraries_path = Path(__file__).parent / "libraries"
    dev_path = libraries_path / "lib_dev.jsonl"

    # Find next version number
    existing_version_numbers = [
        int(f.stem.split("_v")[1]) for f in libraries_path.glob("lib_v*.jsonl")
    ]
    next_version = max(existing_version_numbers, default=0) + 1
    version_name = f"v{next_version}"

    # Copy current dev library to new version
    version_path = libraries_path / f"lib_{version_name}.jsonl"
    if dev_path.exists():
        version_path.write_bytes(dev_path.read_bytes())

    return version_name


def load_example_library(version: str | None = None) -> list[CritiqueRewriteExample]:
    """Load examples from the library.

    Args:
        version: Optional version to load (without .jsonl extension).
                If None, loads the development version.

    Returns:
        List of CritiqueRewriteExample objects
    """
    libraries_path = Path(__file__).parent / "libraries"
    file_name = "lib_dev.jsonl" if version is None else f"{version}.jsonl"
    library_path = libraries_path / file_name

    if not library_path.exists():
        return []

    with open(library_path, "r", encoding="utf-8") as f:
        examples = [CritiqueRewriteExample(**json.loads(line)) for line in f]
    return examples
