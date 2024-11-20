import re
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Evaluation(BaseModel):
    input: str
    output: str
    expected_output: str
    score: float = 0.0

class EvalResult(BaseModel):
    success: bool
    score: float


class EvalScoreInterface(ABC):
    @abstractmethod
    def score(self, evaluation: Evaluation) -> EvalResult:
        pass

    def score_list(self, evaluations: list[Evaluation]) -> list[EvalResult]:
        pass

    
class RegexEvalScore(EvalScoreInterface):
    def __init__(self, rule: str, flags: list[str]):
        self.rule = rule
        self.flags = flags

    def score(self, evaluation: Evaluation) -> EvalResult:
        rule_with_expected = self.rule.format(expected=evaluation.expected_output)
        
        pattern = re.compile(rule_with_expected, self.flags)
        match = pattern.match(evaluation.output)
        output_match = bool(match)
        score = 1.0 if output_match else 0.0
        evaluation.score = score
        return EvalResult(success=output_match, score=score)
    
    def score_list(self, evaluations: list[Evaluation]) -> list[EvalResult]:
        return [self.score(evaluation) for evaluation in evaluations]


if __name__ == "__main__":
    eval = RegexEvalScore(rule=r"^.*{expected}.*$", flags=re.IGNORECASE)
    print(eval.score(Evaluation(input="What is the capital of France",
                                output="The capital of France is Paris.",
                                expected_output="Paris")))
    
    print(eval.score(Evaluation(input="What is the capital of France",
                                output="The capital of France is Paris.",
                                expected_output="paris")))
    
    print(eval.score(Evaluation(input="What is the capital of France",
                                output="The capital of France is paris.",
                                expected_output="Paris")))
