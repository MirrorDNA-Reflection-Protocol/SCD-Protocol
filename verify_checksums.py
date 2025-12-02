#!/usr/bin/env python3
import hashlib, os, sys

FILES = [
    "README.md",
    "SCD_v31_Academic_Paper.docx",
    "SCD_ENDURANCE_1000.json",
    "scd_state_T3.json",
    "scd_engine.py",
]

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

if __name__ == "__main__":
    print("=== SCD v3.1 Checksum Verification ===")
    for f in FILES:
        if not os.path.exists(f):
            print(f"[MISSING] {f}")
        else:
            print(f"[OK] {f}: {sha256_file(f)}")

