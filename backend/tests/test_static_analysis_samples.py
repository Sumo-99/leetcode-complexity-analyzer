import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.static_analysis.python_analyzer import PythonStaticAnalyzer
from core.static_analysis.cpp_analyzer import CppStaticAnalyzer
from core.static_analysis.java_analyzer import JavaStaticAnalyzer

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), '../examples/sample_codes')


def test_python_static_analysis():
    with open(os.path.join(SAMPLE_DIR, 'sample.py'), 'r') as f:
        code = f.read()
    analyzer = PythonStaticAnalyzer()
    result = analyzer.analyze(code)
    print('Python Analysis:', result)

def test_cpp_static_analysis():
    with open(os.path.join(SAMPLE_DIR, 'sample.cpp'), 'r') as f:
        code = f.read()
    analyzer = CppStaticAnalyzer()
    result = analyzer.analyze(code)
    print('C++ Analysis:', result)

def test_java_static_analysis():
    with open(os.path.join(SAMPLE_DIR, 'sample.java'), 'r') as f:
        code = f.read()
    analyzer = JavaStaticAnalyzer()
    result = analyzer.analyze(code)
    print('Java Analysis:', result)

if __name__ == "__main__":
    test_python_static_analysis()
    test_cpp_static_analysis()
    test_java_static_analysis()
