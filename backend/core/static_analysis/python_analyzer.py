import ast
import networkx as nx
from core.static_analysis.base import BaseStaticAnalyzer
from core.result_schema import StaticComplexityResult

# Python static analyzer implementation
class PythonStaticAnalyzer(BaseStaticAnalyzer):
    def analyze(self, code: str) -> StaticComplexityResult:
        tree = ast.parse(code)
        nested_loops = self._count_nested_loops(tree)
        recursion = self._detect_recursion(tree)
        cfg = self._build_cfg(tree)
        space = self._estimate_space(tree)
        # Heuristic: time complexity increases with nested loops and recursion
        if recursion:
            time = 'O(recursive)'
            confidence = 0.7
        elif nested_loops >= 2:
            time = 'O(n^%d)' % nested_loops
            confidence = 0.8
        elif nested_loops == 1:
            time = 'O(n)'
            confidence = 0.9
        else:
            time = 'O(1)'
            confidence = 0.95
        return StaticComplexityResult(time=time, space=space, confidence=confidence)

    def _count_nested_loops(self, tree):
        class LoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0
            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1
        visitor = LoopVisitor()
        visitor.visit(tree)
        return visitor.max_depth

    def _detect_recursion(self, tree):
        class RecursionVisitor(ast.NodeVisitor):
            def __init__(self):
                self.func_names = set()
                self.recursive = False
            def visit_FunctionDef(self, node):
                self.func_names.add(node.name)
                self.generic_visit(node)
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id in self.func_names:
                    self.recursive = True
                self.generic_visit(node)
        visitor = RecursionVisitor()
        visitor.visit(tree)
        return visitor.recursive

    def _build_cfg(self, tree):
        # Placeholder: In-depth CFG construction can be added as needed
        G = nx.DiGraph()
        # ...build nodes/edges from AST...
        return G

    def _estimate_space(self, tree):
        class SpaceVisitor(ast.NodeVisitor):
            def __init__(self):
                self.list_count = 0
                self.dict_count = 0
            def visit_List(self, node):
                self.list_count += 1
                self.generic_visit(node)
            def visit_Dict(self, node):
                self.dict_count += 1
                self.generic_visit(node)
        visitor = SpaceVisitor()
        visitor.visit(tree)
        if visitor.list_count + visitor.dict_count > 0:
            return 'O(n)'
        return 'O(1)'
