"""
Cross-vendor handoff simulation demo.

Simulates:
- Vendor A updating SCD state
- Writing to disk
- Vendor B loading the same state and continuing

No real API calls; this is protocol-level only.
"""

from mirrordna_scd import SCDProtocol


STATE_FILE = "scd_cross_vendor_state.json"


def vendor_a() -> None:
    scd = SCDProtocol(state_file=STATE_FILE)

    scd.supersede(
        {
            "vendor": "A",
            "session": "demo-session-1",
            "step": 1,
            "note": "initialized by Vendor A",
        }
    )

    print("[Vendor A] state:", scd.get_state())
    print("[Vendor A] checksum:", scd.get_checksum())
    print()


def vendor_b() -> None:
    scd = SCDProtocol(state_file=STATE_FILE)

    scd.supersede(
        {
            "vendor": "B",
            "step": 2,
            "note": "continued by Vendor B",
        }
    )

    print("[Vendor B] state:", scd.get_state())
    print("[Vendor B] checksum:", scd.get_checksum())
    print()


def main() -> None:
    print("=== Vendor A run ===")
    vendor_a()

    print("=== Vendor B run (same state file) ===")
    vendor_b()

    print("If the checksum after Vendor B matches expectations,")
    print("the handoff was deterministic and verifiable.")


if __name__ == "__main__":
    main()
