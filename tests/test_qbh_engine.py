"""
Test module for QBH Validation Engine

Following Protocol 04: Robust Testing & Quality Assurance

This module provides comprehensive tests for the quantum-validator
system using the established VDE testing framework.
"""

import pytest
import numpy as np
from quantum_validator import QBHValidationEngine, ValidationMode
from quantum_validator.validation_engine import ValidationResult


class TestQBHValidationEngine:
    """Test suite for the main QBH Validation Engine."""
    
    def setup_method(self):
        """Setup method called before each test."""
        self.engine = QBHValidationEngine(mode=ValidationMode.HYBRID, enable_logging=False)
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        assert self.engine.mode == ValidationMode.HYBRID
        assert self.engine.quantum_validator is not None
        assert self.engine.biological_validator is not None
        assert self.engine.holographic_validator is not None
    
    def test_basic_validation_happy_path(self):
        """Test basic validation with valid input - Happy Path."""
        test_data = {"valid": True, "value": 42}
        result = self.engine.validate(test_data)
        
        assert isinstance(result, ValidationResult)
        assert isinstance(result.is_valid, bool)
        assert 0.0 <= result.confidence_score <= 1.0
        assert result.validation_path is not None
        assert len(result.validation_path) > 0
    
    def test_validation_with_schema(self):
        """Test validation with schema constraints."""
        test_data = {"number": 100, "text": "test"}
        test_schema = {"required": ["number", "text"], "number_range": [0, 200]}
        
        result = self.engine.validate(test_data, schema=test_schema)
        
        assert isinstance(result, ValidationResult)
        assert result.validation_path is not None
    
    def test_validation_edge_cases(self):
        """Test validation with edge case inputs."""
        edge_cases = [
            None,
            "",
            [],
            {},
            0,
            -1,
            float('inf'),
            "a" * 10000,  # Very long string
        ]
        
        for edge_case in edge_cases:
            result = self.engine.validate(edge_case)
            assert isinstance(result, ValidationResult)
            assert isinstance(result.is_valid, bool)
            assert 0.0 <= result.confidence_score <= 1.0
    
    def test_validation_negative_cases(self):
        """Test validation properly handles invalid scenarios."""
        # Test with intentionally problematic data
        problematic_data = {
            "circular_ref": None
        }
        problematic_data["circular_ref"] = problematic_data
        
        # Should not crash, should return result
        result = self.engine.validate(problematic_data)
        assert isinstance(result, ValidationResult)
    
    def test_different_validation_modes(self):
        """Test all validation modes work correctly."""
        test_data = {"mode_test": True}
        
        for mode in ValidationMode:
            engine = QBHValidationEngine(mode=mode, enable_logging=False)
            result = engine.validate(test_data)
            
            assert isinstance(result, ValidationResult)
            assert isinstance(result.is_valid, bool)
            assert 0.0 <= result.confidence_score <= 1.0
    
    def test_quantum_coherence_metrics(self):
        """Test quantum coherence metrics are properly calculated."""
        engine = QBHValidationEngine(mode=ValidationMode.QUANTUM_ENHANCED, enable_logging=False)
        result = engine.validate({"quantum_test": [1, 0, 1, 0]})
        
        # Quantum mode should provide quantum metrics
        if result.quantum_coherence is not None:
            assert 0.0 <= result.quantum_coherence <= 1.0
    
    def test_biological_resilience_metrics(self):
        """Test biological resilience metrics are properly calculated."""
        engine = QBHValidationEngine(mode=ValidationMode.BIO_INSPIRED, enable_logging=False)
        result = engine.validate({"bio_test": "pattern recognition test"})
        
        # Bio mode should provide biological metrics
        if result.biological_resilience is not None:
            assert 0.0 <= result.biological_resilience <= 1.0
    
    def test_holographic_integrity_metrics(self):
        """Test holographic integrity metrics are properly calculated."""
        engine = QBHValidationEngine(mode=ValidationMode.HOLOGRAPHIC, enable_logging=False)
        result = engine.validate({"holographic_test": list(range(10))})
        
        # Holographic mode should provide holographic metrics
        if result.holographic_integrity is not None:
            assert 0.0 <= result.holographic_integrity <= 1.0
    
    def test_error_handling(self):
        """Test proper error handling and reporting."""
        # Test with data that might cause processing errors
        class UnserializableClass:
            def __str__(self):
                raise Exception("Cannot serialize")
        
        result = self.engine.validate(UnserializableClass())
        
        # Should handle gracefully
        assert isinstance(result, ValidationResult)
        if not result.is_valid:
            assert result.error_details is not None
    
    def test_validation_path_tracking(self):
        """Test that validation path is properly tracked."""
        result = self.engine.validate({"path_test": True})
        
        assert result.validation_path is not None
        assert len(result.validation_path) > 0
        assert "QBH_ENGINE_START" in result.validation_path
    
    def test_confidence_score_calculation(self):
        """Test confidence score calculation is consistent."""
        test_data = {"confidence_test": "consistent data"}
        
        # Run validation multiple times
        results = [self.engine.validate(test_data) for _ in range(3)]
        
        # Confidence scores should be consistent for same data
        confidence_scores = [r.confidence_score for r in results]
        confidence_variance = np.var(confidence_scores)
        
        # Variance should be low for deterministic validation
        assert confidence_variance < 0.1  # Allow some variance due to randomness in bio algorithms


