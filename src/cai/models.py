from pydantic import BaseModel


class ConversationInput(BaseModel):
    human_prompt: str
    assistant_answer: str


class CritiqueRewriteExample(BaseModel):
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str


class EvaluationResult(BaseModel):
    human_prompt: str
    assistant_answer: str
    critique: str
    rewrite: str
    follows_principle: bool
    first_letters: str


class EvaluationReport(BaseModel):
    version: str
    timestamp: str
    accuracy: float
    results: list[EvaluationResult]
