# ADR 001: Tree-sitter Integration Strategy

## Status
Accepted

## Context
The Product Engineering Platform (PEP) needs a robust code parsing foundation to enable Code Knowledge Graph generation, architectural analysis, security scanning, and autonomous engineering. We need a solution that can parse multiple programming languages, support incremental updates, and handle malformed code efficiently.

## Decision
We will use **Tree-sitter** as the foundational parsing layer.

### Key Principles

1. **Tree-sitter is strictly a Parser:**
   Tree-sitter takes source code and turns it into a structured concrete syntax tree (CST) that software can inspect. It is NOT an AI model, a dependency analyzer, or a semantic analyzer. It provides the syntax; PEP derives the engineering knowledge.

2. **PEP Code Model Abstraction:**
   PEP will NOT tightly couple its downstream engines to raw Tree-sitter AST/CST. Instead, we will build a `TreeSitterAdapter` that converts Tree-sitter's CST into a normalized **PEP Code Model**. The rest of PEP (LangGraph agents, Architecture Analysis, Decision Board) will only interact with the PEP Code Model.

3. **Incremental & Error-Tolerant:**
   We will leverage Tree-sitter's incremental parsing capabilities and error tolerance to analyze code continuously as it is being written, allowing for dynamic Code Knowledge Graph updates.

## Consequences
- **Positive:** Enables multi-language support (Python, JS/TS, Java, etc.). Facilitates real-time, IDE-like code analysis.
- **Positive:** Isolates downstream analysis from the quirks of specific language grammars through the intermediate PEP Code Model.
- **Negative/Risk:** Requires us to design and maintain a robust PEP Code Model schema that can adequately represent abstractions across multiple programming paradigms (OOP, functional, scripts).

## Next Steps
Define the exact schema for the **PEP Code Model**, determining how entities like Files, Classes, Functions, Imports, Variables, and Calls are represented and interrelated.
