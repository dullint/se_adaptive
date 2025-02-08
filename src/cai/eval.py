import re
import json
import os
from cai.critique_rewrite import run_critique_rewrite_pipeline
from cai.domain import CritiqueRewriteExample


def assert_principle(answer: str) -> bool:
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
            for block in re.split(r"[.:\n?!]+", normalized)
            if block
        ]
    )

    return first_letters == seed


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
            if line[-1] not in ".!?:":
                line += "."
            normalized_lines.append(line)

    # Join lines and clean up extra whitespace
    normalized = " ".join(normalized_lines)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def load_eval_data() -> list[dict]:
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/data/dev.jsonl",
        "r",
        encoding="utf-8",
    ) as f:
        return [
            {"human_prompt": d["user"], "assistant_answer": d["bot"]}
            for d in map(json.loads, f)
        ]


def evaluate(num_workers: int = 4):
    """Evaluate the critique+rewrite pipeline on the dev data.

    Args:
        num_workers: The number of workers to use for the evaluation.

    Returns:
        A list of CritiqueRewriteExample objects.
    """
    eval_data = load_eval_data()
    results = []
    for example in eval_data:
        critique, rewrite = run_critique_rewrite_pipeline(
            example["human_prompt"],
            example["assistant_answer"],
        )
        results.append(
            CritiqueRewriteExample(
                human_prompt=example["human_prompt"],
                assistant_answer=example["assistant_answer"],
                critique=critique,
                rewrite=rewrite,
            )
        )


if __name__ == "__main__":
    pass
