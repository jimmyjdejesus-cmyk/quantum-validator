"""
Configuration management for QBH Validation Engine

Following Protocol 03: Secure Code Implementation
This module provides configuration management for the quantum-validator.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
import os


@dataclass
class QuantumConfig:
    """Configuration for quantum validation components."""
    backend: str = "qiskit_aer"
    num_qubits: int = 4
    shots: int = 1000
    coherence_threshold: float = 0.8
    fidelity_threshold: float = 0.85
    enable_noise_simulation: bool = False
    quantum_volume: int = 16


@dataclass 
class BiologicalConfig:
    """Configuration for biological validation components."""
    immune_sensitivity: float = 0.1
    neural_layers: int = 3
    population_size: int = 50
    mutation_rate: float = 0.01
    selection_pressure: float = 0.8
    swarm_size: int = 20
    learning_rate: float = 0.01
    memory_size: int = 100


@dataclass
class HolographicConfig:
    """Configuration for holographic validation components."""
    dimensions: int = 8
    redundancy_factor: float = 3.0
    reconstruction_threshold: float = 0.85
    basis_seed: int = 42
    max_data_vector_size: int = 64
    fragment_overlap_threshold: float = 0.7


@dataclass
class ValidationConfig:
    """Master configuration for QBH Validation Engine."""
    quantum: QuantumConfig = field(default_factory=QuantumConfig)
    biological: BiologicalConfig = field(default_factory=BiologicalConfig)
    holographic: HolographicConfig = field(default_factory=HolographicConfig)
    
    # General settings
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_performance_monitoring: bool = True
    cache_validation_results: bool = False
    max_cache_size: int = 1000
    
    # Security settings
    max_input_size: int = 10_000_000  # 10MB
    max_processing_time: int = 300  # 5 minutes
    enable_input_sanitization: bool = True
    
    # Quality settings
    min_confidence_threshold: float = 0.5
    consensus_threshold: float = 0.5
    enable_hybrid_weighting: bool = True
    
    @classmethod
    def from_file(cls, config_path: str) -> 'ValidationConfig':
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            ValidationConfig instance
        """
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls.from_dict(config_data)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ValidationConfig':
        """Create configuration from dictionary."""
        config = cls()
        
        # Update quantum config
        if 'quantum' in config_dict:
            for key, value in config_dict['quantum'].items():
                if hasattr(config.quantum, key):
                    setattr(config.quantum, key, value)
        
        # Update biological config  
        if 'biological' in config_dict:
            for key, value in config_dict['biological'].items():
                if hasattr(config.biological, key):
                    setattr(config.biological, key, value)
        
        # Update holographic config
        if 'holographic' in config_dict:
            for key, value in config_dict['holographic'].items():
                if hasattr(config.holographic, key):
                    setattr(config.holographic, key, value)
        
        # Update general settings
        for key, value in config_dict.items():
            if key not in ['quantum', 'biological', 'holographic'] and hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    @classmethod
    def from_environment(cls) -> 'ValidationConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Quantum settings
        config.quantum.backend = os.getenv('QBH_QUANTUM_BACKEND', config.quantum.backend)
        config.quantum.num_qubits = int(os.getenv('QBH_QUANTUM_QUBITS', config.quantum.num_qubits))
        config.quantum.shots = int(os.getenv('QBH_QUANTUM_SHOTS', config.quantum.shots))
        
        # Biological settings
        config.biological.population_size = int(os.getenv('QBH_BIO_POPULATION', config.biological.population_size))
        config.biological.mutation_rate = float(os.getenv('QBH_BIO_MUTATION_RATE', config.biological.mutation_rate))
        
        # Holographic settings
        config.holographic.dimensions = int(os.getenv('QBH_HOLO_DIMENSIONS', config.holographic.dimensions))
        config.holographic.redundancy_factor = float(os.getenv('QBH_HOLO_REDUNDANCY', config.holographic.redundancy_factor))
        
        # General settings
        config.enable_logging = os.getenv('QBH_ENABLE_LOGGING', 'true').lower() == 'true'
        config.log_level = os.getenv('QBH_LOG_LEVEL', config.log_level)
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'quantum': {
                'backend': self.quantum.backend,
                'num_qubits': self.quantum.num_qubits,
                'shots': self.quantum.shots,
                'coherence_threshold': self.quantum.coherence_threshold,
                'fidelity_threshold': self.quantum.fidelity_threshold,
                'enable_noise_simulation': self.quantum.enable_noise_simulation,
                'quantum_volume': self.quantum.quantum_volume
            },
            'biological': {
                'immune_sensitivity': self.biological.immune_sensitivity,
                'neural_layers': self.biological.neural_layers,
                'population_size': self.biological.population_size,
                'mutation_rate': self.biological.mutation_rate,
                'selection_pressure': self.biological.selection_pressure,
                'swarm_size': self.biological.swarm_size,
                'learning_rate': self.biological.learning_rate,
                'memory_size': self.biological.memory_size
            },
            'holographic': {
                'dimensions': self.holographic.dimensions,
                'redundancy_factor': self.holographic.redundancy_factor,
                'reconstruction_threshold': self.holographic.reconstruction_threshold,
                'basis_seed': self.holographic.basis_seed,
                'max_data_vector_size': self.holographic.max_data_vector_size,
                'fragment_overlap_threshold': self.holographic.fragment_overlap_threshold
            },
            'enable_logging': self.enable_logging,
            'log_level': self.log_level,
            'enable_performance_monitoring': self.enable_performance_monitoring,
            'cache_validation_results': self.cache_validation_results,
            'max_cache_size': self.max_cache_size,
            'max_input_size': self.max_input_size,
            'max_processing_time': self.max_processing_time,
            'enable_input_sanitization': self.enable_input_sanitization,
            'min_confidence_threshold': self.min_confidence_threshold,
            'consensus_threshold': self.consensus_threshold,
            'enable_hybrid_weighting': self.enable_hybrid_weighting
        }
    
    def save_to_file(self, config_path: str) -> None:
        """Save configuration to JSON file."""
        config_dict = self.to_dict()
        
        # Create directory if it doesn't exist
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration settings and return any issues.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Validate quantum config
        if self.quantum.num_qubits < 1 or self.quantum.num_qubits > 20:
            issues.append("Quantum qubits must be between 1 and 20")
        
        if self.quantum.shots < 100 or self.quantum.shots > 100000:
            issues.append("Quantum shots must be between 100 and 100,000")
        
        # Validate biological config
        if self.biological.population_size < 10 or self.biological.population_size > 1000:
            issues.append("Biological population size must be between 10 and 1,000")
        
        if not 0.0 <= self.biological.mutation_rate <= 1.0:
            issues.append("Biological mutation rate must be between 0.0 and 1.0")
        
        # Validate holographic config
        if self.holographic.dimensions < 2 or self.holographic.dimensions > 16:
            issues.append("Holographic dimensions must be between 2 and 16")
        
        if self.holographic.redundancy_factor < 1.0 or self.holographic.redundancy_factor > 10.0:
            issues.append("Holographic redundancy factor must be between 1.0 and 10.0")
        
        # Validate general settings
        if not 0.0 <= self.min_confidence_threshold <= 1.0:
            issues.append("Minimum confidence threshold must be between 0.0 and 1.0")
        
        if self.max_input_size < 1000:
            issues.append("Maximum input size must be at least 1,000 bytes")
        
        return issues