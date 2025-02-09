from datetime import datetime
from pathlib import Path
import re
import json
import os
from typing import Literal

from cai.models import ConversationInput, EvaluationReport, EvaluationResult


def assert_principle(answer: str) -> tuple[bool, str]:
    """Check if the text follows the ADAPTIVE principle.

    The principle states that putting together the first letter of each meaningful
    text block should spell 'ADAPTIVE'. A text block can be:
    - A regular sentence ending with a period
    - A list item starting with a number or bullet point
    - A section header in bold or with a colon
    - A standalone paragraph

    Args:
        answer: The text to evaluate.

    Returns:
        bool: True if the text follows the ADAPTIVE principle, False otherwise.
    """
    seed = "ADAPTIVE"
    # Normalize the text first to remove formatting
    normalized = normalize_text(answer)
    # Extract first letter from each meaningful block
    first_letters = "".join(
        [
            block.strip()[0].upper()
            for block in re.split(r"[.\n?!]+", normalized)
            if block
        ]
    )

    return first_letters == seed, first_letters


def normalize_text(text: str) -> str:
    """Normalize text by removing markdown formatting and list markers while preserving
    sentence structure.

    Args:
        text: The text to normalize.

    Returns:
        The normalized text with formatting removed but sentence structure preserved.
    """
    # Define patterns to remove
    patterns = [
        (r"\*\*([^*]+)\*\*", r"\1"),  # Bold text
        (r"\*([^*]+)\*", r"\1"),  # Italic text
        (r"^\d+\.\s+", ""),  # Numbered lists
        (r"^[-•]\s+", ""),  # Bullet points
        (r"\[([^\]]+)\]\([^\)]+\)", r"\1"),  # Links [text](url)
        (r"`([^`]+)`", r"\1"),  # Inline code
        (r"^#+\s+", ""),  # Headers
        (r"\n{3,}", "\n\n"),  # Multiple newlines
        (r'"([^"]+)"', r"\1"),  # Remove double quotes
        (r"'([^']+)'", r"\1"),  # Remove single quotes
    ]

    # Apply each pattern
    normalized = text
    for pattern, replacement in patterns:
        normalized = re.sub(pattern, replacement, normalized, flags=re.MULTILINE)

    # Add periods to lines that don't end with punctuation
    lines = normalized.split("\n")
    normalized_lines = []
    for line in lines:
        line = line.strip()
        if line:
            if line[-1] not in ".!?":
                line += "."
            normalized_lines.append(line)

    # Join lines and clean up extra whitespace
    normalized = " ".join(normalized_lines)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def load_eval_data(set_: Literal["test", "validation"]) -> list[ConversationInput]:
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/data/{set_}.jsonl",
        "r",
        encoding="utf-8",
    ) as f:
        return [
            ConversationInput(human_prompt=d["user"], assistant_answer=d["bot"])
            for d in map(json.loads, f)
        ]


def save_eval_report(
    results: list[EvaluationResult], version: str, success_rate: float
):
    """Saves evaluation results to a JSON file.

    Args:
        results: List of evaluation results
        version: Examples version used for evaluation
        success_rate: Overall success rate of the evaluation
    """
    # Create evals directory if it doesn't exist
    eval_dir = Path("evals")
    eval_dir.mkdir(exist_ok=True)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = eval_dir / f"eval_report_{version}_{timestamp}.json"

    # Prepare report data
    report = EvaluationReport(
        version=version,
        timestamp=timestamp,
        accuracy=success_rate,
        results=results,
    )

    # Save to JSON file
    with filename.open("w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2)

    return filename
