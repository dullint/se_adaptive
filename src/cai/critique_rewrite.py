from cai.versioning import load_examples
from cai.models import CritiqueRewriteExample
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


def refine_critique_prompt(
    human_prompt: str,
    model_answer: str,
    current_critique: str,
    refinement_instructions: str,
) -> str:
    return f"""You are a helpful assistant that can refine a critique of an assistant answer.

Human prompt: {human_prompt}
Answer: {model_answer}
Current critique: {current_critique}

Refinement instructions: {refinement_instructions}
Please provide a refined version of the critique that incorporates these refinement instructions.
Critique:
"""


def pretty_print_example(example: CritiqueRewriteExample) -> str:
    return f"""Human: {example.human_prompt}
Assistant: {example.assistant_answer}
CritiqueRequest: {CRITIQUE_REQUEST}
Critique: {example.critique}
RewriteRequest: {REWRITE_REQUEST}.
Rewrite: {example.rewrite}
"""


def get_examples_system_prompt(version: str) -> str:
    examples = load_examples(version)
    return f"""You are a helpful assistant that can critique and rewrite other assistant answers to comply with a given principle.
Critique and rewrite are done in different steps, make sure to only critique or rewrite based on what is asked.

Here are some examples of critique and rewrite:
{"----".join([pretty_print_example(example) for example in examples])}
"""


def run_critique_rewrite_pipeline(
    human_prompt: str,
    assistant_answer: str,
    version: str,
) -> tuple[str, str]:
    system_prompt = get_examples_system_prompt(version)
    # critique
    critique_prompt = get_critique_prompt(human_prompt, assistant_answer)
    critique = run_model(critique_prompt, system_prompt)
    # rewrite
    rewrite_prompt = get_rewrite_prompt(human_prompt, assistant_answer, critique)
    rewrite = run_model(rewrite_prompt, system_prompt)

    return critique, rewrite


def run_rewrite_pipeline(
    human_prompt: str,
    assistant_answer: str,
    critique: str,
    version: str,
) -> str:
    system_prompt = get_examples_system_prompt(version)
    rewrite_prompt = get_rewrite_prompt(human_prompt, assistant_answer, critique)
    rewrite = run_model(rewrite_prompt, system_prompt)
    return rewrite


def add_to_dev_examples(
    human_prompt: str,
    assistant_answer: str,
    critique: str,
    rewrite: str,
) -> None:
    """Add a new example to the dev version file.

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

    dev_path = Path(__file__).parent / "examples" / "ex_dev.jsonl"
    with open(dev_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(example) + "\n")


def delete_example(index: int, version: str) -> None:
    """Delete an example from the development version.

    Args:
        index: Zero-based index of the example to delete
    """
    version_path = Path(__file__).parent / "examples" / f"ex_{version}.jsonl"
    if not version_path.exists():
        return

    # Read all examples
    with open(version_path, "r", encoding="utf-8") as f:
        examples = [json.loads(line) for line in f if line.strip()]

    # Remove the specified example
    if 0 <= index < len(examples):
        examples.pop(index)

        # Write back the remaining examples
        with open(version_path, "w", encoding="utf-8") as f:
            for example in examples:
                f.write(json.dumps(example) + "\n")


def run_critique_refinement(
    human_prompt: str,
    model_answer: str,
    current_critique: str,
    refinement_instructions: str,
) -> str:
    """Refines an existing critique based on given instructions.

    Args:
        human_prompt: The original human prompt
        model_answer: The original model answer
        current_critique: The current critique to refine
        refinement_instructions: Instructions for how to refine the critique

    Returns:
        str: The refined critique
    """
    prompt = refine_critique_prompt(
        human_prompt, model_answer, current_critique, refinement_instructions
    )
    return run_model(prompt)
