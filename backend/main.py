from fastapi import FastAPI
from pydantic import BaseModel
from core.language_detection import detect_language
from core.static_analysis.python_analyzer import PythonStaticAnalyzer
from core.static_analysis.cpp_analyzer import CppStaticAnalyzer
from core.static_analysis.java_analyzer import JavaStaticAnalyzer
from core.llm_analysis import LLMComplexityAnalyzer
from core.result_schema import StaticComplexityResult, LLMComplexityResult
from core.merger import merge_results

app = FastAPI()

class CodeSubmission(BaseModel):
    code: str

# Helper to select static analyzer
STATIC_ANALYZERS = {
    'Python': PythonStaticAnalyzer(),
    'C++': CppStaticAnalyzer(),
    'Java': JavaStaticAnalyzer(),
}

def run_static_analysis(code, lang):
    analyzer = STATIC_ANALYZERS.get(lang)
    if analyzer:
        return analyzer.analyze(code)
    return StaticComplexityResult(time='Unknown', space='Unknown', confidence=0.0)

def query_llm(code, lang):
    analyzer = LLMComplexityAnalyzer()
    return analyzer.analyze(code, language=lang)

def assess_confidence(static_result, llm_result):
    # Simple heuristic: average confidence
    return (static_result.confidence + llm_result.confidence) / 2

@app.get("/ping")
def ping():
    return {
        "status": "ok",
        "message": "PONG! Complexity Analyzer API is running"
    }

@app.post("/analyze")
def analyze_code(request: CodeSubmission):
    lang = detect_language(request.code)
    static_result = run_static_analysis(request.code, lang)
    llm_result = query_llm(request.code, lang)
    confidence = assess_confidence(static_result, llm_result)
    final = merge_results(static_result, llm_result, confidence)
    return final
