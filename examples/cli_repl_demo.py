"""
SCD CLI REPL demo.

Simple command-line loop:
- each user input becomes a new SCD state
- checksum and context are printed every turn
"""

from typing import Dict, Any

from mirrordna_scd import SCDProtocol


def main() -> None:
    scd = SCDProtocol(state_file="scd_cli_state.json")

    print("SCD CLI REPL")
    print("Type messages; empty line to exit.\n")

    turn = scd.get_state().get("turn", 0)

    while True:
        try:
            raw = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            print("Bye.")
            break

        turn += 1
        update: Dict[str, Any] = {
            "turn": turn,
            "last_input": raw,
            "mode": "cli_repl",
        }
        scd.supersede(update)

        print("\n[scd] state:", scd.get_state())
        print("[scd] checksum:", scd.get_checksum())
        print("[scd] context:", scd.get_context_string())
        print()


if __name__ == "__main__":
    main()
