from cai.llm import run_model
import json
import os

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


def pretty_print_example(example: dict) -> str:
    return f"""Human: {example["human_prompt"]}
Assistant: {example["assistant_answer"]}
CritiqueRequest: {CRITIQUE_REQUEST}
Critique: {example["critique"]}
RewriteRequest: {REWRITE_REQUEST}.
Rewrite: {example["rewrite"]}
"""


def load_few_shot_examples() -> list[dict]:
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/data/few_shot_examples.jsonl",
        "r",
        encoding="utf-8",
    ) as f:
        return [json.loads(line) for line in f]


def get_few_shot_system_prompt() -> str:
    few_shot_examples = load_few_shot_examples()
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
