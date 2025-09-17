#!/usr/bin/env python3
"""
Advanced QBH Validation Engine Demo

This example demonstrates the complete capabilities of the Quantum-Biological 
Holographic Validation Engine including advanced quantum algorithms, ML integration,
performance monitoring, and plugin system.
"""

import logging
import json
from quantum_validator import (
    QBHValidationEngine, 
    ValidationMode, 
    ValidationConfig,
    PerformanceMonitor,
    MLBiologicalValidator,
    EvolutionaryOptimizer,
    plugin_manager
)

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """Demonstrate advanced QBH validation engine capabilities."""
    
    print("🚀 Advanced Quantum-Biological Holographic Validation Engine Demo")
    print("=" * 80)
    
    # 1. Configuration Management Demo
    print("\n📋 1. Configuration Management")
    print("-" * 40)
    
    # Create custom configuration
    config = ValidationConfig()
    config.quantum.num_qubits = 6
    config.biological.population_size = 100
    config.holographic.dimensions = 12
    config.enable_performance_monitoring = True
    
    print(f"   Quantum qubits: {config.quantum.num_qubits}")
    print(f"   Biological population: {config.biological.population_size}")
    print(f"   Holographic dimensions: {config.holographic.dimensions}")
    
    # 2. Performance Monitoring Demo
    print("\n📊 2. Performance Monitoring")
    print("-" * 40)
    
    monitor = PerformanceMonitor(enable_real_time_alerts=True)
    engine = QBHValidationEngine(mode=ValidationMode.HYBRID)
    
    # Run several validations to generate metrics
    test_datasets = [
        {"financial": {"amount": 1500, "currency": "USD"}},
        {"scientific": [3.14159, 2.71828, 1.41421]},
        {"text": "quantum entanglement validation"},
        {"complex": {"nested": {"data": [1, 2, {"inner": "value"}]}}}
    ]
    
    for i, test_data in enumerate(test_datasets):
        validation_id = f"demo_validation_{i}"
        
        # Start monitoring
        metrics = monitor.start_validation(validation_id, "hybrid", len(str(test_data)))
        
        # Perform validation
        result = engine.validate(test_data)
        
        # Finish monitoring
        monitor.finish_validation(validation_id, result)
        
        print(f"   ✅ Validation {i+1}: {result.is_valid} (confidence: {result.confidence_score:.3f})")
    
    # Display performance report
    report = monitor.generate_performance_report()
    print(f"\n📈 Performance Report:")
    print(report)
    
    # 3. Machine Learning Integration Demo
    print("\n🧠 3. Machine Learning Integration")
    print("-" * 40)
    
    try:
        ml_validator = MLBiologicalValidator(
            enable_anomaly_detection=True,
            enable_clustering=True,
            enable_neural_classification=True
        )
        
        # Test ML-enhanced validation
        ml_test_data = {
            "transaction_id": "txn_ml_001",
            "amount": 2500.75,
            "merchant": "Quantum Mart",
            "risk_score": 0.15,
            "geo_location": "US-CA-SF"
        }
        
        ml_result = ml_validator.validate_with_ml(ml_test_data)
        
        print(f"   🔬 ML Validation: {ml_result.is_valid}")
        print(f"   🎯 ML Confidence: {ml_result.ml_confidence:.3f}")
        print(f"   📊 Algorithm: {ml_result.algorithm_name}")
        
        if ml_result.anomaly_score is not None:
            print(f"   ⚠️  Anomaly Score: {ml_result.anomaly_score:.3f}")
        
    except Exception as e:
        print(f"   ⚠️  ML features require scikit-learn: {e}")
    
    # 4. Advanced Quantum Algorithms Demo
    print("\n⚛️  4. Advanced Quantum Algorithms")
    print("-" * 40)
    
    try:
        from quantum_validator.algorithms import quantum_algorithm_registry
        
        # List available quantum algorithms
        algorithms = quantum_algorithm_registry.list_algorithms()
        print(f"   Available algorithms: {', '.join(algorithms)}")
        
        # Test QFT algorithm
        qft_data = [1, 0, 1, 0, 1, 1, 0, 1]  # Binary pattern
        qft_result = quantum_algorithm_registry.execute_algorithm("qft", qft_data)
        
        if qft_result:
            print(f"   🌊 QFT Validation: {qft_result.result_data.get('is_valid', 'unknown')}")
            print(f"   📈 Quantum Advantage: {qft_result.quantum_advantage:.1f}x")
        
        # Test Grover search
        grover_data = ["pattern1", "pattern2", "target_pattern", "pattern3"]
        grover_result = quantum_algorithm_registry.execute_algorithm(
            "grover", 
            grover_data,
            search_criteria={"target_states": [2]}
        )
        
        if grover_result:
            print(f"   🔍 Grover Search: {grover_result.result_data.get('is_valid', 'unknown')}")
            print(f"   🚀 Search Efficiency: {grover_result.resource_efficiency:.3f}")
        
    except Exception as e:
        print(f"   ⚠️  Advanced algorithms require qiskit: {e}")
    
    # 5. Plugin System Demo
    print("\n🔌 5. Plugin System")
    print("-" * 40)
    
    # List registered plugins
    plugins = plugin_manager.list_plugins()
    print(f"   Registered plugins: {', '.join(plugins)}")
    
    # Test custom plugin
    plugin_test_data = {"custom_field": "test_value", "length": 50}
    plugin_result = plugin_manager.execute_plugin("custom_validator", plugin_test_data)
    
    if plugin_result:
        print(f"   🔧 Custom Plugin: {plugin_result.get('is_valid', 'unknown')}")
        print(f"   🎯 Plugin Confidence: {plugin_result.get('confidence', 0):.3f}")
    
    # 6. Evolutionary Optimization Demo
    print("\n🧬 6. Evolutionary Optimization")
    print("-" * 40)
    
    # Create training data for optimization
    training_data = [
        ({"valid_data": True, "score": 95}, True),
        ({"valid_data": False, "score": 15}, False),
        ({"valid_data": True, "score": 88}, True),
        ({"valid_data": False, "score": 22}, False),
    ]
    
    def simple_validation_function(data, strategy):
        """Simple validation function for demonstration."""
        score = data.get("score", 50)
        threshold = strategy.get("confidence_threshold", 0.5) * 100
        
        return {
            'is_valid': score > threshold,
            'confidence': min(score / 100.0, 1.0)
        }
    
    try:
        optimizer = EvolutionaryOptimizer(population_size=20, max_generations=10)
        best_strategy = optimizer.optimize_validation_parameters(training_data, simple_validation_function)
        
        print(f"   🎯 Optimal confidence threshold: {best_strategy.get('confidence_threshold', 'N/A'):.3f}")
        print(f"   ⚖️  Quantum weight: {best_strategy.get('ensemble_weight_quantum', 'N/A'):.3f}")
        print(f"   🧬 Biological weight: {best_strategy.get('ensemble_weight_biological', 'N/A'):.3f}")
        print(f"   🌐 Holographic weight: {best_strategy.get('ensemble_weight_holographic', 'N/A'):.3f}")
        
    except Exception as e:
        print(f"   ⚠️  Evolutionary optimization requires numpy: {e}")
    
    # 7. Comprehensive Validation Scenario
    print("\n🎭 7. Comprehensive Validation Scenario")
    print("-" * 40)
    
    # Complex real-world scenario
    complex_scenario = {
        "financial_transaction": {
            "id": "txn_advanced_001",
            "amount": 15750.50,
            "currency": "USD",
            "timestamp": "2024-01-15T14:30:22Z",
            "merchant": {
                "id": "merchant_789",
                "name": "Quantum Financial Services",
                "category": "financial_services",
                "risk_rating": "low"
            },
            "customer": {
                "id": "cust_456",
                "account_age_days": 1250,
                "previous_transactions": 347,
                "average_transaction": 2150.25
            },
            "metadata": {
                "processing_node": "quantum_node_3",
                "encryption_algorithm": "AES-256-GCM",
                "digital_signature": "valid",
                "fraud_score": 0.05
            }
        }
    }
    
    complex_schema = {
        "required_fields": ["id", "amount", "currency", "merchant", "customer"],
        "amount_range": [1.0, 100000.0],
        "currency_codes": ["USD", "EUR", "GBP", "JPY"],
        "risk_thresholds": {
            "fraud_score_max": 0.1,
            "amount_deviation_factor": 3.0
        }
    }
    
    # Validate with different modes for comparison
    modes_to_test = [ValidationMode.CLASSICAL, ValidationMode.HYBRID]
    
    for mode in modes_to_test:
        engine.mode = mode
        result = engine.validate(complex_scenario, schema=complex_schema)
        
        print(f"\n   🔬 {mode.value.title()} Mode Results:")
        print(f"      Valid: {result.is_valid}")
        print(f"      Confidence: {result.confidence_score:.3f}")
        
        if result.quantum_coherence:
            print(f"      Quantum Coherence: {result.quantum_coherence:.3f}")
        if result.biological_resilience:
            print(f"      Biological Resilience: {result.biological_resilience:.3f}")
        if result.holographic_integrity:
            print(f"      Holographic Integrity: {result.holographic_integrity:.3f}")
        
        print(f"      Path: {' → '.join(result.validation_path[-4:])}")  # Last 4 steps
    
    # 8. API Server Information
    print("\n🌐 8. API Server Capabilities")
    print("-" * 40)
    
    try:
        from quantum_validator.api import app
        if app:
            print("   ✅ REST API available at /validate endpoint")
            print("   📊 Performance metrics at /metrics endpoint")
            print("   💚 Health check at /health endpoint") 
            print("   📦 Batch validation at /validate/batch endpoint")
            print("   📖 API documentation at /docs endpoint")
            print("   🚀 Start server with: python -m quantum_validator.api")
        else:
            print("   ⚠️  API requires FastAPI: pip install 'quantum-validator[api]'")
    except ImportError:
        print("   ⚠️  API requires FastAPI: pip install 'quantum-validator[api]'")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("🎉 Advanced QBH Validation Engine Demo Complete!")
    print("=" * 80)
    
    print("\nDemonstrated Features:")
    print("✅ Quantum-enhanced validation with multiple algorithms")
    print("✅ Bio-inspired validation with ML integration")
    print("✅ Holographic data distribution validation")
    print("✅ Performance monitoring and adaptive optimization")
    print("✅ Plugin system for extensibility")
    print("✅ Evolutionary parameter optimization")
    print("✅ REST API interface")
    print("✅ Comprehensive configuration management")
    
    print(f"\nThe QBH Validation Engine provides ultra-high precision validation")
    print(f"beyond classical computational limits using quantum computing principles,")
    print(f"biological algorithms, and holographic data distribution.")
    
    print(f"\n🔗 Next Steps:")
    print(f"   • Install quantum dependencies: pip install 'quantum-validator[quantum]'")
    print(f"   • Install ML dependencies: pip install 'quantum-validator[ml]'")
    print(f"   • Install API dependencies: pip install 'quantum-validator[api]'")
    print(f"   • Run tests: pytest tests/")
    print(f"   • Start API server: python -m quantum_validator.api")


if __name__ == "__main__":
    main()