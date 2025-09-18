"""
Biological Validator - Bio-Inspired Validation Algorithms

Implements validation patterns inspired by biological systems such as
immune system recognition, neural network validation, and evolutionary algorithms.
"""

from typing import Any, Dict, Optional, List, Tuple
import numpy as np
from dataclasses import dataclass
import logging
import random
from collections import defaultdict


@dataclass 
class BiologicalValidationResult:
    """Result from bio-inspired validation."""
    is_valid: bool
    confidence_score: float
    biological_resilience: float
    immune_response: Optional[float] = None
    evolutionary_fitness: Optional[float] = None
    validation_path: List[str] = None
    
    def __post_init__(self):
        if self.validation_path is None:
            self.validation_path = []


class BiologicalValidator:
    """
    Bio-inspired validator using biological system patterns.
    
    This validator implements biological validation strategies:
    - Immune system-like pattern recognition
    - Neural network-inspired validation
    - Evolutionary algorithm fitness scoring
    - Swarm intelligence consensus validation
    """
    
    def __init__(self, 
                 immune_sensitivity: float = 0.1,
                 neural_layers: int = 3,
                 population_size: int = 50):
        """
        Initialize biological validator.
        
        Args:
            immune_sensitivity: Sensitivity threshold for immune system detection
            neural_layers: Number of neural network layers for validation
            population_size: Population size for evolutionary validation
        """
        self.immune_sensitivity = immune_sensitivity
        self.neural_layers = neural_layers
        self.population_size = population_size
        self.logger = logging.getLogger("BiologicalValidator")
        
        # Initialize biological components
        self.immune_memory = []  # Known patterns
        self.neural_weights = self._initialize_neural_network()
        self.evolutionary_population = []
        
        self.logger.info("Biological validator initialized with bio-inspired algorithms")
    
    def validate(self, 
                 data: Any, 
                 schema: Optional[Dict[str, Any]] = None) -> BiologicalValidationResult:
        """
        Perform bio-inspired validation.
        
        Args:
            data: Data to validate using biological methods
            schema: Validation schema (optional)
            
        Returns:
            BiologicalValidationResult with biological metrics
        """
        self.logger.info("Starting biological validation")
        
        try:
            validation_path = ["BIO_START"]
            
            # Phase 1: Immune system validation
            immune_result = self._immune_system_validation(data, schema)
            validation_path.append("IMMUNE_SYSTEM")
            
            # Phase 2: Neural network validation
            neural_result = self._neural_network_validation(data, schema)
            validation_path.append("NEURAL_NETWORK")
            
            # Phase 3: Evolutionary algorithm validation
            evolutionary_result = self._evolutionary_validation(data, schema)
            validation_path.append("EVOLUTIONARY")
            
            # Phase 4: Swarm intelligence consensus
            swarm_result = self._swarm_consensus_validation(data, schema)
            validation_path.append("SWARM_CONSENSUS")
            
            # Synthesize biological validation results
            final_result = self._synthesize_biological_results(
                immune_result, neural_result, evolutionary_result, swarm_result
            )
            final_result.validation_path = validation_path
            
            self.logger.info(f"Biological validation completed with resilience: {final_result.biological_resilience}")
            return final_result
            
        except Exception as e:
            self.logger.error(f"Biological validation failed: {str(e)}")
            return BiologicalValidationResult(
                is_valid=False,
                confidence_score=0.0,
                biological_resilience=0.0,
                validation_path=["BIO_ERROR"]
            )
    
    def _immune_system_validation(self, 
                                data: Any, 
                                schema: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Immune system-inspired validation using pattern recognition.
        
        Mimics how biological immune systems recognize self vs non-self patterns.
        """
        # Extract features from data
        features = self._extract_biological_features(data)
        
        # Check against immune memory (known good patterns)
        self_recognition_score = 0.0
        if self.immune_memory:
            similarities = [
                self._calculate_pattern_similarity(features, memory_pattern)
                for memory_pattern in self.immune_memory
            ]
            self_recognition_score = max(similarities) if similarities else 0.0
        
        # Calculate immune response (higher = more foreign/potentially invalid)
        immune_response = 1.0 - self_recognition_score
        
        # Validation decision based on immune response
        is_self_pattern = immune_response < self.immune_sensitivity
        confidence = 1.0 - immune_response if is_self_pattern else immune_response
        
        # Update immune memory with new valid patterns
        if is_self_pattern and features not in self.immune_memory:
            self.immune_memory.append(features)
            # Limit memory size (like biological immune system)
            if len(self.immune_memory) > 100:
                self.immune_memory.pop(0)
        
        return {
            'is_valid': is_self_pattern,
            'confidence': confidence,
            'immune_response': immune_response
        }
    
    def _neural_network_validation(self, 
                                 data: Any, 
                                 schema: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Neural network-inspired validation using pattern learning.
        """
        # Convert data to neural network input
        input_vector = self._data_to_neural_input(data)
        
        # Forward pass through biological neural network
        activation = input_vector
        for layer_weights in self.neural_weights:
            # Apply weights and activation function (sigmoid)
            activation = self._sigmoid(np.dot(activation, layer_weights))
        
        # Output interpretation (last neuron output as validity score)
        validity_score = activation[-1] if len(activation) > 0 else 0.5
        
        # Adaptive learning: adjust weights based on validation result
        self._adapt_neural_weights(input_vector, validity_score)
        
        return {
            'is_valid': validity_score > 0.5,
            'confidence': abs(validity_score - 0.5) * 2,  # Distance from decision boundary
            'neural_activation': validity_score
        }
    
    def _evolutionary_validation(self, 
                               data: Any, 
                               schema: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Evolutionary algorithm-inspired validation using fitness scoring.
        """
        # Generate population of validation hypotheses
        population = self._generate_validation_population(data, schema)
        
        # Evaluate fitness of each hypothesis
        fitness_scores = [
            self._calculate_validation_fitness(hypothesis, data, schema)
            for hypothesis in population
        ]
        
        # Select best hypotheses (natural selection)
        best_fitness = max(fitness_scores) if fitness_scores else 0.0
        average_fitness = np.mean(fitness_scores) if fitness_scores else 0.0
        
        # Evolve population for next validation (mutation and crossover)
        self._evolve_population(population, fitness_scores)
        
        return {
            'is_valid': best_fitness > 0.7,
            'confidence': best_fitness,
            'evolutionary_fitness': average_fitness
        }
    
    def _swarm_consensus_validation(self, 
                                  data: Any, 
                                  schema: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Swarm intelligence-inspired consensus validation.
        
        Mimics how biological swarms reach consensus decisions.
        """
        # Generate swarm of validation agents
        swarm_size = 20
        swarm_opinions = []
        
        for _ in range(swarm_size):
            # Each agent makes independent validation decision
            agent_opinion = self._agent_validation_opinion(data, schema)
            swarm_opinions.append(agent_opinion)
        
        # Calculate swarm consensus
        positive_votes = sum(1 for opinion in swarm_opinions if opinion > 0.5)
        consensus_strength = positive_votes / swarm_size
        
        # Confidence based on agreement level
        agreement_variance = np.var(swarm_opinions)
        confidence = 1.0 - agreement_variance  # Higher agreement = higher confidence
        
        return {
            'is_valid': consensus_strength > 0.5,
            'confidence': confidence,
            'consensus_strength': consensus_strength
        }
    
    def _extract_biological_features(self, data: Any) -> List[float]:
        """Extract biological-style features from data."""
        features = []
        
        if isinstance(data, str):
            # String features: length, character diversity, pattern regularity
            features.extend([
                len(data) / 100.0,  # Normalized length
                len(set(data)) / max(len(data), 1),  # Character diversity
                self._calculate_pattern_regularity(data)
            ])
        elif isinstance(data, (int, float)):
            # Numeric features: magnitude, sign, fractional part
            features.extend([
                abs(data) / 1000.0,  # Normalized magnitude
                1.0 if data >= 0 else 0.0,  # Sign
                abs(data) % 1  # Fractional part
            ])
        elif isinstance(data, (list, dict)):
            # Collection features: size, complexity, depth
            features.extend([
                len(str(data)) / 1000.0,  # Serialized length
                self._calculate_structural_complexity(data),
                self._calculate_nesting_depth(data)
            ])
        else:
            # Default features for unknown types
            features = [0.5, 0.5, 0.5]
        
        # Ensure consistent feature vector length
        while len(features) < 10:
            features.append(0.0)
        
        return features[:10]  # Limit to 10 features
    
    def _calculate_pattern_similarity(self, features1: List[float], features2: List[float]) -> float:
        """Calculate similarity between two feature patterns."""
        if not features1 or not features2:
            return 0.0
        
        # Euclidean distance-based similarity
        distance = np.sqrt(sum((a - b)**2 for a, b in zip(features1, features2)))
        similarity = 1.0 / (1.0 + distance)  # Convert distance to similarity
        
        return similarity
    
    def _initialize_neural_network(self) -> List[np.ndarray]:
        """Initialize neural network weights for biological validation."""
        layers = []
        input_size = 10  # Feature vector size
        
        # Create layers with decreasing size
        layer_sizes = [input_size]
        for i in range(self.neural_layers):
            next_size = max(1, input_size // (2 ** (i + 1)))
            layer_sizes.append(next_size)
        
        # Initialize weights between layers
        for i in range(len(layer_sizes) - 1):
            weights = np.random.normal(0, 0.1, (layer_sizes[i], layer_sizes[i + 1]))
            layers.append(weights)
        
        return layers
    
    def _data_to_neural_input(self, data: Any) -> np.ndarray:
        """Convert data to neural network input vector."""
        features = self._extract_biological_features(data)
        return np.array(features)
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
    
    def _adapt_neural_weights(self, input_vector: np.ndarray, validity_score: float):
        """Adapt neural network weights based on validation feedback."""
        # Simple Hebbian learning rule adaptation
        learning_rate = 0.01
        
        # Reinforce weights that led to correct decisions
        if len(self.neural_weights) > 0:
            # Adjust first layer weights based on input pattern
            adjustment = learning_rate * validity_score * np.outer(input_vector, np.ones(self.neural_weights[0].shape[1]))
            self.neural_weights[0] += adjustment * 0.1  # Small adaptation
    
    def _generate_validation_population(self, data: Any, schema: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate population of validation hypotheses."""
        population = []
        
        for _ in range(self.population_size):
            hypothesis = {
                'threshold': random.uniform(0.1, 0.9),
                'feature_weights': [random.uniform(0, 1) for _ in range(10)],
                'validation_strategy': random.choice(['strict', 'lenient', 'adaptive'])
            }
            population.append(hypothesis)
        
        return population
    
    def _calculate_validation_fitness(self, hypothesis: Dict[str, Any], data: Any, schema: Optional[Dict[str, Any]]) -> float:
        """Calculate fitness score for validation hypothesis."""
        features = self._extract_biological_features(data)
        
        # Apply hypothesis weights to features
        weighted_score = sum(f * w for f, w in zip(features, hypothesis['feature_weights']))
        normalized_score = weighted_score / (sum(hypothesis['feature_weights']) + 1e-10)
        
        # Apply threshold strategy
        if hypothesis['validation_strategy'] == 'strict':
            fitness = 1.0 if normalized_score > hypothesis['threshold'] * 1.2 else 0.0
        elif hypothesis['validation_strategy'] == 'lenient':
            fitness = 1.0 if normalized_score > hypothesis['threshold'] * 0.8 else 0.0
        else:  # adaptive
            fitness = max(0.0, min(1.0, normalized_score))
        
        return fitness
    
    def _evolve_population(self, population: List[Dict[str, Any]], fitness_scores: List[float]):
        """Evolve population using mutation and crossover."""
        # Simple evolutionary update
        if not fitness_scores:
            return
        
        # Keep best performers
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
        elite_size = max(1, len(population) // 4)
        
        # Mutate elite individuals
        for i in range(elite_size):
            individual = population[sorted_indices[i]]
            # Small mutations
            individual['threshold'] += random.uniform(-0.1, 0.1)
            individual['threshold'] = max(0.1, min(0.9, individual['threshold']))
            
            for j in range(len(individual['feature_weights'])):
                individual['feature_weights'][j] += random.uniform(-0.1, 0.1)
                individual['feature_weights'][j] = max(0.0, min(1.0, individual['feature_weights'][j]))
    
    def _agent_validation_opinion(self, data: Any, schema: Optional[Dict[str, Any]]) -> float:
        """Generate individual swarm agent validation opinion."""
        features = self._extract_biological_features(data)
        
        # Each agent uses slightly different validation criteria
        agent_threshold = random.uniform(0.3, 0.7)
        feature_importance = [random.uniform(0.5, 1.5) for _ in range(len(features))]
        
        # Calculate weighted opinion
        weighted_sum = sum(f * w for f, w in zip(features, feature_importance))
        normalized_opinion = weighted_sum / (sum(feature_importance) + 1e-10)
        
        return 1.0 if normalized_opinion > agent_threshold else 0.0
    
    def _synthesize_biological_results(self, 
                                     immune_result: Dict[str, float],
                                     neural_result: Dict[str, float], 
                                     evolutionary_result: Dict[str, float],
                                     swarm_result: Dict[str, float]) -> BiologicalValidationResult:
        """Synthesize all biological validation results."""
        
        # Combine validity decisions using biological consensus
        validity_votes = [
            immune_result['is_valid'],
            neural_result['is_valid'],
            evolutionary_result['is_valid'],
            swarm_result['is_valid']
        ]
        
        # Majority consensus with confidence weighting
        positive_votes = sum(validity_votes)
        is_valid = positive_votes >= 2  # Majority rule
        
        # Weighted confidence score
        confidence_scores = [
            immune_result['confidence'],
            neural_result['confidence'], 
            evolutionary_result['confidence'],
            swarm_result['confidence']
        ]
        
        # Calculate biological resilience as system redundancy
        system_agreement = sum(1 for vote in validity_votes if vote == is_valid) / len(validity_votes)
        biological_resilience = system_agreement * np.mean(confidence_scores)
        
        return BiologicalValidationResult(
            is_valid=is_valid,
            confidence_score=np.mean(confidence_scores),
            biological_resilience=biological_resilience,
            immune_response=immune_result['immune_response'],
            evolutionary_fitness=evolutionary_result['evolutionary_fitness']
        )
    
    def _calculate_pattern_regularity(self, text: str) -> float:
        """Calculate pattern regularity in text."""
        if len(text) < 2:
            return 0.5
        
        # Simple regularity measure based on character transitions
        transitions = defaultdict(int)
        for i in range(len(text) - 1):
            transitions[text[i:i+2]] += 1
        
        # More regular patterns have fewer unique transitions
        regularity = 1.0 - (len(transitions) / max(len(text) - 1, 1))
        return max(0.0, min(1.0, regularity))
    
    def _calculate_structural_complexity(self, obj: Any) -> float:
        """Calculate structural complexity of an object."""
        try:
            str_repr = str(obj)
            # Count nesting indicators
            nesting_chars = str_repr.count('{') + str_repr.count('[') + str_repr.count('(')
            complexity = min(1.0, nesting_chars / 20.0)  # Normalize to 0-1
            return complexity
        except:
            return 0.5
    
    def _calculate_nesting_depth(self, obj: Any, current_depth: int = 0) -> float:
        """Calculate maximum nesting depth of an object."""
        if current_depth > 10:  # Prevent infinite recursion
            return 10.0
        
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._calculate_nesting_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, (list, tuple)):
            if not obj:
                return current_depth
            return max(self._calculate_nesting_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth