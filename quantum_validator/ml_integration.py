"""
Machine Learning Integration for Bio-Inspired Validation

Following Protocol 03: Secure Code Implementation
This module provides ML-enhanced biological validation algorithms.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
from dataclasses import dataclass
import logging
from abc import ABC, abstractmethod

try:
    from sklearn.ensemble import IsolationForest, RandomForestClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


@dataclass
class MLValidationResult:
    """Result from machine learning validation."""
    algorithm_name: str
    is_valid: bool
    confidence: float
    ml_confidence: float
    anomaly_score: Optional[float] = None
    cluster_info: Optional[Dict[str, Any]] = None
    feature_importance: Optional[List[float]] = None


class MLBiologicalValidator:
    """
    Machine learning enhanced biological validator.
    
    Integrates classical ML algorithms with bio-inspired validation
    to provide adaptive and learning-based validation capabilities.
    """
    
    def __init__(self, 
                 enable_anomaly_detection: bool = True,
                 enable_clustering: bool = True,
                 enable_neural_classification: bool = True):
        """
        Initialize ML biological validator.
        
        Args:
            enable_anomaly_detection: Enable isolation forest anomaly detection
            enable_clustering: Enable DBSCAN clustering analysis
            enable_neural_classification: Enable neural network classification
        """
        self.enable_anomaly_detection = enable_anomaly_detection
        self.enable_clustering = enable_clustering
        self.enable_neural_classification = enable_neural_classification
        
        self.logger = logging.getLogger("MLBiologicalValidator")
        
        # Initialize ML models
        self._anomaly_detector = None
        self._clusterer = None
        self._neural_classifier = None
        self._scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        
        # Training data storage
        self._training_features: List[np.ndarray] = []
        self._training_labels: List[bool] = []
        
        self._initialize_models()
    
    def validate_with_ml(self, 
                        data: Any, 
                        schema: Optional[Dict[str, Any]] = None,
                        update_models: bool = True) -> MLValidationResult:
        """
        Validate data using ML-enhanced biological algorithms.
        
        Args:
            data: Data to validate
            schema: Optional validation schema
            update_models: Whether to update models with this validation
            
        Returns:
            MLValidationResult with ML-specific metrics
        """
        try:
            if not SKLEARN_AVAILABLE:
                return self._classical_ml_fallback(data)
            
            # Extract features for ML analysis
            features = self._extract_ml_features(data)
            
            # Normalize features
            if self._scaler and len(self._training_features) > 0:
                features_scaled = self._scaler.transform([features])[0]
            else:
                features_scaled = features
            
            # Run ML validation algorithms
            results = {}
            
            if self.enable_anomaly_detection:
                results['anomaly'] = self._anomaly_detection_validation(features_scaled)
            
            if self.enable_clustering:
                results['clustering'] = self._clustering_validation(features_scaled)
            
            if self.enable_neural_classification:
                results['neural'] = self._neural_classification_validation(features_scaled)
            
            # Synthesize ML results
            final_result = self._synthesize_ml_results(results, features)
            
            # Update models if requested and result is reliable
            if update_models and final_result.confidence > 0.7:
                self._update_models(features, final_result.is_valid)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"ML validation failed: {e}")
            return MLValidationResult(
                algorithm_name="ML_Biological_Error",
                is_valid=False,
                confidence=0.0,
                ml_confidence=0.0
            )
    
    def _initialize_models(self) -> None:
        """Initialize ML models."""
        if not SKLEARN_AVAILABLE:
            self.logger.warning("scikit-learn not available, ML features disabled")
            return
        
        if self.enable_anomaly_detection:
            self._anomaly_detector = IsolationForest(
                contamination=0.1,  # Expect 10% anomalies
                random_state=42,
                n_estimators=100
            )
        
        if self.enable_clustering:
            self._clusterer = DBSCAN(
                eps=0.5,
                min_samples=5
            )
        
        if self.enable_neural_classification:
            self._neural_classifier = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42,
                early_stopping=True
            )
        
        self.logger.info("ML models initialized")
    
    def _extract_ml_features(self, data: Any) -> np.ndarray:
        """Extract features suitable for ML algorithms."""
        features = []
        
        # Basic statistical features
        data_str = str(data)
        features.extend([
            len(data_str),  # Length
            len(set(data_str)),  # Unique characters
            data_str.count(' '),  # Space count
            data_str.count(','),  # Comma count
            data_str.count('{'),  # Opening braces
            data_str.count('}'),  # Closing braces
        ])
        
        # Numerical features if applicable
        if isinstance(data, (int, float)):
            features.extend([
                float(data),
                abs(data),
                np.sign(data),
                data % 1 if isinstance(data, float) else 0
            ])
        elif isinstance(data, (list, tuple)):
            numeric_items = [x for x in data if isinstance(x, (int, float))]
            if numeric_items:
                features.extend([
                    np.mean(numeric_items),
                    np.std(numeric_items),
                    np.min(numeric_items),
                    np.max(numeric_items)
                ])
            else:
                features.extend([0, 0, 0, 0])
        else:
            features.extend([0, 0, 0, 0])
        
        # Structural features
        features.extend([
            str(data).count('\n'),  # Line count
            self._calculate_entropy(data_str),  # Information entropy
            self._calculate_complexity_score(data),  # Structural complexity
        ])
        
        # Ensure consistent feature vector length
        while len(features) < 20:
            features.append(0.0)
        
        return np.array(features[:20])
    
    def _anomaly_detection_validation(self, features: np.ndarray) -> Dict[str, Any]:
        """Perform anomaly detection validation."""
        if self._anomaly_detector is None:
            return {'is_valid': True, 'confidence': 0.5, 'anomaly_score': 0.0}
        
        try:
            # Predict anomaly
            prediction = self._anomaly_detector.predict([features])[0]
            anomaly_score = self._anomaly_detector.decision_function([features])[0]
            
            # Convert to validation result
            is_valid = prediction == 1  # 1 = normal, -1 = anomaly
            confidence = abs(anomaly_score)  # Higher absolute score = higher confidence
            
            return {
                'is_valid': is_valid,
                'confidence': min(confidence, 1.0),
                'anomaly_score': anomaly_score
            }
            
        except Exception as e:
            self.logger.error(f"Anomaly detection failed: {e}")
            return {'is_valid': True, 'confidence': 0.5, 'anomaly_score': 0.0}
    
    def _clustering_validation(self, features: np.ndarray) -> Dict[str, Any]:
        """Perform clustering-based validation."""
        if self._clusterer is None or len(self._training_features) < 10:
            return {'is_valid': True, 'confidence': 0.5}
        
        try:
            # Combine with training features for clustering
            all_features = np.vstack([self._training_features, [features]])
            
            # Perform clustering
            cluster_labels = self._clusterer.fit_predict(all_features)
            
            # Analyze clustering result for validation
            data_cluster = cluster_labels[-1]  # Cluster of current data
            cluster_info = self._analyze_cluster_assignment(cluster_labels, data_cluster)
            
            return cluster_info
            
        except Exception as e:
            self.logger.error(f"Clustering validation failed: {e}")
            return {'is_valid': True, 'confidence': 0.5}
    
    def _neural_classification_validation(self, features: np.ndarray) -> Dict[str, Any]:
        """Perform neural network classification validation."""
        if (self._neural_classifier is None or 
            len(self._training_features) < 20 or 
            len(set(self._training_labels)) < 2):
            return {'is_valid': True, 'confidence': 0.5}
        
        try:
            # Predict using trained neural network
            prediction_proba = self._neural_classifier.predict_proba([features])[0]
            prediction = self._neural_classifier.predict([features])[0]
            
            # Extract confidence from probability
            confidence = max(prediction_proba)
            is_valid = bool(prediction)
            
            return {
                'is_valid': is_valid,
                'confidence': confidence,
                'prediction_probabilities': prediction_proba.tolist()
            }
            
        except Exception as e:
            self.logger.error(f"Neural classification failed: {e}")
            return {'is_valid': True, 'confidence': 0.5}
    
    def _synthesize_ml_results(self, 
                              results: Dict[str, Dict[str, Any]], 
                              features: np.ndarray) -> MLValidationResult:
        """Synthesize results from all ML algorithms."""
        
        # Collect validity decisions and confidences
        validities = []
        confidences = []
        anomaly_score = None
        cluster_info = None
        
        for algorithm, result in results.items():
            validities.append(result['is_valid'])
            confidences.append(result['confidence'])
            
            if algorithm == 'anomaly':
                anomaly_score = result.get('anomaly_score')
            elif algorithm == 'clustering':
                cluster_info = result
        
        # Calculate consensus
        validity_consensus = sum(validities) / len(validities) if validities else 0.5
        is_valid = validity_consensus >= 0.5
        
        # Calculate combined confidence
        ml_confidence = np.mean(confidences) if confidences else 0.5
        
        # Adjust confidence based on consensus strength
        consensus_strength = 1.0 - abs(validity_consensus - 0.5) * 2  # 0-1 scale
        final_confidence = ml_confidence * consensus_strength
        
        return MLValidationResult(
            algorithm_name="ML_Biological_Synthesis",
            is_valid=is_valid,
            confidence=final_confidence,
            ml_confidence=ml_confidence,
            anomaly_score=anomaly_score,
            cluster_info=cluster_info
        )
    
    def _update_models(self, features: np.ndarray, is_valid: bool) -> None:
        """Update ML models with new training data."""
        # Add to training data
        self._training_features.append(features)
        self._training_labels.append(is_valid)
        
        # Limit training data size
        max_training_size = 1000
        if len(self._training_features) > max_training_size:
            self._training_features = self._training_features[-max_training_size:]
            self._training_labels = self._training_labels[-max_training_size:]
        
        # Retrain models periodically
        if len(self._training_features) % 50 == 0:  # Every 50 samples
            self._retrain_models()
    
    def _retrain_models(self) -> None:
        """Retrain ML models with accumulated data."""
        if not SKLEARN_AVAILABLE or len(self._training_features) < 10:
            return
        
        try:
            features_array = np.vstack(self._training_features)
            labels_array = np.array(self._training_labels)
            
            # Fit scaler
            self._scaler.fit(features_array)
            features_scaled = self._scaler.transform(features_array)
            
            # Retrain anomaly detector
            if self._anomaly_detector:
                self._anomaly_detector.fit(features_scaled)
            
            # Retrain neural classifier if we have both classes
            if self._neural_classifier and len(set(labels_array)) >= 2:
                self._neural_classifier.fit(features_scaled, labels_array)
            
            self.logger.info(f"Retrained ML models with {len(self._training_features)} samples")
            
        except Exception as e:
            self.logger.error(f"Model retraining failed: {e}")
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        if not text:
            return 0.0
        
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        text_length = len(text)
        entropy = 0.0
        
        for count in char_counts.values():
            probability = count / text_length
            if probability > 0:
                entropy -= probability * np.log2(probability)
        
        return entropy
    
    def _calculate_complexity_score(self, data: Any) -> float:
        """Calculate structural complexity score."""
        data_str = str(data)
        
        # Factors contributing to complexity
        nesting_chars = data_str.count('{') + data_str.count('[') + data_str.count('(')
        separators = data_str.count(',') + data_str.count(';') + data_str.count(':')
        quotes = data_str.count('"') + data_str.count("'")
        
        # Normalize complexity score
        complexity = (nesting_chars * 2 + separators + quotes * 0.5) / max(len(data_str), 1)
        
        return min(1.0, complexity)
    
    def _analyze_cluster_assignment(self, cluster_labels: np.ndarray, data_cluster: int) -> Dict[str, Any]:
        """Analyze cluster assignment for validation."""
        unique_clusters = set(cluster_labels)
        cluster_sizes = {cluster: np.sum(cluster_labels == cluster) for cluster in unique_clusters}
        
        # Validation based on cluster characteristics
        is_noise = data_cluster == -1  # DBSCAN noise label
        
        if is_noise:
            is_valid = False
            confidence = 0.2
        else:
            cluster_size = cluster_sizes.get(data_cluster, 0)
            total_points = len(cluster_labels)
            
            # Larger clusters indicate more normal patterns
            cluster_proportion = cluster_size / total_points
            is_valid = cluster_proportion > 0.05  # At least 5% of data in cluster
            confidence = min(cluster_proportion * 5, 1.0)  # Scale to confidence
        
        return {
            'is_valid': is_valid,
            'confidence': confidence,
            'cluster_id': data_cluster,
            'cluster_size': cluster_sizes.get(data_cluster, 0),
            'is_noise': is_noise,
            'total_clusters': len(unique_clusters)
        }
    
    def _classical_ml_fallback(self, data: Any) -> MLValidationResult:
        """Classical fallback when ML libraries unavailable."""
        # Simple heuristic-based validation
        data_str = str(data)
        
        # Basic validation heuristics
        is_valid = len(data_str) > 0 and not data_str.isspace()
        confidence = 0.6 if is_valid else 0.2
        
        return MLValidationResult(
            algorithm_name="ML_Classical_Fallback",
            is_valid=is_valid,
            confidence=confidence,
            ml_confidence=confidence
        )


class EvolutionaryOptimizer:
    """
    Evolutionary algorithm optimizer for validation parameters.
    
    Uses genetic algorithms to optimize validation parameters
    and discover optimal validation strategies.
    """
    
    def __init__(self, 
                 population_size: int = 50,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8,
                 max_generations: int = 100):
        """Initialize evolutionary optimizer."""
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations
        
        self.logger = logging.getLogger("EvolutionaryOptimizer")
        
        # Current population of validation strategies
        self.population: List[Dict[str, Any]] = []
        self.fitness_history: List[List[float]] = []
    
    def optimize_validation_parameters(self, 
                                     training_data: List[Tuple[Any, bool]],
                                     validation_function: callable) -> Dict[str, Any]:
        """
        Optimize validation parameters using evolutionary algorithms.
        
        Args:
            training_data: List of (data, expected_validity) tuples
            validation_function: Function to evaluate validation strategies
            
        Returns:
            Best validation parameters found
        """
        try:
            # Initialize population
            self._initialize_population()
            
            best_strategy = None
            best_fitness = -1.0
            
            for generation in range(self.max_generations):
                # Evaluate fitness for each strategy
                fitness_scores = []
                
                for strategy in self.population:
                    fitness = self._evaluate_strategy_fitness(
                        strategy, training_data, validation_function
                    )
                    fitness_scores.append(fitness)
                    
                    # Track best strategy
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_strategy = strategy.copy()
                
                # Record fitness history
                self.fitness_history.append(fitness_scores.copy())
                
                # Evolve population
                self.population = self._evolve_population(self.population, fitness_scores)
                
                # Early stopping if converged
                if generation > 10 and self._has_converged():
                    self.logger.info(f"Evolutionary optimization converged at generation {generation}")
                    break
            
            self.logger.info(f"Evolutionary optimization completed. Best fitness: {best_fitness:.3f}")
            
            return best_strategy or {}
            
        except Exception as e:
            self.logger.error(f"Evolutionary optimization failed: {e}")
            return {}
    
    def _initialize_population(self) -> None:
        """Initialize population of validation strategies."""
        self.population = []
        
        for _ in range(self.population_size):
            strategy = {
                'confidence_threshold': np.random.uniform(0.1, 0.9),
                'ensemble_weight_quantum': np.random.uniform(0.5, 2.0),
                'ensemble_weight_biological': np.random.uniform(0.5, 2.0),
                'ensemble_weight_holographic': np.random.uniform(0.5, 2.0),
                'consensus_threshold': np.random.uniform(0.3, 0.8),
                'anomaly_sensitivity': np.random.uniform(0.05, 0.3),
                'neural_learning_rate': np.random.uniform(0.001, 0.1),
                'quantum_coherence_weight': np.random.uniform(0.1, 1.0),
                'biological_resilience_weight': np.random.uniform(0.1, 1.0),
                'holographic_integrity_weight': np.random.uniform(0.1, 1.0)
            }
            self.population.append(strategy)
    
    def _evaluate_strategy_fitness(self, 
                                  strategy: Dict[str, Any],
                                  training_data: List[Tuple[Any, bool]],
                                  validation_function: callable) -> float:
        """Evaluate fitness of a validation strategy."""
        if not training_data:
            return 0.0
        
        correct_predictions = 0
        total_confidence = 0.0
        
        for data, expected_valid in training_data:
            try:
                # Apply strategy to validation function
                result = validation_function(data, strategy)
                
                # Check correctness
                if result.get('is_valid', False) == expected_valid:
                    correct_predictions += 1
                
                # Accumulate confidence
                total_confidence += result.get('confidence', 0.0)
                
            except Exception:
                # Strategy caused error, penalize fitness
                continue
        
        # Calculate fitness as combination of accuracy and confidence
        accuracy = correct_predictions / len(training_data)
        average_confidence = total_confidence / len(training_data)
        
        fitness = 0.7 * accuracy + 0.3 * average_confidence
        
        return fitness
    
    def _evolve_population(self, 
                          population: List[Dict[str, Any]], 
                          fitness_scores: List[float]) -> List[Dict[str, Any]]:
        """Evolve population using selection, crossover, and mutation."""
        new_population = []
        
        # Sort by fitness
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
        
        # Elitism: keep best 20%
        elite_count = max(1, int(0.2 * self.population_size))
        for i in range(elite_count):
            new_population.append(population[sorted_indices[i]].copy())
        
        # Generate rest through crossover and mutation
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            if np.random.random() < self.crossover_rate:
                child = self._crossover(parent1, parent2)
            else:
                child = parent1.copy()
            
            # Mutation
            if np.random.random() < self.mutation_rate:
                child = self._mutate(child)
            
            new_population.append(child)
        
        return new_population
    
    def _tournament_selection(self, 
                             population: List[Dict[str, Any]], 
                             fitness_scores: List[float],
                             tournament_size: int = 3) -> Dict[str, Any]:
        """Select individual using tournament selection."""
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        return population[winner_index].copy()
    
    def _crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Perform crossover between two parents."""
        child = {}
        
        for key in parent1.keys():
            # Random choice between parents for each parameter
            if np.random.random() < 0.5:
                child[key] = parent1[key]
            else:
                child[key] = parent2[key]
        
        return child
    
    def _mutate(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate individual parameters."""
        mutated = individual.copy()
        
        for key, value in mutated.items():
            if np.random.random() < 0.1:  # 10% chance per parameter
                # Apply small random mutation
                if isinstance(value, float):
                    mutation = np.random.normal(0, 0.1 * value)
                    mutated[key] = max(0.01, value + mutation)  # Ensure positive
        
        return mutated
    
    def _has_converged(self) -> bool:
        """Check if population has converged."""
        if len(self.fitness_history) < 10:
            return False
        
        # Check if fitness improvement has stagnated
        recent_best = [max(generation) for generation in self.fitness_history[-10:]]
        improvement = recent_best[-1] - recent_best[0]
        
        return improvement < 0.01  # Less than 1% improvement over 10 generations