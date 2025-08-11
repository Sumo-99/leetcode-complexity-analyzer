from .simple_static_analysis import analyze_code

__all__ = ["analyze"]

def analyze(source_code: str):
    """Run static analysis for C++ code using the simplified analyzer."""
    return analyze_code("cpp", source_code)

if __name__ == "__main__":
    import sys, json
    code = sys.stdin.read()
    print(json.dumps(analyze(code), indent=2))
