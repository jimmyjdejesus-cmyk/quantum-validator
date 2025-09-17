"""
Command Line Interface for QBH Validation Engine

Following Protocol 03: Secure Code Implementation
This module provides a command-line interface for the quantum-validator.
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .validation_engine import QBHValidationEngine, ValidationMode


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for CLI usage."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_data_from_file(file_path: str) -> Any:
    """
    Load data from various file formats.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        Loaded data object
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    suffix = path.suffix.lower()
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if suffix == '.json':
                return json.load(f)
            elif suffix in ['.txt', '.csv']:
                return f.read()
            else:
                # Try to parse as JSON first, then fall back to text
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content
    except Exception as e:
        raise ValueError(f"Failed to load data from {file_path}: {e}")


def load_schema_from_file(file_path: str) -> Dict[str, Any]:
    """
    Load validation schema from JSON file.
    
    Args:
        file_path: Path to the schema file
        
    Returns:
        Schema dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            if not isinstance(schema, dict):
                raise ValueError("Schema must be a JSON object")
            return schema
    except Exception as e:
        raise ValueError(f"Failed to load schema from {file_path}: {e}")


def format_validation_result(result, output_format: str = 'text') -> str:
    """
    Format validation result for output.
    
    Args:
        result: ValidationResult object
        output_format: Output format ('text', 'json', 'compact')
        
    Returns:
        Formatted result string
    """
    if output_format == 'json':
        result_dict = {
            'is_valid': result.is_valid,
            'confidence_score': result.confidence_score,
            'quantum_coherence': result.quantum_coherence,
            'biological_resilience': result.biological_resilience,
            'holographic_integrity': result.holographic_integrity,
            'validation_path': result.validation_path,
            'error_details': result.error_details
        }
        return json.dumps(result_dict, indent=2)
    
    elif output_format == 'compact':
        status = "VALID" if result.is_valid else "INVALID"
        return f"{status} (confidence: {result.confidence_score:.3f})"
    
    else:  # text format
        lines = []
        lines.append("🔬 QBH Validation Results")
        lines.append("=" * 40)
        lines.append(f"✅ Valid: {result.is_valid}")
        lines.append(f"🎯 Confidence: {result.confidence_score:.3f}")
        
        if result.quantum_coherence is not None:
            lines.append(f"⚛️  Quantum Coherence: {result.quantum_coherence:.3f}")
        
        if result.biological_resilience is not None:
            lines.append(f"🧬 Biological Resilience: {result.biological_resilience:.3f}")
        
        if result.holographic_integrity is not None:
            lines.append(f"🌐 Holographic Integrity: {result.holographic_integrity:.3f}")
        
        if result.validation_path:
            lines.append(f"🛤️  Path: {' → '.join(result.validation_path)}")
        
        if result.error_details:
            lines.append(f"❌ Errors: {result.error_details}")
        
        return '\n'.join(lines)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quantum-Biological Holographic (QBH) Validation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate JSON data in hybrid mode
  qbh-validate --data data.json --mode hybrid
  
  # Validate with schema and custom output
  qbh-validate --data input.json --schema schema.json --output json
  
  # Quantum-enhanced validation with verbose logging
  qbh-validate --data scientific_data.json --mode quantum --verbose
  
  # Bio-inspired validation from stdin
  echo '{"test": "data"}' | qbh-validate --mode bio
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--data', '-d',
        type=str,
        help="Path to data file (JSON, text, or CSV)"
    )
    input_group.add_argument(
        '--stdin',
        action='store_true',
        help="Read data from standard input"
    )
    
    # Validation options
    parser.add_argument(
        '--mode', '-m',
        type=str,
        choices=['classical', 'quantum', 'bio', 'holographic', 'hybrid'],
        default='hybrid',
        help="Validation mode (default: hybrid)"
    )
    
    parser.add_argument(
        '--schema', '-s',
        type=str,
        help="Path to validation schema file (JSON)"
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        choices=['text', 'json', 'compact'],
        default='text',
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        '--output-file', '-f',
        type=str,
        help="Write output to file instead of stdout"
    )
    
    # General options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        '--quantum-backend',
        type=str,
        default='qiskit_aer',
        help="Quantum computing backend (default: qiskit_aer)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Load data
        if args.stdin:
            logger.info("Reading data from stdin...")
            data_content = sys.stdin.read()
            try:
                data = json.loads(data_content)
            except json.JSONDecodeError:
                data = data_content
        else:
            logger.info(f"Loading data from {args.data}...")
            data = load_data_from_file(args.data)
        
        # Load schema if provided
        schema = None
        if args.schema:
            logger.info(f"Loading schema from {args.schema}...")
            schema = load_schema_from_file(args.schema)
        
        # Map mode names to enum values
        mode_mapping = {
            'classical': ValidationMode.CLASSICAL,
            'quantum': ValidationMode.QUANTUM_ENHANCED,
            'bio': ValidationMode.BIO_INSPIRED,
            'holographic': ValidationMode.HOLOGRAPHIC,
            'hybrid': ValidationMode.HYBRID
        }
        
        validation_mode = mode_mapping[args.mode]
        
        # Initialize validation engine
        logger.info(f"Initializing QBH Validation Engine in {args.mode} mode...")
        engine = QBHValidationEngine(
            mode=validation_mode,
            quantum_backend=args.quantum_backend,
            enable_logging=args.verbose
        )
        
        # Perform validation
        logger.info("Starting validation process...")
        result = engine.validate(data, schema=schema)
        
        # Format output
        output = format_validation_result(result, args.output)
        
        # Write output
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            logger.info(f"Results written to {args.output_file}")
        else:
            print(output)
        
        # Return exit code based on validation result
        return 0 if result.is_valid else 1
        
    except KeyboardInterrupt:
        logger.error("Validation interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())