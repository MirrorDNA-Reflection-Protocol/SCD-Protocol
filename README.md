# SCD Protocol

Deterministic, vendor-independent state management for AI agents. Relocates agent memory from volatile model internals to cryptographically verified filesystem artifacts.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18629531.svg)](https://doi.org/10.5281/zenodo.18629531)
[![PyPI](https://img.shields.io/pypi/v/mirrordna-scd.svg)](https://pypi.org/project/mirrordna-scd/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Overview

Structured Contextual Distillation (SCD) is a state protocol for AI agents. It provides deterministic checksums, cross-vendor continuity, drift detection, and a full audit trail over every state transition.

Current approaches to agent memory -- RAG, conversation history, vendor-specific memory APIs -- each fail to provide what autonomous agents require: deterministic, verifiable, portable state that persists across sessions and across vendors. SCD solves this by treating agent state as a first-class filesystem artifact rather than an opaque model internal.

**Production status:** Running continuously in the [MirrorDNA](https://github.com/MirrorDNA-Reflection-Protocol/MirrorBrain) sovereign AI stack since January 2026.

## Design Principles

- **External** -- State lives on disk as inspectable JSON, not inside model weights or context windows
- **Canonical** -- RFC 8785 JSON canonicalization ensures byte-identical serialization across any platform
- **Deterministic** -- Turn-based versioning with monotonically increasing counters; same inputs produce same outputs
- **Governed** -- Constitutional locks protect invariants that cannot be overridden by prompt-level instructions
- **Vendor-independent** -- State files port between Claude, Gemini, GPT, Ollama, and any other LLM
- **Tamper-evident** -- SHA-256 integrity chains make any unauthorized modification immediately detectable

## Installation

```bash
pip install mirrordna-scd
```

## Usage

```python
from mirrordna_scd import SCDProtocol

# Initialize with optional persistence
scd = SCDProtocol(state_file="agent_state.json")

# Update state atomically
scd.supersede({
    "project": "MyApp",
    "mode": "production",
    "version": "1.0"
})

# Verify integrity
print(scd.get_checksum())  # ASHA-256:a3f2b9c1...

# Export for cross-vendor handoff
exported = scd.export_state()

# Import on a different vendor
scd_other = SCDProtocol()
scd_other.import_state(exported)  # Verified handoff
```

## API Reference

| Method | Description |
|--------|-------------|
| `SCDProtocol(state_file=None)` | Initialize protocol with optional persistence file |
| `.supersede(deltas: dict)` | Atomically update state. Setting a value to `None` deletes the key |
| `.get_checksum()` | Return current ASHA-256 checksum |
| `.get_context_string()` | Format state for LLM context injection |
| `.export_state()` | Export state as JSON for cross-vendor handoff |
| `.import_state(json_str)` | Import and verify state from another vendor |
| `SCDProtocol.verify_checksum(state)` | Static method to verify state integrity |

ASHA-256 (Alphabetically Sorted Hashing Algorithm) ensures that key insertion order does not affect checksums. Two state objects with the same key-value pairs always produce the same checksum.

## Validation

The protocol has been validated across four tiers:

- **Functional integrity** -- 24/24 tests passed on both Gemini and Claude
- **Cross-vendor handoff** -- State initialized on Gemini, modified, exported to Claude, verified, modified, re-imported to Gemini with full integrity chain preserved
- **Endurance** -- 1,005 sequential state transitions with zero checksum failures and zero corruption (5.3 ms total)
- **Adversarial defense** -- Indirect prompt injection payloads embedded in files were blocked by the constitutional governance layer

## Examples

The `examples/` directory contains working demonstrations:

- `basic_demo.py` -- Minimal state, checksum, and context usage
- `cli_repl_demo.py` -- Interactive REPL using SCD as session memory
- `cross_vendor_handoff_demo.py` -- Simulated platform handoff
- `langgraph_demo/` -- Deterministic workflow integration with LangGraph

## Research

Two peer-reviewed papers document the protocol:

- **SCD v3.1** -- Desai, P. (2026). *Structured Contextual Distillation (SCD v3.1): A Deterministic, Vendor-Independent Protocol for Persistent, Verifiable Agent State.* DOI: [10.5281/zenodo.18629531](https://doi.org/10.5281/zenodo.18629531)

- **SCD v4** -- Desai, P. (2026). *Structured Contextual Distillation v4: Deployment Benchmarks and Artifact-Backed Evidence from 10 Months of AI State Management.* DOI: [10.5281/zenodo.18910362](https://doi.org/10.5281/zenodo.18910362)

## Citation

```bibtex
@software{desai2026scd,
  author = {Desai, Paul},
  title = {SCD Protocol: Deterministic State Management for AI},
  year = {2026},
  doi = {10.5281/zenodo.18629531},
  url = {https://github.com/MirrorDNA-Reflection-Protocol/SCD-Protocol}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Built by [Active Mirror](https://activemirror.ai) -- Governed AI for Institutional Work.
