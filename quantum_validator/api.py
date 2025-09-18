"""
REST API Server for QBH Validation Engine

Following Protocol 03: Secure Code Implementation
This module provides a REST API interface for the quantum-validator.
"""

from typing import Any, Dict, List, Optional
import json
import logging
from datetime import datetime
from dataclasses import asdict
import asyncio
import uuid

try:
    from fastapi import FastAPI, HTTPException, Depends, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field, validator
    import uvicorn
    import importlib.util
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


# Request/Response models
if FASTAPI_AVAILABLE:
    class ValidationRequest(BaseModel):
        """Request model for validation endpoint."""
        data: Any = Field(..., description="Data to validate")
        validation_schema: Optional[Dict[str, Any]] = Field(None, description="Optional validation schema")
        mode: str = Field("hybrid", description="Validation mode", pattern="^(classical|quantum|bio|holographic|hybrid)$")
        enable_monitoring: bool = Field(True, description="Enable performance monitoring")
        
        class Config:
            json_schema_extra = {
                "example": {
                    "data": {"transaction_id": "txn_001", "amount": 1500.00},
                    "validation_schema": {"required_fields": ["transaction_id", "amount"]},
                    "mode": "hybrid",
                    "enable_monitoring": True
                }
            }


    class ValidationResponse(BaseModel):
        """Response model for validation endpoint."""
        request_id: str
        is_valid: bool
        confidence_score: float
        quantum_coherence: Optional[float] = None
        biological_resilience: Optional[float] = None
        holographic_integrity: Optional[float] = None
        validation_path: List[str]
        processing_time_ms: float
        mode: str
        error_details: Optional[Dict[str, Any]] = None
        
        class Config:
            json_schema_extra = {
                "example": {
                    "request_id": "req_123456",
                    "is_valid": True,
                    "confidence_score": 0.892,
                    "quantum_coherence": 0.815,
                    "biological_resilience": 0.923,
                    "holographic_integrity": 0.867,
                    "validation_path": ["QBH_ENGINE_START", "CLASSICAL_VALIDATION", "QUANTUM_VALIDATION"],
                    "processing_time_ms": 125.3,
                    "mode": "hybrid"
                }
            }


    class HealthResponse(BaseModel):
        """Response model for health check endpoint."""
        status: str
        timestamp: str
        version: str
        quantum_backend_available: bool
        ml_backend_available: bool
        active_validations: int
        total_validations: int


    class PerformanceResponse(BaseModel):
        """Response model for performance metrics endpoint."""
        total_validations: int
        successful_validations: int
        failed_validations: int
        success_rate: float
        average_duration_ms: float
        average_confidence: float
        mode_distribution: Dict[str, int]


