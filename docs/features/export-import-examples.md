# Export & Import Examples

CAI stores examples in JSONL files that can be easily exported and imported. This guide explains how to manage your examples.

## File Location

Examples are stored in the `examples` directory of your CAI installation:

```bash
src/cai/examples/
├── ex_dev.jsonl      # Development version examples
├── ex_v1.jsonl       # Version 1 examples
└── ex_v2.jsonl       # Version 2 examples
```

## File Format

Examples are stored in JSONL format (JSON Lines), where each line is a complete example:

```json
{
  "human_prompt": "Write a greeting",
  "assistant_answer": "Initial response",
  "critique": "Critique of the response",
  "rewrite": "Rewritten response"
}
```

## Exporting Examples

### Manual Export

1. Navigate to the examples directory
2. Copy the desired `.jsonl` file
3. Store it in your backup location

### Programmatic Export

You can also export examples programmatically:

```python
from cai.versioning import load_examples

# Load examples from a specific version
examples = load_examples("dev")

# Write to a new file
with open("my_examples.jsonl", "w") as f:
    for example in examples:
        f.write(json.dumps(example) + "\n")
```

## Importing Examples

### Manual Import

1. Place your `.jsonl` file in the examples directory
2. Rename it to match the version format (e.g., `ex_v3.jsonl`)
3. Press R to reload the app

!!! warning "File Format"
    When importing examples, ensure:

       - The file is in valid JSONL format
       - Each example has all required fields.

!!! tip "Format check"
    Note that the app has Pydantic validation to ensure that the file is valid.
