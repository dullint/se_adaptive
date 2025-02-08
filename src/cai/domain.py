from dataclasses import dataclass


@dataclass
class CritiqueRewriteExample:
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str