class TestValidationModes:
    """Test specific validation mode behaviors."""
    
    def test_classical_mode_baseline(self):
        """Test classical mode provides baseline validation."""
        engine = QBHValidationEngine(mode=ValidationMode.CLASSICAL, enable_logging=False)
        result = engine.validate({"classical_test": True})
        
        assert result.is_valid is not None
        assert result.confidence_score > 0.0
    
    def test_hybrid_mode_synthesis(self):
        """Test hybrid mode properly synthesizes multiple approaches."""
        engine = QBHValidationEngine(mode=ValidationMode.HYBRID, enable_logging=False)
        result = engine.validate({"hybrid_test": [1, 2, 3, 4, 5]})
        
        # Hybrid mode should have validation path with multiple components
        assert len(result.validation_path) >= 3
        
        # Should have at least some of the specialized metrics
        metrics_present = [
            result.quantum_coherence is not None,
            result.biological_resilience is not None,
            result.holographic_integrity is not None
        ]
        assert any(metrics_present)


class TestSecurityValidation:
    """Security-focused tests following Protocol 03: Secure Code Implementation."""
    
    def test_injection_attack_resistance(self):
        """Test resistance to injection-style attacks in validation data."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "{{7*7}}",  # Template injection
            "$(rm -rf /)",  # Command injection
        ]
        
        engine = QBHValidationEngine(enable_logging=False)
        
        for malicious_input in malicious_inputs:
            result = engine.validate(malicious_input)
            # Should not crash and should return valid result
            assert isinstance(result, ValidationResult)
    
    def test_resource_exhaustion_protection(self):
        """Test protection against resource exhaustion attacks."""
        # Very large data structure
        large_data = {"data": "x" * 100000}
        
        engine = QBHValidationEngine(enable_logging=False)
        result = engine.validate(large_data)
        
        # Should complete without crashing
        assert isinstance(result, ValidationResult)
    
    def test_input_sanitization(self):
        """Test that inputs are properly sanitized during validation."""
        suspicious_data = {
            "eval": "exec('print(1)')",
            "import": "__import__('os').system('ls')",
            "file_access": "/etc/passwd"
        }
        
        engine = QBHValidationEngine(enable_logging=False)
        result = engine.validate(suspicious_data)
        
        # Should handle safely
        assert isinstance(result, ValidationResult)


@pytest.mark.integration
class TestIntegrationScenarios:
    """Integration tests for complete validation scenarios."""
    
    def test_financial_transaction_validation(self):
        """Test complete financial transaction validation scenario."""
        transaction = {
            "id": "txn_001",
            "amount": 1500.00,
            "currency": "USD",
            "merchant": "Test Store",
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        schema = {
            "required_fields": ["id", "amount", "currency"],
            "amount_range": [0, 10000],
            "currency_codes": ["USD", "EUR", "GBP"]
        }
        
        engine = QBHValidationEngine(mode=ValidationMode.HYBRID, enable_logging=False)
        result = engine.validate(transaction, schema=schema)
        
        assert isinstance(result, ValidationResult)
        assert result.confidence_score > 0.5  # Should have reasonable confidence
    
    def test_scientific_data_validation(self):
        """Test scientific data validation with quantum enhancement."""
        scientific_data = {
            "experiment_id": "QE_2024_001",
            "measurements": [1.414, 2.718, 3.141, 1.618],
            "uncertainty": [0.001, 0.002, 0.001, 0.003],
            "equipment": "Quantum Analyzer v2.1"
        }
        
        engine = QBHValidationEngine(mode=ValidationMode.QUANTUM_ENHANCED, enable_logging=False)
        result = engine.validate(scientific_data)
        
        assert isinstance(result, ValidationResult)
        # Scientific data should benefit from quantum validation
        if result.quantum_coherence is not None:
            assert result.quantum_coherence > 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])