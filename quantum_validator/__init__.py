"""
Quantum-Biological Holographic (QBH) Validation Engine

This package provides quantum-enhanced validation capabilities using 
bio-inspired algorithms and holographic data distribution patterns.

Complete implementation includes:
- Core validation engines (quantum, biological, holographic)
- Advanced quantum algorithms (QFT, Grover, entanglement)
- Machine learning integration for bio-inspired validation
- Performance monitoring and adaptive thresholds
- Plugin system for extensibility
- REST API server for remote validation
- Comprehensive CLI interface
"""

__version__ = "0.1.0"
__author__ = "QBH Validation Team"

from .core.quantum_validator import QuantumValidator
from .core.biological_validator import BiologicalValidator
from .core.holographic_validator import HolographicValidator
from .validation_engine import QBHValidationEngine, ValidationMode, ValidationResult
from .config import ValidationConfig, QuantumConfig, BiologicalConfig, HolographicConfig
from .monitoring import PerformanceMonitor, AdaptiveThresholdMonitor
from .plugins import PluginManager, plugin_manager
from .ml_integration import MLBiologicalValidator, EvolutionaryOptimizer

# Optional imports with graceful fallbacks
try:
    from .algorithms import quantum_algorithm_registry
    __all_algorithms__ = ["quantum_algorithm_registry"]
except ImportError:
    __all_algorithms__ = []

try:
    from .api import run_server
    __all_api__ = ["run_server"] 
except ImportError:
    __all_api__ = []

__all__ = [
    # Core validators
    "QuantumValidator",
    "BiologicalValidator", 
    "HolographicValidator",
    
    # Main engine
    "QBHValidationEngine",
    "ValidationMode",
    "ValidationResult",
    
    # Configuration
    "ValidationConfig",
    "QuantumConfig", 
    "BiologicalConfig",
    "HolographicConfig",
    
    # Monitoring
    "PerformanceMonitor",
    "AdaptiveThresholdMonitor", 
    
    # Extensions
    "PluginManager",
    "plugin_manager",
    "MLBiologicalValidator",
    "EvolutionaryOptimizer"
] + __all_algorithms__ + __all_api__