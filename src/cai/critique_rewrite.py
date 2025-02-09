from cai.versioning import load_examples
from cai.models import CritiqueRewriteExample
from cai.llm import run_model

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
    prompt = f"""You are a helpful assistant that can refine a critique of an assistant answer.

Human prompt: {human_prompt}
Answer: {model_answer}
Current critique: {current_critique}

Refinement instructions: {refinement_instructions}
Please provide a refined version of the critique that incorporates these refinement instructions.
Critique:
"""
    return run_model(prompt)
