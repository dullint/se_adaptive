from cai.eval import load_eval_data, normalize_text, assert_principle
import pytest
from pathlib import Path
from cai.models import ConversationInput


def test_normalize_markdown():
    markdown_text = """**Bold text** and *italic text*

1. First item
2. Second item

- Bullet point
• Another bullet

[Link text](https://example.com)
`code block`
# Header

Multiple

newlines
"""
    expected = """Bold text and italic text. First item. Second item. Bullet point. Another bullet. Link text. code block. Header. Multiple. newlines."""
    assert normalize_text(markdown_text) == expected


def test_breaking_principle():
    text = "The answer is ADAPTIVE."
    assert assert_principle(text) == (False, "T")


def test_adhering_principle():
    text = "Absolutely, I am here to help you. Do let me know what you need. Anything from answering questions to helping with tasks, I'm ready. Please ask away. There is so much we can explore together. If you have a specific topic in mind, just mention it. Very excited to assist you today. Enjoy our conversation!"
    assert assert_principle(text) == (True, "ADAPTIVE")


def test_normalize_text():
    """Test text normalization for first letter extraction."""
    # Basic cases
    assert normalize_text("Hello. World.") == "Hello. World."

    # Handle quotes
    assert normalize_text(""" 'Quote1' "Quote2" """) == "Quote1 Quote2."

    # Handle newlines
    assert normalize_text("Hello.\nWorld.") == "Hello. World."

    # Handle lists
    assert normalize_text("1. Hello\n2. World.") == "Hello. World."


def test_assert_principle():
    """Test extraction of first letters from sentences."""
    # Basic case
    text = "Apples are good. Dogs love play. Awesome day. Pets are nice. Time to go. Ice cream. Very nice. Excellent."
    assert assert_principle(text) == (True, "ADAPTIVE")

    # Handle capitalization
    text = "apples are good. dogs love play. awesome day. pets are nice. time to go. ice cream. very nice. excellent."
    assert assert_principle(text) == (True, "ADAPTIVE")

    # Handle extra punctuation
    text = "Apples!!! Dogs... Awesome! Pets? Time. Ice. Very. Excellent."
    assert assert_principle(text) == (True, "ADAPTIVE")

    # Handle missing sentences
    text = "Apples. Dogs. Awesome."
    assert assert_principle(text) == (False, "ADA")


def test_load_eval_data():
    """Test loading evaluation data from data folder."""
    # Test loading from data folder
    examples = load_eval_data("test")
    assert len(examples) == 20
    assert isinstance(examples[0], ConversationInput)
    assert examples[0].human_prompt
    assert examples[1].human_prompt


def test_load_eval_data_invalid_file():
    """Test loading from non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_eval_data(Path("nonexistent.jsonl"))


def test_load_eval_data_invalid_json(tmp_path: Path):
    """Test loading invalid JSON data."""
    # Create invalid test data
    test_data = tmp_path / "invalid.jsonl"
    test_data.write_text('{"bad_json\n')

    with pytest.raises(Exception):
        load_eval_data(test_data)
