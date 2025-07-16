from tree_sitter import Language, Parser
from core.static_analysis.base import BaseStaticAnalyzer
from core.result_schema import StaticComplexityResult
import os

LIB_PATH = os.path.join(os.path.dirname(__file__), 'build', 'my-languages.so')

class JavaStaticAnalyzer(BaseStaticAnalyzer):
    def __init__(self):
        JAVA_LANGUAGE = Language(LIB_PATH, 'java')
        self.parser = Parser()
        self.parser.set_language(JAVA_LANGUAGE)

    def analyze(self, code: str) -> StaticComplexityResult:
        tree = self.parser.parse(bytes(code, "utf8"))
        root = tree.root_node
        nested_loops = self._count_nested_loops(root)
        recursion = self._detect_recursion(root)
        space = self._estimate_space(root)
        if recursion:
            time = 'O(recursive)'
            confidence = 0.7
        elif nested_loops >= 2:
            time = f'O(n^{nested_loops})'
            confidence = 0.8
        elif nested_loops == 1:
            time = 'O(n)'
            confidence = 0.9
        else:
            time = 'O(1)'
            confidence = 0.95
        return StaticComplexityResult(time=time, space=space, confidence=confidence)

    def _count_nested_loops(self, node):
        def visit(node, depth=0):
            max_depth = depth
            for child in node.children:
                if child.type in ('for_statement', 'while_statement', 'do_statement', 'enhanced_for_statement'):
                    max_depth = max(max_depth, visit(child, depth+1))
                else:
                    max_depth = max(max_depth, visit(child, depth))
            return max_depth
        return visit(node)

    def _detect_recursion(self, node):
        func_names = set()
        recursive = False
        def visit(node, current_func=None):
            nonlocal recursive
            if node.type == 'method_declaration':
                for child in node.children:
                    if child.type == 'identifier':
                        current_func = child.text.decode()
                        func_names.add(current_func)
                for child in node.children:
                    visit(child, current_func)
            elif node.type == 'method_invocation':
                for child in node.children:
                    if child.type == 'identifier' and current_func and child.text.decode() == current_func:
                        recursive = True
            for child in node.children:
                visit(child, current_func)
        visit(node)
        return recursive

    def _estimate_space(self, node):
        array_count = 0
        def visit(node):
            nonlocal array_count
            if node.type in ('array_creation_expression', 'object_creation_expression'):
                array_count += 1
            for child in node.children:
                visit(child)
        visit(node)
        return 'O(n)' if array_count > 0 else 'O(1)'
