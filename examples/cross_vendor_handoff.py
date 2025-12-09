"""Cross-vendor handoff example

Demonstrates starting a conversation on one AI platform and continuing on another.
"""

from mirrordna_scd import SCDProtocol

print("=" * 60)
print("SCENARIO: Cross-Vendor Handoff")
print("=" * 60)

# === On Claude (or any AI vendor) ===
print("\n[Step 1] On Claude:")
scd_claude = SCDProtocol()
scd_claude.supersede({
    "vendor": "claude",
    "task": "Write research paper",
    "sections_completed": ["introduction", "methodology"]
})

print(f"  Turn: {scd_claude.get_turn()}")
print(f"  Checksum: {scd_claude.get_checksum()[:30]}...")

# Export state for handoff

exported_state = scd_claude.export_state()
print(f"\n[Step 2] Exporting state ({len(exported_state)} bytes)")

# === On ChatGPT (or different AI vendor) ===
print("\n[Step 3] On ChatGPT:")
scd_chatgpt = SCDProtocol()

# Import the state
success = scd_chatgpt.import_state(exported_state)

if success:
    print("  ✅ State imported successfully!")
    print(f"  Turn: {scd_chatgpt.get_turn()}")
    print(f"  Checksum: {scd_chatgpt.get_checksum()[:30]}...")
    print(f"  Previous vendor: {scd_chatgpt.get_state()['state']['vendor']}")
    
    # Continue the work
    scd_chatgpt.supersede({
        "vendor": "chatgpt",
        "sections_completed": ["introduction", "methodology", "results"]
    })
    
    print("\n[Step 4] Continued work on ChatGPT:")
    print(f"  New turn: {scd_chatgpt.get_turn()}")
    print(f"  Sections: {scd_chatgpt.get_state()['state']['sections_completed']}")
    print("\n✅ Cross-vendor handoff successful!")
else:
    print("  ❌ Import failed - checksum verification error")
