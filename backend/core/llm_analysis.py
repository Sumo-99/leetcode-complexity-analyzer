
import os
from core.result_schema import LLMComplexityResult
from core.config import settings

# Example using OpenAI API (requires openai package and API key)
try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
except ImportError:
    client = None

class LLMComplexityAnalyzer:
    def __init__(self, model="gpt-3.5-turbo"):
        if client is None:
            raise ImportError("openai package is required for LLM analysis.")
        self.model = model

    def analyze(self, code: str, language: str = None) -> LLMComplexityResult:
        prompt = self._build_prompt(code, language)
        response = client.chat.completions.create(model=self.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.0)
        result = self._parse_response(response.choices[0].message.content)
        return result

    def _build_prompt(self, code, language=None):
        lang_str = f" in {language}" if language else ""
        return (
            f"Analyze the following code{lang_str} and estimate its time and space complexity. "
            "Respond in the format: Time: <complexity>, Space: <complexity>, Confidence: <0-1>.\n. " \
            "Also provide a simple explanation for your estimates.\n\n" \
            f"Code:\n{code}"
        )

    def _parse_response(self, response_text):
        import re
        time, space, confidence = 'Unknown', 'Unknown', 0.5
        time_match = re.search(r'Time:\s*([\w\(\)\^\/\*\+\-]+)', response_text, re.I)
        space_match = re.search(r'Space:\s*([\w\(\)\^\/\*\+\-]+)', response_text, re.I)
        conf_match = re.search(r'Confidence:\s*([0-9.]+)', response_text, re.I)
        if time_match:
            time = time_match.group(1)
        if space_match:
            space = space_match.group(1)
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
            except Exception:
                confidence = 0.5
        return LLMComplexityResult(time=time, space=space, confidence=confidence)
