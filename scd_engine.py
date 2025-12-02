"""SCD v3.1 reference helper for state + checksum operations, based on the Structured Contextual Distillation paper by Paul Desai (December 2025)."""

import json
import hashlib
import os
import logging

logger = logging.getLogger("mirrorbrain.scd")

class SCDEngine:
    def __init__(self, state_file="scd_state.json"):
        self.state_file = state_file
        self.current_state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load SCD state: {e}")
        
        # Default Genesis State
        return {
            "version": "v3.0-Antigravity",
            "turn": 0,
            "state": {
                "project_name": "MirrorBrain-Core",
                "mode": "Sovereign",
                "constitutional_lock": False
            },
            "checksum": "GENESIS",
            "glyph": "ANCHOR RESET"
        }

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.current_state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save SCD state: {e}")

    def compute_checksum(self, state_dict):
        """Computes ASHA-256 checksum on sorted state."""
        state_json = json.dumps(state_dict, sort_keys=True).encode('utf-8')
        sha256_hash = hashlib.sha256(state_json).hexdigest()
        return f"ASHA-256:{sha256_hash}"

    def supersede(self, deltas):
        """Atomically apply updates and return new full state object."""
        prev_inner_state = self.current_state["state"]
        new_inner_state = prev_inner_state.copy()
        
        for key, value in deltas.items():
            if value is None:
                new_inner_state.pop(key, None)
            else:
                new_inner_state[key] = value
        
        new_checksum = self.compute_checksum(new_inner_state)
        
        new_full_state = {
            "version": self.current_state["version"],
            "turn": self.current_state["turn"] + 1,
            "state": new_inner_state,
            "checksum": new_checksum,
            "glyph": "STATE UPDATE"
        }
        
        self.current_state = new_full_state
        self.save_state()
        return new_full_state

    def get_context_string(self):
        """Returns the formatted string for LLM context injection."""
        s = self.current_state
        return f"""
[SCD STATE]
Turn: {s['turn']}
Checksum: {s['checksum']}
State: {json.dumps(s['state'], indent=2)}
"""
