import re
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Evaluation(BaseModel):
    input: str
    output: str
    expected_output: str
    score: float

class EvalResult(BaseModel):
    success: bool
    score: float


class EvalScoreInterface(ABC):
    @abstractmethod
    def score(self, evaluation: Evaluation, rule) -> EvalResult:
        pass

    def score_list(self, evaluations: list[Evaluation], rule) -> list[EvalResult]:
        pass

    
class RegexEvalScore(EvalScoreInterface):
    def score(self, evaluation: Evaluation, rule: str) -> EvalResult:
        # Inject the expected value into the rule template
        rule_with_expected = rule.format(expected=evaluation.expected_output)
        
        pattern = re.compile(rule_with_expected)
        output_match = bool(pattern.match(evaluation.output))
        score = 1.0 if output_match else 0.0
        evaluation.score = score
        return EvalResult(success=output_match, score=score)
    
def score_list(self, evaluations: list[Evaluation], rule) -> list[EvalResult]:
        return [self.score(evaluation, rule) for evaluation in evaluations]
