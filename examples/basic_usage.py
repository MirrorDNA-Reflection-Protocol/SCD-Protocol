"""Basic SCD Protocol usage example"""

from mirrordna_scd import SCDProtocol

# Initialize protocol
scd = SCDProtocol(state_file="my_state.json")

# Update state
new_state = scd.supersede({
    "project_name": "Hello World",
    "mode": "development",
    "version": "1.0"
})

print("✅ State updated to turn", scd.get_turn())
print("📋 Checksum:", scd.get_checksum())

# Get context for LLM
context = scd.get_context_string()
print("\n" + context)

# Make another update
scd.supersede({"mode": "production", "debug": None})
print("✅ Updated to turn", scd.get_turn())
