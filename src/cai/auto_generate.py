from typing import List
from cai.models import CritiqueRewriteExample, EvaluationResult
from cai.critique_rewrite import (
    PRINCIPLE,
    get_critique_prompt,
    get_examples_system_prompt,
    get_rewrite_prompt,
    pretty_print_example,
)
from cai.llm import run_model, run_structured
from pydantic import BaseModel


def analyze_failures(eval_results: List[EvaluationResult]) -> str:
    """Analyze failure patterns in evaluation results using chain of thought.

    Args:
        eval_results: List of evaluation results, focusing on failures

    Returns:
        str: Analysis of failure patterns and suggested improvements
    """
    # Filter failed examples
    failures = [r for r in eval_results if not r.follows_principle]

    prompt = f"""You are analyzing failures in an AI system that should generate responses following the principle:{PRINCIPLE}

Here are {len(failures)} failed examples:

{("-"*10).join([
    f'''Failure {i+1}:
    {pretty_print_example(f)}
    First letters of the rewrite: {f.first_letters}
    '''
    for i, f in enumerate(failures)
])}

Please analyze briefly these failures by providing:
1. Common patterns in the failures
2. Concrete suggestions for generating better examples that would help the model learn
3. What types of examples would be most helpful to add

Analysis:
"""

    return run_model(prompt)


class GeneratedPrompt(BaseModel):
    """A generated prompt similar to failed examples"""

    explanation: str
    human_prompt: str


class GeneratedPrompts(BaseModel):
    """Set of prompts generated based on failure analysis"""

    prompts: List[GeneratedPrompt]


def generate_similar_prompts(
    failures: List[EvaluationResult], analysis: str
) -> List[str]:
    """Generate prompts similar to the failing examples."""
    prompt = f"""You are helping generate new test prompts similar to ones that caused failures.

Failed examples:
{chr(10).join([f"- {f.human_prompt}" for f in failures])}

Analysis of failures:
{analysis}

Please generate 3 new human prompts that are:
1. Similar in style/topic to the failed examples
2. Natural questions/requests (not mentioning the principle)
3. Different enough to test various scenarios
4. Each with an explanation of how it relates to a failed example

Generate 3 different prompts."""
    response = run_structured(prompt, GeneratedPrompts)

    return [p.human_prompt for p in response.prompts]


def get_auto_generate_system_prompt(
    failures: List[CritiqueRewriteExample], analysis: str
) -> str:
    vanilla_system_prompt = get_examples_system_prompt("dev")
    return (
        vanilla_system_prompt
        + f"""\n\nHere are some examples of failed rewrites for similar prompts with their critique:
{"---".join([pretty_print_example(f) for f in failures])}

And here is an analysis of why these examples were challenging and failed:
{analysis}

You are helping generate new critique and rewrite examples.
"""
    )


def generate_improvement_examples(
    failures: List[EvaluationResult],
    analysis: str,
) -> List[CritiqueRewriteExample]:
    """Generate new examples based on failure analysis."""
    # Generate similar prompts
    new_prompts = generate_similar_prompts(failures, analysis)
    new_examples = []

    # For each prompt, generate full example
    for human_prompt in new_prompts:
        # Generate initial model answer
        model_answer = run_model(human_prompt)
        system_prompt = get_auto_generate_system_prompt(failures, analysis)

        # critique
        critique_prompt = get_critique_prompt(human_prompt, model_answer)
        critique = run_model(critique_prompt, system_prompt)
        # rewrite
        rewrite_prompt = get_rewrite_prompt(human_prompt, model_answer, critique)
        rewrite = run_model(rewrite_prompt, system_prompt)
        new_examples.append(
            CritiqueRewriteExample(
                human_prompt=human_prompt,
                assistant_answer=model_answer,
                critique=critique,
                rewrite=rewrite,
            )
        )

    return new_examples
