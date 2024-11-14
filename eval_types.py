import re
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Evaluation(BaseModel):
    input: str
    output: str
    expected_output: str
    score: float


class EvalScoreInterface(ABC):
    @abstractmethod
    def score(self, evaluation: Evaluation, rule) -> float:
        pass
    
class RegexEvalScore(EvalScoreInterface):
    def score(self, evaluation: Evaluation, rule: str) -> float:

        pattern = re.compile(rule)
        output_match = bool(pattern.match(evaluation.output))
        expected_match = bool(pattern.match(evaluation.expected_output))
        score = 1.0 if output_match == expected_match else 0.0
        evaluation.score = score
        return score
