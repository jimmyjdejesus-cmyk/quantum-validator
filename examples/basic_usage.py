#!/usr/bin/env python3
"""
QBH Validation Engine - Basic Usage Example

This example demonstrates the basic usage of the Quantum-Biological 
Holographic Validation Engine for validating different types of data.
"""

import logging
from quantum_validator import QBHValidationEngine, ValidationMode

# Configure logging to see validation process
logging.basicConfig(level=logging.INFO)

def main():
    """Demonstrate QBH validation engine capabilities."""
    
    print("🌟 Quantum-Biological Holographic Validation Engine Demo")
    print("=" * 60)
    
    # Initialize the validation engine in different modes
    engines = {
        "Classical": QBHValidationEngine(mode=ValidationMode.CLASSICAL),
        "Quantum Enhanced": QBHValidationEngine(mode=ValidationMode.QUANTUM_ENHANCED),
        "Bio-Inspired": QBHValidationEngine(mode=ValidationMode.BIO_INSPIRED), 
        "Holographic": QBHValidationEngine(mode=ValidationMode.HOLOGRAPHIC),
        "Hybrid": QBHValidationEngine(mode=ValidationMode.HYBRID)
    }
    
    # Test data samples
    test_cases = [
        {
            "name": "Financial Transaction",
            "data": {
                "transaction_id": "txn_2024_001",
                "amount": 1250.75,
                "currency": "USD",
                "timestamp": "2024-01-15T10:30:00Z",
                "merchant": "Quantum Retail Corp"
            },
            "schema": {
                "required_fields": ["transaction_id", "amount", "currency"],
                "amount_range": [0, 100000],
                "currency_codes": ["USD", "EUR", "GBP"]
            }
        },
        {
            "name": "Scientific Data",
            "data": [1.414, 2.718, 3.141, 1.618, 0.577],  # Mathematical constants
            "schema": {
                "data_type": "numerical_array",
                "min_length": 3,
                "value_range": [0, 10]
            }
        },
        {
            "name": "Text Content",
            "data": "The quantum entanglement validates holographic information distribution",
            "schema": {
                "data_type": "text",
                "min_length": 10,
                "allowed_topics": ["quantum", "science", "technology"]
            }
        }
    ]
    
    # Run validation tests across all modes
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print("-" * 40)
        
        for mode_name, engine in engines.items():
            print(f"\n🔬 {mode_name} Mode:")
            
            try:
                result = engine.validate(
                    data=test_case["data"],
                    schema=test_case["schema"]
                )
                
                # Display results
                print(f"   ✅ Valid: {result.is_valid}")
                print(f"   🎯 Confidence: {result.confidence_score:.3f}")
                
                if result.quantum_coherence is not None:
                    print(f"   ⚛️  Quantum Coherence: {result.quantum_coherence:.3f}")
                
                if result.biological_resilience is not None:
                    print(f"   🧬 Biological Resilience: {result.biological_resilience:.3f}")
                
                if result.holographic_integrity is not None:
                    print(f"   🌐 Holographic Integrity: {result.holographic_integrity:.3f}")
                
                print(f"   🛤️  Path: {' → '.join(result.validation_path[-3:])}")  # Last 3 steps
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
    
    # Demonstrate advanced hybrid validation
    print(f"\n🚀 Advanced Hybrid Validation Demo")
    print("=" * 60)
    
    hybrid_engine = QBHValidationEngine(mode=ValidationMode.HYBRID)
    
    # Complex test case requiring multi-dimensional validation
    complex_data = {
        "quantum_state": {
            "qubits": 4,
            "entanglement_pairs": [(0, 1), (2, 3)],
            "measurement_basis": "computational"
        },
        "biological_parameters": {
            "population_size": 1000,
            "mutation_rate": 0.01,
            "selection_pressure": 0.8
        },
        "holographic_distribution": {
            "dimensions": 8,
            "redundancy_factor": 3.2,
            "reconstruction_threshold": 0.85
        }
    }
    
    result = hybrid_engine.validate(complex_data)
    
    print(f"\n📈 Hybrid Validation Results:")
    print(f"   Overall Validity: {result.is_valid}")
    print(f"   Confidence Score: {result.confidence_score:.3f}")
    print(f"   Quantum Coherence: {result.quantum_coherence:.3f}")
    print(f"   Biological Resilience: {result.biological_resilience:.3f}")
    print(f"   Holographic Integrity: {result.holographic_integrity:.3f}")
    print(f"   Validation Path: {' → '.join(result.validation_path)}")
    
    if result.error_details:
        print(f"   Error Details: {result.error_details}")
    
    print(f"\n✨ QBH Validation Engine Demo Complete!")
    print(f"   The engine demonstrated quantum-enhanced, bio-inspired,")
    print(f"   and holographic validation approaches working together")
    print(f"   to achieve ultra-high precision validation beyond classical limits.")


if __name__ == "__main__":
    main()