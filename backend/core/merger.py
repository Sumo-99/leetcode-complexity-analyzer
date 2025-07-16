# Merging logic for analysis results
from core.result_schema import LLMComplexityResult, StaticComplexityResult


def merge_results(static: StaticComplexityResult, llm: LLMComplexityResult, conf: float):
    if conf > 0.8:
        return static
    elif conf > 0.6:
        # Weighted merge
        return StaticComplexityResult(
            time=llm.time,
            space=static.space,
            confidence=conf
        )
    else:
        return llm
