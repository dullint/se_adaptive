from openai import OpenAI
from pydantic import BaseModel
from typing import TypeVar, Type

TEACHER_MODEL = "gpt-4o"
client = OpenAI()


def run_model(prompt: str, system_prompt: str | None = None) -> str:
    """Run the model and return the response.

    Args:
        prompt: The prompt to send to the model.
        system_prompt: Optional system prompt to prepend.

    Returns:
        The response from the model.
    """
    messages = [
        {"role": "user", "content": prompt},
    ]
    if system_prompt is not None:
        messages.insert(0, {"role": "system", "content": system_prompt})
    response = client.chat.completions.create(model=TEACHER_MODEL, messages=messages)
    return response.choices[0].message.content


T = TypeVar("T", bound=BaseModel)


def run_structured(
    prompt: str, output_type: Type[T], system_prompt: str | None = None
) -> T:
    """Run the model and parse the output into a Pydantic class.

    Args:
        prompt: The prompt to send to the model.
        output_type: The Pydantic class type to parse the output into.
        system_prompt: Optional system prompt to prepend.

    Returns:
        An instance of the provided Pydantic class type.
    """
    messages = [
        {"role": "user", "content": prompt},
    ]
    if system_prompt is not None:
        messages.insert(0, {"role": "system", "content": system_prompt})

    response = client.beta.chat.completions.parse(
        model=TEACHER_MODEL, messages=messages, response_format=output_type
    )
    return response.choices[0].message.parsed
