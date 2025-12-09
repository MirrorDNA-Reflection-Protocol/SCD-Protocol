"""Tests for SCD Protocol core functionality"""

import pytest
import json
import tempfile
from pathlib import Path
from mirrordna_scd import SCDProtocol


def test_genesis_state():
    """Test that genesis state is created correctly"""
    scd = SCDProtocol()
    state = scd.get_state()
    
    assert state["turn"] == 0
    assert state["checksum"] == "GENESIS"
    assert state["state"] == {}


def test_deterministic_checksum():
    """Same state should produce same checksum regardless of key order"""
    scd1 = SCDProtocol()
    scd1.supersede({"a": 1, "b": 2, "c": 3})
    checksum1 = scd1.get_checksum()
    
    scd2 = SCDProtocol()
    scd2.supersede({"c": 3, "a": 1, "b": 2})  # Different order
    checksum2 = scd2.get_checksum()
    
    assert checksum1 == checksum2, "Checksums should match regardless of key order"


def test_supersede_updates():
    """Test that supersede correctly updates state"""
    scd = SCDProtocol()
    
    # First update
    state1 = scd.supersede({"key1": "value1"})
    assert state1["turn"] == 1
    assert state1["state"]["key1"] == "value1"
    
    # Second update
    state2 = scd.supersede({"key2": "value2"})
    assert state2["turn"] == 2
    assert state2["state"]["key1"] == "value1"  # Previous key still there
    assert state2["state"]["key2"] == "value2"


def test_supersede_deletion():
    """Test that setting value to None deletes the key"""
    scd = SCDProtocol()
    scd.supersede({"keep": "this", "delete": "this"})
    
    scd.supersede({"delete": None})
    state = scd.get_state()
    
    assert "keep" in state["state"]
    assert "delete" not in state["state"]


def test_checksum_verification():
    """Test checksum verification detects tampering"""
    scd = SCDProtocol()
    scd.supersede({"data": "test"})
    state = scd.get_state()
    
    # Valid state
    assert SCDProtocol.verify_checksum(state) is True
    
    # Tampered state
    tampered = state.copy()
    tampered["checksum"] = "ASHA-256:fakehash"
    assert SCDProtocol.verify_checksum(tampered) is False


def test_persistence():
    """Test that state persists to file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "test_state.json"
        
        # Create and update
        scd1 = SCDProtocol(state_file=str(state_file))
        scd1.supersede({"persistent": "data"})
        turn1 = scd1.get_turn()
        
        # Load in new instance
        scd2 = SCDProtocol(state_file=str(state_file))
        assert scd2.get_turn() == turn1
        assert scd2.get_state()["state"]["persistent"] == "data"


def test_export_import():
    """Test cross-vendor handoff via export/import"""
    # Create state on "vendor 1"
    scd1 = SCDProtocol()
    scd1.supersede({"vendor": "first", "data": [1, 2, 3]})
    
    # Export
    exported = scd1.export_state()
    assert isinstance(exported, str)
    
    # Import on "vendor 2"
    scd2 = SCDProtocol()
    success = scd2.import_state(exported)
    
    assert success is True
    assert scd2.get_turn() == scd1.get_turn()
    assert scd2.get_checksum() == scd1.get_checksum()
    assert scd2.get_state()["state"]["vendor"] == "first"


def test_context_string_format():
    """Test that context string is properly formatted"""
    scd = SCDProtocol()
    scd.supersede({"test": "value"})
    
    context = scd.get_context_string()
    
    assert "[SCD STATE]" in context
    assert "Turn:" in context
    assert "Checksum:" in context
    assert "State:" in context
    assert "ASHA-256:" in context


def test_invalid_import_rejected():
    """Test that invalid state is rejected on import"""
    scd = SCDProtocol()
    
    # Invalid JSON
    assert scd.import_state("not valid json") is False
    
    # Valid JSON but wrong checksum
    invalid_state = json.dumps({
        "turn": 1,
        "state": {"data": "test"},
        "checksum": "ASHA-256:wronghash"
    })
    assert scd.import_state(invalid_state) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
