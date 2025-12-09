# LangGraph + SCD Protocol Demo

This example shows how to integrate the **SCD Protocol (mirrordna-scd)** as a
deterministic state layer inside a simple LangGraph workflow.

## Requirements

Install dependencies:

```bash
pip install langgraph mirrordna-scd
```

## Run

From the repo root:

```bash
python3 examples/langgraph_demo/scd_langgraph_example.py
```

You should see:

* A LangGraph result dictionary
* The SCD deterministic state
* The SCD checksum (SHA-256)
* The SCD context string

This demonstrates how SCD can:

* Provide deterministic, replayable state for agent workflows
* Attach a cryptographic checksum to each state update
* Generate a stable context string for use with any LLM or agent framework.
