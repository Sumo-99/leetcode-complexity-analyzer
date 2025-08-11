
import re
import ast
from typing import Dict, Any, List, Tuple

def _strip_cpp_java_comments(code: str) -> str:
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    code = re.sub(r"//.*?$", "", code, flags=re.M)
    return code

def _brace_positions(code: str) -> List[Tuple[str, int]]:
    return [(ch, i) for i, ch in enumerate(code) if ch in "{}"]

def _find_function_spans(code: str, language: str) -> List[Tuple[str, int, int]]:
    controls = {"if","for","while","switch","catch","synchronized","try","do","else"}
    sig = re.compile(
        r"""
        (?P<prefix>
            (?:[\w:\<\>\[\]\*&]+\s+)*
        )
        (?P<name>[A-Za-z_]\w*)
        \s*\((?:[^()]|\([^()]*\))*\)\s*
        \{
        """,
        re.X | re.S,
    )
    spans = []
    for m in sig.finditer(code):
        name = m.group("name")
        if name in controls:
            continue
        body_start = m.end() - 1
        depth = 0
        for i in range(body_start, len(code)):
            if code[i] == "{":
                depth += 1
            elif code[i] == "}":
                depth -= 1
                if depth == 0:
                    spans.append((name, body_start, i))
                    break
    return spans

def _max_loop_nesting_java_cpp(code: str) -> int:
    code_nc = _strip_cpp_java_comments(code)
    loop_kw = re.compile(r"\b(for|while|do)\b")
    matches = list(loop_kw.finditer(code_nc))
    if not matches:
        return 0
    max_depth = 0
    depth = 0
    i = 0
    while i < len(code_nc):
        if matches and i == matches[0].start():
            kw = matches.pop(0)
            j = kw.end()
            while j < len(code_nc) and code_nc[j] in " \t\r\n)":
                j += 1
            if j < len(code_nc) and code_nc[j] == "{":
                depth += 1
                max_depth = max(max_depth, depth)
            else:
                max_depth = max(max_depth, depth + 1)
            i = kw.end()
        ch = code_nc[i]
        if ch == "{":
            i += 1
            continue
        elif ch == "}":
            if depth > 0:
                depth -= 1
            i += 1
            continue
        i += 1
    return max_depth

def _space_signals_java_cpp(code: str) -> int:
    code_nc = _strip_cpp_java_comments(code)
    patterns = [
        r"\bnew\s+\w+\s*\[",
        r"\bnew\s+\w+\s*\(",
        r"\bstd::vector\b",
        r"\bstd::string\b",
        r"\bArrayList\b",
        r"\bHashMap\b|\bunordered_map\b",
        r"\bList<",
        r"\bMap<",
        r"\b\w+\s+\w+\s*\[[^\]]*\]",
    ]
    return sum(len(re.findall(p, code_nc)) for p in patterns)

def _is_recursive_java_cpp(code: str) -> bool:
    code_nc = _strip_cpp_java_comments(code)
    spans = _find_function_spans(code_nc, language="java_cpp")
    for name, b0, b1 in spans:
        body = code_nc[b0:b1]
        if re.search(rf"\b{name}\s*\(", body):
            return True
    return False

def analyze_java_cpp(code: str) -> Dict[str, Any]:
    nested = _max_loop_nesting_java_cpp(code)
    recursive = _is_recursive_java_cpp(code)
    space_hits = _space_signals_java_cpp(code)

    if recursive:
        time = "O(T_rec)"
        conf = 0.65
    elif nested >= 2:
        time = f"O(n^{nested})"
        conf = 0.8
    elif nested == 1:
        time = "O(n)"
        conf = 0.9
    else:
        time = "O(1)"
        conf = 0.95

    space = "O(n)" if space_hits > 0 else "O(1)"
    return {
        "time": time,
        "space": space,
        "confidence": conf,
        "signals": {"nested_loops": nested, "recursive": recursive, "space_hits": space_hits},
    }

class _LoopDepthVisitor(ast.NodeVisitor):
    def __init__(self):
        self.max_depth = 0
        self.cur = 0
    def visit_For(self, node):
        self.cur += 1
        self.max_depth = max(self.max_depth, self.cur)
        self.generic_visit(node)
        self.cur -= 1
    def visit_While(self, node):
        self.cur += 1
        self.max_depth = max(self.max_depth, self.cur)
        self.generic_visit(node)
        self.cur -= 1

class _RecursionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.names = set()
        self.recursive = False
    def visit_FunctionDef(self, node):
        self.names.add(node.name)
        self.generic_visit(node)
    def visit_AsyncFunctionDef(self, node):
        self.names.add(node.name)
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.names:
            self.recursive = True
        self.generic_visit(node)

class _SpaceVisitor(ast.NodeVisitor):
    def __init__(self):
        self.list_count = 0
        self.dict_count = 0
        self.set_count = 0
    def visit_List(self, node):
        self.list_count += 1
        self.generic_visit(node)
    def visit_Dict(self, node):
        self.dict_count += 1
        self.generic_visit(node)
    def visit_Set(self, node):
        self.set_count += 1
        self.generic_visit(node)

def analyze_python(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
    except Exception:
        nested = len(re.findall(r"^\s*(for|while)\b", code, flags=re.M))
        return {
            "time": "O(n)" if nested else "O(1)",
            "space": "O(n)" if any(x in code for x in ["[", "{"]) else "O(1)",
            "confidence": 0.5,
            "signals": {"nested_loops": nested, "recursive": False, "space_hits": 0},
        }
    lv = _LoopDepthVisitor()
    lv.visit(tree)
    rv = _RecursionVisitor()
    rv.visit(tree)
    sv = _SpaceVisitor()
    sv.visit(tree)

    if rv.recursive:
        time = "O(T_rec)"
        conf = 0.7
    elif lv.max_depth >= 2:
        time = f"O(n^{lv.max_depth})"
        conf = 0.85
    elif lv.max_depth == 1:
        time = "O(n)"
        conf = 0.92
    else:
        time = "O(1)"
        conf = 0.96

    space_hits = sv.list_count + sv.dict_count + sv.set_count
    space = "O(n)" if space_hits > 0 else "O(1)"
    return {
        "time": time,
        "space": space,
        "confidence": conf,
        "signals": {
            "nested_loops": lv.max_depth,
            "recursive": rv.recursive,
            "space_hits": space_hits,
        },
    }

def analyze_code(language: str, code: str) -> Dict[str, Any]:
    lang = language.lower()
    if lang in ("py", "python"):
        return analyze_python(code)
    if lang in ("java", "c++", "cpp", "cc", "cxx"):
        return analyze_java_cpp(code)
    if "import java" in code or ("class Solution" in code and ";" in code):
        return analyze_java_cpp(code)
    if "#include" in code or "std::" in code:
        return analyze_java_cpp(code)
    if "def " in code or ("for " in code and ":" in code):
        return analyze_python(code)
    return {"time": "N/A", "space": "N/A", "confidence": 0, "signals": {}}
