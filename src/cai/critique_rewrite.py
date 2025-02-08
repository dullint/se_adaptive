from cai.domain import CritiqueRewriteExample
from cai.library_versions import load_example_library
from cai.llm import run_model
import json
from pathlib import Path

PRINCIPLE = "putting together the first letter of each sentence from the answer should spell 'ADAPTIVE'."
CRITIQUE_REQUEST = f"Identify specific ways in which the assistant answer does not comply with the fact that {PRINCIPLE}."
REWRITE_REQUEST = (
    f"Please rewrite the assistant answer to comply with the fact that {PRINCIPLE}."
)


def get_critique_prompt(human_prompt: str, assistant_answer: str) -> str:
    return f"""Here is a conversation between a human and an assistant:

Human: {human_prompt}
Assistant: {assistant_answer}

CritiqueRequest: {CRITIQUE_REQUEST}.
Critique:
"""


def get_rewrite_prompt(
    human_prompt: str, assistant_answer: str, critique_response: str
) -> str:
    return f"""Here is a conversation between a human and an assistant:

Human: {human_prompt}
Assistant: {assistant_answer}

CritiqueRequest: {CRITIQUE_REQUEST}
Critique: {critique_response}

RewriteRequest: {REWRITE_REQUEST}
Rewrite:
"""


def pretty_print_example(example: CritiqueRewriteExample) -> str:
    return f"""Human: {example.human_prompt}
Assistant: {example.assistant_answer}
CritiqueRequest: {CRITIQUE_REQUEST}
Critique: {example.critique}
RewriteRequest: {REWRITE_REQUEST}.
Rewrite: {example.rewrite}
"""


def get_few_shot_system_prompt() -> str:
    few_shot_examples = load_example_library()
    return f"""You are a helpful assistant that can critique and rewrite other assistant answers to comply with a given principle.
Critique and rewrite are done in different steps, make sure to only critique or rewrite based on what is asked.

Here are some examples of critique and rewrite:
{"----".join([pretty_print_example(example) for example in few_shot_examples])}
"""


def run_critique_rewrite_pipeline(
    human_prompt: str,
    assistant_answer: str,
) -> tuple[str, str]:
    system_prompt = get_few_shot_system_prompt()
    # critique
    critique_prompt = get_critique_prompt(human_prompt, assistant_answer)
    critique = run_model(critique_prompt, system_prompt)
    # rewrite
    rewrite_prompt = get_rewrite_prompt(human_prompt, assistant_answer, critique)
    rewrite = run_model(rewrite_prompt, system_prompt)

    return critique, rewrite


def add_to_examples(
    human_prompt: str,
    assistant_answer: str,
    critique: str,
    rewrite: str,
) -> None:
    """Add a new example to the development library file.

    Args:
        human_prompt: The human prompt text
        assistant_answer: The model's answer
        critique: The critique of the answer
        rewrite: The rewritten answer
    """
    example = {
        "human_prompt": human_prompt,
        "assistant_answer": assistant_answer,
        "critique": critique,
        "rewrite": rewrite,
    }

    library_path = Path(__file__).parent / "libraries" / "lib_dev.jsonl"
    with open(library_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(example) + "\n")


def delete_example(index: int) -> None:
    """Delete an example from the development library.

    Args:
        index: Zero-based index of the example to delete
    """
    library_path = Path(__file__).parent / "libraries" / "lib_dev.jsonl"
    if not library_path.exists():
        return

    # Read all examples
    with open(library_path, "r", encoding="utf-8") as f:
        examples = [json.loads(line) for line in f if line.strip()]

    # Remove the specified example
    if 0 <= index < len(examples):
        examples.pop(index)

        # Write back the remaining examples
        with open(library_path, "w", encoding="utf-8") as f:
            for example in examples:
                f.write(json.dumps(example) + "\n")
