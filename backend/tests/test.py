import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.language_detection import detect_language

def test_language_detection():
    test_cases = [
        ("def greet(name):\n    return f'Hello, {name}!'", "python"),
        ("public class HelloWorld {\n    public static void main(String[] args) {\n        int x = 5;\n    }\n}", "java"),
        ("int main() {\n    int x = 10;\n    return 0;\n}", "cpp")
    ]
    for code, expected in test_cases:
        detected = detect_language(code)
        result = 'PASS' if expected in detected else f'FAIL (detected: {detected})'
        print(f"Test for {expected}: {result}")

test_language_detection()
