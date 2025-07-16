import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.llm_analysis import LLMComplexityAnalyzer

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), '../examples/sample_codes')

def test_llm_analysis():
    analyzer = LLMComplexityAnalyzer()
    for fname in ['sample.py', 'sample.cpp', 'sample.java']:
        with open(os.path.join(SAMPLE_DIR, fname), 'r') as f:
            code = f.read()
        print(f'LLM Analysis for {fname}:')
        result = analyzer.analyze(code)
        print(result)
        print('-' * 40)

if __name__ == "__main__":
    test_llm_analysis()
