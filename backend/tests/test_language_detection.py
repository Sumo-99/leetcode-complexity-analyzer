import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.language_detection import detect_language
import unittest

class TestLanguageDetection(unittest.TestCase):
    def test_python_code(self):
        code = """
def hello():
    print('Hello, world!')
"""
        lang = detect_language(code)
        print(f"Detected language for Python code: {lang}")
        self.assertIn(lang, ['Python', 'Python 3'])

    def test_java_code(self):
        code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
        lang = detect_language(code)
        print(f"Detected language for Java code: {lang}")
        self.assertIn(lang, ['Java'])

    def test_cpp_code(self):
        code = """
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
        lang = detect_language(code)
        print(f"Detected language for C++ code: {lang}")
        self.assertIn(lang, ['C++'])

    def test_short_python_code(self):
        code = "print(1)"
        lang = detect_language(code)
        print(f"Detected language for short Python code: {lang}")
        self.assertIn(lang, ['Python', 'Python 3'])

    def test_short_java_code(self):
        code = "System.out.println(1);"
        lang = detect_language(code)
        print(f"Detected language for short Java code: {lang}")
        self.assertIn(lang, ['Java'])

    def test_short_cpp_code(self):
        code = "std::cout << 1;"
        lang = detect_language(code)
        print(f"Detected language for short C++ code: {lang}")
        self.assertIn(lang, ['C++'])

    def test_unknown_code(self):
        code = "This is not code."
        lang = detect_language(code)
        print(f"Detected language for unknown code: {lang}")
        self.assertEqual(lang, 'Unknown')

if __name__ == "__main__":
    unittest.main()
