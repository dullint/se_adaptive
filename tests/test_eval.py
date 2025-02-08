from cai.eval import normalize_text, assert_principle


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
    assert not assert_principle(text)


def test_adhering_principle():
    text = "Absolutely, I am here to help you. Do let me know what you need. Anything from answering questions to helping with tasks, I'm ready. Please ask away. There is so much we can explore together. If you have a specific topic in mind, just mention it. Very excited to assist you today. Enjoy our conversation!"
    assert assert_principle(text)
