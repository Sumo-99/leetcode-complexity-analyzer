import re
# from guesslang import Guess

def rule_based_detect_leetcode(code: str) -> str:
    code = code.strip()

    # --- Python ---
    if re.search(r"\bdef\s+\w+\s*\(.*\)\s*:", code):
        return "python"
    if re.search(r"\bclass\s+\w+\s*:", code) and "self" in code:
        return "python"
    if re.search(r"\breturn\b", code) and "#" in code:  # Python-style comment
        return "python"

    # --- Java ---
    if re.search(r"\bclass\s+Solution\b", code) and ";" in code:
        return "java"
    if re.search(r"\bpublic\b|\bprivate\b|\bprotected\b", code) and "{" in code:
        return "java"
    if re.search(r"\bList<.*>\b|\bMap<.*>\b|\bString\b", code):
        return "java"

    # --- C++ ---
    if "->" in code or "::" in code:
        return "cpp"
    if re.search(r"\bvector<.*>\b|\bunordered_map<.*>\b|\bint\s+\w+\s*\[", code):
        return "cpp"
    if re.search(r"\bint\b.*\{", code) and ";" in code:
        return "cpp"

    return "unknown"

def detect_language(code: str) -> str:
    lang = rule_based_detect_leetcode(code)
    if lang != "unknown":
        return lang

    # try:
    #     guess = Guess()
    #     lang_name = guess.language_name(code).lower()
    #     if "python" in lang_name:
    #         return "python"
    #     elif "java" in lang_name:
    #         return "java"
    #     elif "c++" in lang_name:
    #         return "cpp"
    # except:
    #     pass

    return "unknown"
