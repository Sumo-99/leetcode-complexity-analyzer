from tree_sitter import Language
import os

BUILD_DIR = os.path.join("core", "static_analysis", "build")
os.makedirs(BUILD_DIR, exist_ok=True)
LIB_PATH = os.path.join(BUILD_DIR, "my-languages.so")

GRAMMARS = [
    os.path.join("core", "static_analysis", "tree-sitter-cpp"),
    os.path.join("core", "static_analysis", "tree-sitter-java"),
]

print(f"Building Tree-sitter language library at {LIB_PATH}...")
Language.build_library(LIB_PATH, GRAMMARS)
print("✅ Tree-sitter library built successfully!")
