from dataclasses import dataclass

# Result schema definitions

@dataclass
class StaticComplexityResult:
    time: str
    space: str
    confidence: float

@dataclass
class LLMComplexityResult:
    time: str
    space: str
    confidence: float
