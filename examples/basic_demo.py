"""
Basic SCD Protocol demo.

Shows:
- creating an SCDProtocol instance
- updating deterministic state
- computing checksum
- generating a context string
"""

from mirrordna_scd import SCDProtocol


def main() -> None:
    scd = SCDProtocol(state_file=None)

    scd.supersede(
        {
            "project": "MirrorDNA",
            "mode": "demo",
            "turn": 1,
            "note": "basic demo",
        }
    )

    print("SCD deterministic state:")
    print(scd.get_state())
    print()

    print("SCD checksum:")
    print(scd.get_checksum())
    print()

    print("SCD context string:")
    print(scd.get_context_string())
    print()


if __name__ == "__main__":
    main()