# Initialize FastAPI app
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="QBH Validation Engine API",
        description="REST API for Quantum-Biological Holographic Validation Engine",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Global validation engine and monitor
    from quantum_validator.validation_engine import QBHValidationEngine, ValidationMode
    from quantum_validator.monitoring import PerformanceMonitor
    from quantum_validator import __version__
    
    validation_engine = None
    performance_monitor = None
    active_validations = {}
    
    def get_validation_engine():
        """Dependency to get validation engine."""
        global validation_engine
        if validation_engine is None:
            validation_engine = QBHValidationEngine(
                mode=ValidationMode.HYBRID,
                enable_logging=True
            )
        return validation_engine
    
    def get_performance_monitor():
        """Dependency to get performance monitor."""
        global performance_monitor
        if performance_monitor is None:
            performance_monitor = PerformanceMonitor(
                max_history=10000,
                enable_real_time_alerts=True
            )
        return performance_monitor
    
    
    @app.post("/validate", response_model=ValidationResponse)
    async def validate_data(
        request: ValidationRequest,
        engine: QBHValidationEngine = Depends(get_validation_engine),
        monitor: PerformanceMonitor = Depends(get_performance_monitor)
    ):
        """
        Validate data using QBH validation engine.
        
        Performs quantum-biological-holographic validation on the provided data
        and returns comprehensive validation results with confidence metrics.
        """
        request_id = str(uuid.uuid4())[:8]
        start_time = datetime.now()
        
        try:
            # Map mode string to enum
            mode_mapping = {
                'classical': ValidationMode.CLASSICAL,
                'quantum': ValidationMode.QUANTUM_ENHANCED,
                'bio': ValidationMode.BIO_INSPIRED,
                'holographic': ValidationMode.HOLOGRAPHIC,
                'hybrid': ValidationMode.HYBRID
            }
            
            validation_mode = mode_mapping[request.mode]
            
            # Start performance monitoring
            data_size = len(json.dumps(request.data, default=str).encode('utf-8'))
            if request.enable_monitoring:
                metrics = monitor.start_validation(request_id, request.mode, data_size)
            
            # Update engine mode if different
            if engine.mode != validation_mode:
                engine.mode = validation_mode
            
            # Perform validation
            result = engine.validate(request.data, schema=request.schema)
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Finish performance monitoring
            if request.enable_monitoring:
                monitor.finish_validation(request_id, result)
            
            # Build response
            response = ValidationResponse(
                request_id=request_id,
                is_valid=result.is_valid,
                confidence_score=result.confidence_score,
                quantum_coherence=result.quantum_coherence,
                biological_resilience=result.biological_resilience,
                holographic_integrity=result.holographic_integrity,
                validation_path=result.validation_path or [],
                processing_time_ms=processing_time_ms,
                mode=request.mode,
                error_details=result.error_details
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Validation request {request_id} failed: {e}")
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
    
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check(
        monitor: PerformanceMonitor = Depends(get_performance_monitor)
    ):
        """
        Health check endpoint.
        
        Returns system health status and basic metrics.
        """
        try:
            stats = monitor.get_performance_stats()
            
            return HealthResponse(
                status="healthy",
                timestamp=datetime.now().isoformat(),
                version=__version__,
                quantum_backend_available=True,  # Would check actual backend
                ml_backend_available=True,       # Would check ML backend
                active_validations=len(active_validations),
                total_validations=stats.total_validations
            )
            
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return HealthResponse(
                status="unhealthy",
                timestamp=datetime.now().isoformat(),
                version=__version__,
                quantum_backend_available=False,
                ml_backend_available=False,
                active_validations=0,
                total_validations=0
            )
    
    
    @app.get("/metrics", response_model=PerformanceResponse)
    async def get_performance_metrics(
        monitor: PerformanceMonitor = Depends(get_performance_monitor)
    ):
        """
        Get performance metrics.
        
        Returns detailed performance statistics for the validation engine.
        """
        try:
            stats = monitor.get_performance_stats()
            
            success_rate = 0.0
            if stats.total_validations > 0:
                success_rate = stats.successful_validations / stats.total_validations
            
            return PerformanceResponse(
                total_validations=stats.total_validations,
                successful_validations=stats.successful_validations,
                failed_validations=stats.failed_validations,
                success_rate=success_rate,
                average_duration_ms=stats.average_duration_ms,
                average_confidence=stats.average_confidence,
                mode_distribution=dict(stats.mode_distribution)
            )
            
        except Exception as e:
            logging.error(f"Metrics request failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")
    
    
    @app.get("/metrics/report")
    async def get_performance_report(
        monitor: PerformanceMonitor = Depends(get_performance_monitor)
    ):
        """
        Get detailed performance report.
        
        Returns human-readable performance report with insights.
        """
        try:
            report = monitor.generate_performance_report()
            return {"report": report}
            
        except Exception as e:
            logging.error(f"Performance report failed: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
    
    
    @app.post("/validate/batch")
    async def validate_batch(
        requests: List[ValidationRequest],
        engine: QBHValidationEngine = Depends(get_validation_engine),
        monitor: PerformanceMonitor = Depends(get_performance_monitor)
    ):
        """
        Batch validation endpoint.
        
        Validates multiple data items in a single request for efficiency.
        """
        if len(requests) > 100:  # Limit batch size for security
            raise HTTPException(status_code=400, detail="Batch size exceeds maximum of 100")
        
        results = []
        
        for i, req in enumerate(requests):
            try:
                # Create individual request ID
                request_id = f"batch_{uuid.uuid4().hex[:8]}_{i}"
                
                # Perform validation (reuse single endpoint logic)
                individual_result = await validate_data(req, engine, monitor)
                individual_result.request_id = request_id
                
                results.append(individual_result)
                
            except Exception as e:
                # Include error in batch results
                error_result = ValidationResponse(
                    request_id=f"batch_error_{i}",
                    is_valid=False,
                    confidence_score=0.0,
                    validation_path=["BATCH_ERROR"],
                    processing_time_ms=0.0,
                    mode=req.mode,
                    error_details={"error": str(e)}
                )
                results.append(error_result)
        
        return {"batch_results": results}
    
    
    def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        """
        Run the QBH validation API server.
        
        Args:
            host: Host address to bind to
            port: Port number to listen on
            reload: Enable auto-reload for development
        """
        if not FASTAPI_AVAILABLE:
            raise RuntimeError("FastAPI not available. Install with: pip install fastapi uvicorn")
        
        logging.info(f"Starting QBH Validation API server on {host}:{port}")
        
        uvicorn.run(
            "quantum_validator.api:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )

else:
    # Stub implementations when FastAPI not available
    def run_server(*args, **kwargs):
        raise RuntimeError("FastAPI not available. Install with: pip install fastapi uvicorn")
    
    app = None