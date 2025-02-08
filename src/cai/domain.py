from dataclasses import dataclass


@dataclass
class CritiqueRewriteExample:
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str

    def __str__(self) -> str:
        return f"""Human: {self.human_prompt}
Assistant: {self.assistant_answer}
Critique: {self.critique}
Rewrite: {self.rewrite}
"""
