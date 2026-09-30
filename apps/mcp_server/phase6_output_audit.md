# Phase 6 Output Audit

## 1. Discovery Output Structure
**What is discovered:** Business-level metadata, organizational structure, and linear execution traces of processes.
- **From `OrganizationKnowledgeModel` (OKM):** `name`, `type`, `industry`, `country`, `departments`, `roles`, `policies`, and business-level `workflows` (including approval chains and triggers).
- **From `ProcessIntelligenceEngine` (PIE):** Linear `steps` (traces) representing expected (Camunda BPMN) vs. actual (PM4Py event logs) execution.
- **Overlap:** OKM's `workflows` describe the *business rules* and *roles* of a process, whereas PIE describes the *temporal execution sequence* (the "how"). They represent the same concept at different layers of abstraction.
- **Data Loss:** At the `AnalysisContext` level, nothing is lost (the raw OKM Pydantic object and PIE dicts are stored intact). However, the `DiscoveryService` MCP response discards this rich tree, returning a flattened summary (e.g., `processes_expected: 3`).

## 2. Graph Output Structure
**What is built:** A code-level dependency and semantic syntax graph.
- **Tree-sitter contribution:** `PEPGraph` containing AST `nodes` (functions, classes) and structural `edges` (`calls` relationships).
- **LSP contribution:** Semantic symbols and their physical `locations`.
- **KnowledgeGraphBuilder contribution:** Merges these into a `KnowledgeGraph` by linking AST nodes to LSP semantic symbols.
- **Adequacy:** This graph ONLY represents source code. It has zero awareness of business processes, organizational roles, or infrastructure. Therefore, calling it the "PEP Knowledge Graph" is premature; it is strictly a **Code Dependency Graph**. To support future phases (Maturity, AI Opportunities), the graph must eventually bridge code nodes to OKM business nodes.

## 3. Architecture Output Structure
**What is produced:** Architectural findings and violations.
- **Output:** A list of `dict`s containing `engine`, `severity`, `message`, and `edge` (the offending relationship).
- **Behavior:** `ArchitectureEngine` does NOT enrich the graph. It purely *analyzes* the `KnowledgeGraph` to detect anti-patterns (e.g., controllers calling controllers directly) and outputs isolated findings. It operates strictly on the code structure, independent of discovery data.

## 4. Identify Duplicated Computation
Currently, `ArchitectureService` silently checks if `context.graph` exists. If absent, it invokes `KnowledgeGraphBuilder().build()`. If `GraphService` is subsequently called, it executes the identical heavy AST/LSP parsing sequence again. 
**Conclusion:** `GraphService` *must* precede `ArchitectureService`. The hidden builder fallback inside `ArchitectureService` creates an invisible, expensive duplicate analysis path that defeats the purpose of the `AnalysisContext`.

## 5. Audit Data Loss Table
| Source | Current Context | MCP API Response | Lost? |
| :--- | :--- | :--- | :--- |
| `OrganizationKnowledgeModel` | `discovered_system["organization"]` | Flattened Summary | Lost across MCP boundary |
| Process Intelligence | `discovered_system["processes"]` | Flattened Summary | Lost across MCP boundary |
| `KnowledgeGraph` | `graph` | Flattened Summary | Lost across MCP boundary |
| Architecture Output | `architecture` | Full Findings | Preserved |

## 6. Tree-sitter + LSP Synergy
- **Tree-sitter:** Provides fast, syntax-level structural relationships (e.g., Function A calls Function B).
- **LSP:** Provides deep, semantic resolution (e.g., Function A's definition exists in file X, line Y, and is of type Z).
- **Synergy:** `GraphService` isn't just a utility; it is the fundamental bridge that grounds arbitrary AST tokens into real, semantic codebase coordinates. This makes it the absolute bedrock for any subsequent code generation or refactoring layer.

## 7. Recommended Changes Before Phase 7
1. **Enforce Strict Dependencies:** Remove the hidden `KnowledgeGraphBuilder` fallback from `ArchitectureService`. It should throw a hard `MISSING_DEPENDENCY` error if `context.graph` is unpopulated.
2. **Rename Graph Context:** Rename `context.graph` to `context.code_graph` to explicitly distinguish it from the business OKM graph, setting the stage for a true unified graph later.
3. **Build the Evidence Model:** The data loss across the MCP boundary proves that Phase 7 must establish an `EvidenceModel` capable of safely serializing these rich internal structures back to the MCP client, rather than relying on arbitrary string flattening in the service layer.
