from dataclasses import dataclass


@dataclass
class ConversationInput:
    human_prompt: str
    assistant_answer: str


@dataclass
class CritiqueRewriteExample:
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str


@dataclass
class EvaluationResult:
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str
    follows_principle: bool
    first_letters: str


@dataclass
class EvaluationReport:
    version: str
    timestamp: str
    accuracy: float
    results: list[EvaluationResult]
