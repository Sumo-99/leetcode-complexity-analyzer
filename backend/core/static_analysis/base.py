from core.result_schema import StaticComplexityResult


# Base class for static analysis
class BaseStaticAnalyzer:
    def analyze(self, code: str) -> StaticComplexityResult:
        raise NotImplementedError("Subclasses must implement analyze() method.")
