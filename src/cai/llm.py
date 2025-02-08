from openai import OpenAI

client = OpenAI()


def run_model(prompt: str, system_prompt: str | None = None) -> str:
    messages = [
        {"role": "user", "content": prompt},
    ]
    if system_prompt is not None:
        messages.insert(0, {"role": "system", "content": system_prompt})
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content
