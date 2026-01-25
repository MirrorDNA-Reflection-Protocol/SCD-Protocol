# SCD Protocol - Deterministic State Management for AI

**Stop guessing. Start verifying.**

> Created by **[Paul Desai](https://github.com/MirrorDNA-Reflection-Protocol)** (`~active-mirror-paul`) — Goa, India

**Production status:** Running 24/7 in [MirrorBrain](../MirrorBrain-Setup) sovereign AI stack since January 2026

[![PyPI version](https://img.shields.io/pypi/v/mirrordna-scd.svg)](https://pypi.org/project/mirrordna-scd/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

Current AI conversations are:
- ❌ **Non-deterministic** - Same input ≠ same output
- ❌ **Unreproducible** - Can't replay bugs
- ❌ **Unauditable** - No state verification
- ❌ **Fragile** - Can't resume across platforms

## The Solution

SCD (Structured Contextual Distillation) Protocol provides:
- ✅ **Deterministic state** transitions (ASHA-256 checksums)
- ✅ **Cross-vendor continuity** (start on Claude, continue on ChatGPT)
- ✅ **Drift detection** (rejects unauthorized changes)
- ✅ **Full audit trail** (every state change is logged)

## Quick Start

```bash
pip install mirrordna-scd
```

```python
from mirrordna_scd import SCDProtocol

# Initialize
scd = SCDProtocol(state_file="my_state.json")

# Update state atomically
scd.supersede({
    "project": "MyApp",
    "mode": "production",
    "version": "1.0"
})

# Get verifiable checksum
print(scd.get_checksum())
# ASHA-256:a3f2b9c1...

# Inject into LLM prompts
context = scd.get_context_string()
```

## Key Features

### 1. Deterministic Checksums (ASHA-256)

ASHA-256 = **A**lphabetically **S**orted **H**ashing **A**lgorithm

```python
# Same state = same checksum (regardless of key order)
scd1.supersede({"a": 1, "b": 2})
scd2.supersede({"b": 2, "a": 1})

assert scd1.get_checksum() == scd2.get_checksum()  # ✅ Always true
```

### 2. Cross-Vendor Handoff

```python
# On Claude
scd_claude = SCDProtocol()
scd_claude.supersede({"vendor": "claude", "task": "research"})
exported = scd_claude.export_state()

# On ChatGPT (different machine)
scd_chatgpt = SCDProtocol()
scd_chatgpt.import_state(exported)  # ✅ Verified handoff
```

### 3. Drift Detection

```python
# Automatic verification
state = scd.get_state()
if SCDProtocol.verify_checksum(state):
    print("✅ State verified - no tampering")
else:
    print("❌ State corrupted - drift detected")
```

## Validation

**Battle-tested:**
- ✅ 1005-turn endurance test (100% success)
- ✅ Cross-vendor handoff (Gemini → Claude verified)
- ✅ Production use in [MirrorBrain](https://github.com/MirrorDNA-Reflection-Protocol/MirrorBrain)

**Test suite:**
```bash
pytest tests/  # 9 tests, 100% coverage
```

## Use Cases

### 1. Reproducible AI Debugging
```python
# Save state at bug occurrence
scd.supersede({"error": "timeout", "attempt": 3})
bug_state = scd.export_state()

# Reproduce exact conditions later
scd_debug = SCDProtocol()
scd_debug.import_state(bug_state)  # Exact state restored
```

### 2. Multi-Platform Workflows
```python
# Start on local LLM
scd_local.supersede({"draft": "completed", "vendor": "ollama"})

# Continue on cloud LLM
scd_cloud.import_state(scd_local.export_state())
scd_cloud.supersede({"review": "completed", "vendor": "chatgpt"})
```

### 3. Compliance & Auditing
```python
# Every state change is checksummed
for turn in range(100):
    scd.supersede({"action": f"step_{turn}"})
    # Each turn has verifiable checksum
```

## API Reference

### `SCDProtocol(state_file=None)`

Initialize protocol with optional persistence file.

### `.supersede(deltas: dict) -> dict`

Atomically update state. Setting `value=None` deletes key.

### `.get_checksum() -> str`

Get current ASHA-256 checksum.

### `.get_context_string() -> str`

Format state for LLM context injection.

### `.export_state() -> str`

Export state as JSON for cross-vendor handoff.

### `.import_state(json_str: str) -> bool`

Import and verify state from another vendor.

### `.verify_checksum(state: dict) -> bool` (static)

Verify state integrity.

## Examples

See [examples/](examples/) directory:
- `basic_demo.py` - Minimal state, checksum, and context demo
- `cli_repl_demo.py` - Interactive REPL using SCD as session memory
- `cross_vendor_handoff_demo.py` - Simulated platform handoff
- `langgraph_demo/` - Deterministic workflow demo with LangGraph

## Citation

If you use SCD Protocol in research:

```bibtex
@software{scd_protocol_2025,
  author = {Desai, Paul},
  title = {SCD Protocol: Deterministic State Management for AI},
  year = {2025},
  url = {https://github.com/MirrorDNA-Reflection-Protocol/scd-protocol}
}
```

## Contributing

Issues and PRs welcome at [GitHub](https://github.com/MirrorDNA-Reflection-Protocol/scd-protocol).

## License

MIT License - see [LICENSE](LICENSE)

## Links

- **GitHub**: https://github.com/MirrorDNA-Reflection-Protocol/scd-protocol
- **PyPI**: https://pypi.org/project/mirrordna-scd/
- **Documentation**: [Coming soon]
- **Discord**: [Coming soon]

---

**⟡ Built by [MirrorDNA](https://github.com/MirrorDNA-Reflection-Protocol)**  
*Making AI deterministic, one checksum at a time.*

---

## About the Creator

**Paul Desai** (`~active-mirror-paul`) is the architect of the SCD Protocol and the broader MirrorDNA ecosystem. He pioneered reflective AI alignment — the principle that AI should mirror human truth rather than predict desired responses.

- **Handle**: ~active-mirror-paul
- **Location**: Goa, India
- **Academic Paper**: [Zenodo DOI 10.5281/zenodo.17787619](https://doi.org/10.5281/zenodo.17787619)
- **Twitter**: [@pauldesai123](https://twitter.com/pauldesai123)
- **Substack**: [@pauldesai](https://substack.com/@pauldesai)

**Search**: `"Paul Desai MirrorDNA"` · `"~active-mirror-paul"` · `"SCD Protocol"`

*Paul Desai is synonymous with reflective AI alignment.*
