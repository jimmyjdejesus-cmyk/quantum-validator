"""
Performance Monitoring for QBH Validation Engine

Following Protocol 05: Systematic Debugging & Root Cause Analysis
This module provides comprehensive performance monitoring and metrics collection.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import logging
from collections import defaultdict, deque
import threading
import json
import numpy as np


@dataclass
class ValidationMetrics:
    """Metrics for a single validation operation."""
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    validation_mode: str = ""
    data_size_bytes: int = 0
    is_valid: bool = False
    confidence_score: float = 0.0
    quantum_coherence: Optional[float] = None
    biological_resilience: Optional[float] = None
    holographic_integrity: Optional[float] = None
    error_type: Optional[str] = None
    validation_path: List[str] = field(default_factory=list)
    
    def finalize(self, end_time: datetime) -> None:
        """Finalize metrics calculation."""
        self.end_time = end_time
        if self.start_time:
            delta = end_time - self.start_time
            self.duration_ms = delta.total_seconds() * 1000


@dataclass
class PerformanceStats:
    """Aggregated performance statistics."""
    total_validations: int = 0
    successful_validations: int = 0
    failed_validations: int = 0
    average_duration_ms: float = 0.0
    average_confidence: float = 0.0
    mode_distribution: Dict[str, int] = field(default_factory=dict)
    error_distribution: Dict[str, int] = field(default_factory=dict)
    quantum_coherence_avg: Optional[float] = None
    biological_resilience_avg: Optional[float] = None
    holographic_integrity_avg: Optional[float] = None


class PerformanceMonitor:
    """
    Performance monitoring system for validation operations.
    
    Tracks validation performance, identifies bottlenecks, and provides
    insights for optimization using bio-inspired adaptive monitoring.
    """
    
    def __init__(self, 
                 max_history: int = 10000,
                 enable_real_time_alerts: bool = True,
                 alert_threshold_ms: float = 5000.0):
        """
        Initialize performance monitor.
        
        Args:
            max_history: Maximum number of metrics to keep in memory
            enable_real_time_alerts: Enable real-time performance alerts
            alert_threshold_ms: Threshold for slow validation alerts (ms)
        """
        self.max_history = max_history
        self.enable_real_time_alerts = enable_real_time_alerts
        self.alert_threshold_ms = alert_threshold_ms
        
        # Thread-safe metrics storage
        self._lock = threading.Lock()
        self._metrics_history: deque = deque(maxlen=max_history)
        self._current_validations: Dict[str, ValidationMetrics] = {}
        
        # Performance tracking
        self._stats_cache: Optional[PerformanceStats] = None
        self._last_stats_update = datetime.now()
        self._stats_cache_ttl = timedelta(seconds=30)
        
        self.logger = logging.getLogger("PerformanceMonitor")
        self.logger.info("Performance monitor initialized")
    
    def start_validation(self, 
                        validation_id: str,
                        mode: str,
                        data_size: int) -> ValidationMetrics:
        """
        Start tracking a validation operation.
        
        Args:
            validation_id: Unique identifier for this validation
            mode: Validation mode being used
            data_size: Size of data being validated (bytes)
            
        Returns:
            ValidationMetrics object for this operation
        """
        metrics = ValidationMetrics(
            start_time=datetime.now(),
            validation_mode=mode,
            data_size_bytes=data_size
        )
        
        with self._lock:
            self._current_validations[validation_id] = metrics
        
        self.logger.debug(f"Started tracking validation {validation_id} in {mode} mode")
        return metrics
    
    def finish_validation(self, 
                         validation_id: str,
                         result: Any) -> Optional[ValidationMetrics]:
        """
        Finish tracking a validation operation.
        
        Args:
            validation_id: Unique identifier for this validation
            result: ValidationResult object
            
        Returns:
            Completed ValidationMetrics or None if not found
        """
        with self._lock:
            if validation_id not in self._current_validations:
                self.logger.warning(f"Validation {validation_id} not found in tracking")
                return None
            
            metrics = self._current_validations.pop(validation_id)
            
            # Update metrics with result data
            end_time = datetime.now()
            metrics.finalize(end_time)
            metrics.is_valid = result.is_valid
            metrics.confidence_score = result.confidence_score
            metrics.quantum_coherence = result.quantum_coherence
            metrics.biological_resilience = result.biological_resilience
            metrics.holographic_integrity = result.holographic_integrity
            metrics.validation_path = result.validation_path or []
            
            if hasattr(result, 'error_details') and result.error_details:
                metrics.error_type = result.error_details.get('type', 'unknown')
            
            # Add to history
            self._metrics_history.append(metrics)
            
            # Clear stats cache
            self._stats_cache = None
            
            # Check for performance alerts
            if self.enable_real_time_alerts and metrics.duration_ms:
                self._check_performance_alerts(metrics)
            
            self.logger.debug(f"Finished tracking validation {validation_id}: {metrics.duration_ms:.2f}ms")
            return metrics
    
    def get_performance_stats(self, 
                            time_window: Optional[timedelta] = None) -> PerformanceStats:
        """
        Get aggregated performance statistics.
        
        Args:
            time_window: Optional time window for stats (default: all time)
            
        Returns:
            PerformanceStats with aggregated metrics
        """
        # Check cache
        now = datetime.now()
        if (self._stats_cache and 
            now - self._last_stats_update < self._stats_cache_ttl and
            time_window is None):
            return self._stats_cache
        
        with self._lock:
            # Filter metrics by time window
            if time_window:
                cutoff_time = now - time_window
                relevant_metrics = [
                    m for m in self._metrics_history 
                    if m.start_time >= cutoff_time
                ]
            else:
                relevant_metrics = list(self._metrics_history)
            
            if not relevant_metrics:
                return PerformanceStats()
            
            # Calculate statistics
            stats = PerformanceStats()
            stats.total_validations = len(relevant_metrics)
            stats.successful_validations = sum(1 for m in relevant_metrics if m.is_valid)
            stats.failed_validations = stats.total_validations - stats.successful_validations
            
            # Duration statistics
            durations = [m.duration_ms for m in relevant_metrics if m.duration_ms is not None]
            stats.average_duration_ms = sum(durations) / len(durations) if durations else 0.0
            
            # Confidence statistics
            confidences = [m.confidence_score for m in relevant_metrics]
            stats.average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Mode distribution
            stats.mode_distribution = defaultdict(int)
            for m in relevant_metrics:
                stats.mode_distribution[m.validation_mode] += 1
            
            # Error distribution
            stats.error_distribution = defaultdict(int)
            for m in relevant_metrics:
                if m.error_type:
                    stats.error_distribution[m.error_type] += 1
            
            # Advanced metrics averages
            quantum_coherences = [m.quantum_coherence for m in relevant_metrics if m.quantum_coherence is not None]
            stats.quantum_coherence_avg = sum(quantum_coherences) / len(quantum_coherences) if quantum_coherences else None
            
            bio_resiliences = [m.biological_resilience for m in relevant_metrics if m.biological_resilience is not None]
            stats.biological_resilience_avg = sum(bio_resiliences) / len(bio_resiliences) if bio_resiliences else None
            
            holo_integrities = [m.holographic_integrity for m in relevant_metrics if m.holographic_integrity is not None]
            stats.holographic_integrity_avg = sum(holo_integrities) / len(holo_integrities) if holo_integrities else None
            
            # Cache results
            if time_window is None:
                self._stats_cache = stats
                self._last_stats_update = now
            
            return stats
    
    def get_recent_validations(self, count: int = 10) -> List[ValidationMetrics]:
        """Get most recent validation metrics."""
        with self._lock:
            return list(self._metrics_history)[-count:]
    
    def get_slow_validations(self, threshold_ms: float = None) -> List[ValidationMetrics]:
        """Get validations that exceeded performance thresholds."""
        if threshold_ms is None:
            threshold_ms = self.alert_threshold_ms
        
        with self._lock:
            return [
                m for m in self._metrics_history 
                if m.duration_ms and m.duration_ms > threshold_ms
            ]
    
    def export_metrics(self, file_path: str, format: str = 'json') -> None:
        """
        Export metrics to file.
        
        Args:
            file_path: Path to export file
            format: Export format ('json', 'csv')
        """
        with self._lock:
            metrics_data = []
            
            for m in self._metrics_history:
                metric_dict = {
                    'start_time': m.start_time.isoformat(),
                    'end_time': m.end_time.isoformat() if m.end_time else None,
                    'duration_ms': m.duration_ms,
                    'validation_mode': m.validation_mode,
                    'data_size_bytes': m.data_size_bytes,
                    'is_valid': m.is_valid,
                    'confidence_score': m.confidence_score,
                    'quantum_coherence': m.quantum_coherence,
                    'biological_resilience': m.biological_resilience,
                    'holographic_integrity': m.holographic_integrity,
                    'error_type': m.error_type,
                    'validation_path': m.validation_path
                }
                metrics_data.append(metric_dict)
        
        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(metrics_data, f, indent=2)
        elif format == 'csv':
            # Simple CSV export
            import csv
            with open(file_path, 'w', newline='') as f:
                if metrics_data:
                    writer = csv.DictWriter(f, fieldnames=metrics_data[0].keys())
                    writer.writeheader()
                    writer.writerows(metrics_data)
        
        self.logger.info(f"Exported {len(metrics_data)} metrics to {file_path}")
    
    def _check_performance_alerts(self, metrics: ValidationMetrics) -> None:
        """Check for performance alerts and log warnings."""
        if metrics.duration_ms and metrics.duration_ms > self.alert_threshold_ms:
            self.logger.warning(
                f"Slow validation detected: {metrics.duration_ms:.2f}ms "
                f"(threshold: {self.alert_threshold_ms:.2f}ms) "
                f"in {metrics.validation_mode} mode"
            )
        
        if metrics.confidence_score < 0.3:
            self.logger.warning(
                f"Low confidence validation: {metrics.confidence_score:.3f} "
                f"in {metrics.validation_mode} mode"
            )
        
        if metrics.quantum_coherence and metrics.quantum_coherence < 0.5:
            self.logger.warning(
                f"Low quantum coherence: {metrics.quantum_coherence:.3f}"
            )
    
    def generate_performance_report(self, time_window: Optional[timedelta] = None) -> str:
        """
        Generate human-readable performance report.
        
        Args:
            time_window: Optional time window for report
            
        Returns:
            Formatted performance report
        """
        stats = self.get_performance_stats(time_window)
        
        lines = []
        lines.append("🔬 QBH Validation Engine Performance Report")
        lines.append("=" * 60)
        
        # Basic statistics
        lines.append(f"📊 Total Validations: {stats.total_validations}")
        lines.append(f"✅ Successful: {stats.successful_validations}")
        lines.append(f"❌ Failed: {stats.failed_validations}")
        
        if stats.total_validations > 0:
            success_rate = stats.successful_validations / stats.total_validations * 100
            lines.append(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Performance metrics
        lines.append(f"\n⚡ Performance Metrics:")
        lines.append(f"   Average Duration: {stats.average_duration_ms:.2f}ms")
        lines.append(f"   Average Confidence: {stats.average_confidence:.3f}")
        
        # Advanced metrics
        if stats.quantum_coherence_avg is not None:
            lines.append(f"   Avg Quantum Coherence: {stats.quantum_coherence_avg:.3f}")
        
        if stats.biological_resilience_avg is not None:
            lines.append(f"   Avg Biological Resilience: {stats.biological_resilience_avg:.3f}")
        
        if stats.holographic_integrity_avg is not None:
            lines.append(f"   Avg Holographic Integrity: {stats.holographic_integrity_avg:.3f}")
        
        # Mode distribution
        if stats.mode_distribution:
            lines.append(f"\n🎯 Validation Mode Usage:")
            for mode, count in sorted(stats.mode_distribution.items()):
                percentage = count / stats.total_validations * 100
                lines.append(f"   {mode}: {count} ({percentage:.1f}%)")
        
        # Error analysis
        if stats.error_distribution:
            lines.append(f"\n🚨 Error Distribution:")
            for error_type, count in sorted(stats.error_distribution.items()):
                percentage = count / stats.total_validations * 100
                lines.append(f"   {error_type}: {count} ({percentage:.1f}%)")
        
        # Performance insights
        lines.append(f"\n💡 Performance Insights:")
        
        if stats.average_duration_ms > 1000:
            lines.append("   ⚠️  Average validation time exceeds 1 second")
        else:
            lines.append("   ✅ Good average validation performance")
        
        if stats.average_confidence < 0.7:
            lines.append("   ⚠️  Average confidence below 70% - consider tuning parameters")
        else:
            lines.append("   ✅ Good average confidence levels")
        
        # Recent performance trends
        recent_metrics = self.get_recent_validations(50)
        if len(recent_metrics) >= 10:
            recent_durations = [m.duration_ms for m in recent_metrics[-10:] if m.duration_ms]
            older_durations = [m.duration_ms for m in recent_metrics[-20:-10] if m.duration_ms]
            
            if recent_durations and older_durations:
                recent_avg = sum(recent_durations) / len(recent_durations)
                older_avg = sum(older_durations) / len(older_durations)
                
                if recent_avg > older_avg * 1.2:
                    lines.append("   📈 Performance degradation detected in recent validations")
                elif recent_avg < older_avg * 0.8:
                    lines.append("   📉 Performance improvement detected in recent validations")
                else:
                    lines.append("   📊 Stable performance in recent validations")
        
        return '\n'.join(lines)


class AdaptiveThresholdMonitor:
    """
    Adaptive threshold monitoring using bio-inspired algorithms.
    
    Automatically adjusts performance thresholds based on system behavior
    using biological adaptation principles.
    """
    
    def __init__(self, 
                 initial_threshold: float = 1000.0,
                 adaptation_rate: float = 0.1,
                 stability_window: int = 100):
        """
        Initialize adaptive threshold monitor.
        
        Args:
            initial_threshold: Initial performance threshold (ms)
            adaptation_rate: Rate of threshold adaptation (0.0-1.0)
            stability_window: Number of samples for stability calculation
        """
        self.current_threshold = initial_threshold
        self.adaptation_rate = adaptation_rate
        self.stability_window = stability_window
        
        self._performance_history: deque = deque(maxlen=stability_window)
        self._threshold_history: deque = deque(maxlen=100)
        
        self.logger = logging.getLogger("AdaptiveThresholdMonitor")
    
    def update_threshold(self, new_performance_sample: float) -> float:
        """
        Update threshold based on new performance sample.
        
        Args:
            new_performance_sample: New performance measurement (ms)
            
        Returns:
            Updated threshold value
        """
        self._performance_history.append(new_performance_sample)
        
        if len(self._performance_history) < 10:
            # Need more samples for adaptation
            return self.current_threshold
        
        # Calculate performance statistics
        recent_avg = sum(list(self._performance_history)[-10:]) / 10
        overall_avg = sum(self._performance_history) / len(self._performance_history)
        performance_variance = np.var(list(self._performance_history))
        
        # Adaptive threshold calculation using bio-inspired rules
        # Similar to how biological systems adapt to environmental changes
        
        # If recent performance is consistently worse, raise threshold
        if recent_avg > overall_avg * 1.3:
            adaptation = self.adaptation_rate * (recent_avg - self.current_threshold)
            new_threshold = self.current_threshold + adaptation
        
        # If recent performance is consistently better, lower threshold
        elif recent_avg < overall_avg * 0.7:
            adaptation = self.adaptation_rate * (self.current_threshold - recent_avg)
            new_threshold = self.current_threshold - adaptation
        
        # If performance is stable, make small adjustments toward average
        else:
            target_threshold = overall_avg * 1.5  # 50% above average as reasonable threshold
            adaptation = self.adaptation_rate * (target_threshold - self.current_threshold)
            new_threshold = self.current_threshold + adaptation
        
        # Ensure threshold stays within reasonable bounds
        new_threshold = max(100.0, min(30000.0, new_threshold))  # 100ms to 30s bounds
        
        # Update threshold
        old_threshold = self.current_threshold
        self.current_threshold = new_threshold
        self._threshold_history.append(new_threshold)
        
        self.logger.debug(f"Adapted threshold: {old_threshold:.2f}ms -> {new_threshold:.2f}ms")
        
        return new_threshold
    
    def get_threshold_stability(self) -> float:
        """
        Calculate threshold stability metric.
        
        Returns:
            Stability score (0.0-1.0, higher = more stable)
        """
        if len(self._threshold_history) < 10:
            return 1.0  # Assume stable with insufficient data
        
        # Calculate coefficient of variation for recent thresholds
        recent_thresholds = list(self._threshold_history)[-20:]
        mean_threshold = sum(recent_thresholds) / len(recent_thresholds)
        threshold_variance = sum((t - mean_threshold)**2 for t in recent_thresholds) / len(recent_thresholds)
        coefficient_of_variation = (threshold_variance**0.5) / mean_threshold if mean_threshold > 0 else 1.0
        
        # Convert to stability score (lower variation = higher stability)
        stability = max(0.0, 1.0 - coefficient_of_variation)
        
        return stability