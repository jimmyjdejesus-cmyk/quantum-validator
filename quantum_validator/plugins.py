"""
Plugin system for QBH Validation Engine

Following Protocol 02: System Design & Architecture
This module provides extensible plugin architecture for custom validators.
"""

from typing import Any, Dict, List, Optional, Type, Protocol
from abc import ABC, abstractmethod
import logging
import importlib
import inspect
from pathlib import Path


class ValidationPlugin(Protocol):
    """Protocol for validation plugins."""
    
    def validate(self, data: Any, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate data and return result dictionary."""
        ...
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Return plugin information."""
        ...


class PluginManager:
    """
    Plugin manager for extending QBH validation capabilities.
    
    Allows loading custom validation algorithms and integrating
    them with the core validation engine.
    """
    
    def __init__(self):
        self.plugins: Dict[str, ValidationPlugin] = {}
        self.plugin_metadata: Dict[str, Dict[str, str]] = {}
        self.logger = logging.getLogger("PluginManager")
        
        self.logger.info("Plugin manager initialized")
    
    def register_plugin(self, name: str, plugin: ValidationPlugin) -> bool:
        """
        Register a validation plugin.
        
        Args:
            name: Unique name for the plugin
            plugin: Plugin instance implementing ValidationPlugin protocol
            
        Returns:
            True if successful, False if registration failed
        """
        try:
            # Validate plugin interface
            if not self._validate_plugin_interface(plugin):
                self.logger.error(f"Plugin {name} does not implement required interface")
                return False
            
            # Get plugin metadata
            metadata = plugin.get_plugin_info()
            
            # Register plugin
            self.plugins[name] = plugin
            self.plugin_metadata[name] = metadata
            
            self.logger.info(f"Successfully registered plugin: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register plugin {name}: {e}")
            return False
    
    def unregister_plugin(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self.plugins:
            del self.plugins[name]
            del self.plugin_metadata[name]
            self.logger.info(f"Unregistered plugin: {name}")
            return True
        return False
    
    def execute_plugin(self, 
                      name: str, 
                      data: Any, 
                      schema: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a specific plugin.
        
        Args:
            name: Plugin name
            data: Data to validate
            schema: Optional validation schema
            
        Returns:
            Plugin result or None if plugin not found
        """
        if name not in self.plugins:
            self.logger.error(f"Plugin not found: {name}")
            return None
        
        try:
            plugin = self.plugins[name]
            result = plugin.validate(data, schema)
            
            self.logger.debug(f"Plugin {name} executed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Plugin {name} execution failed: {e}")
            return {
                'is_valid': False,
                'error': str(e),
                'plugin_name': name
            }
    
    def execute_all_plugins(self, 
                           data: Any, 
                           schema: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Execute all registered plugins.
        
        Args:
            data: Data to validate
            schema: Optional validation schema
            
        Returns:
            Dictionary of plugin results keyed by plugin name
        """
        results = {}
        
        for name in self.plugins:
            result = self.execute_plugin(name, data, schema)
            results[name] = result
        
        return results
    
    def load_plugin_from_file(self, file_path: str, class_name: str) -> bool:
        """
        Load plugin from Python file.
        
        Args:
            file_path: Path to Python file containing plugin
            class_name: Name of plugin class
            
        Returns:
            True if loaded successfully
        """
        try:
            # Load module from file
            spec = importlib.util.spec_from_file_location("plugin_module", file_path)
            if spec is None or spec.loader is None:
                self.logger.error(f"Could not load module from {file_path}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin class
            if not hasattr(module, class_name):
                self.logger.error(f"Class {class_name} not found in {file_path}")
                return False
            
            plugin_class = getattr(module, class_name)
            
            # Instantiate plugin
            plugin_instance = plugin_class()
            
            # Register plugin
            plugin_name = f"{Path(file_path).stem}_{class_name}"
            return self.register_plugin(plugin_name, plugin_instance)
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin from {file_path}: {e}")
            return False
    
    def discover_plugins(self, plugin_directory: str) -> int:
        """
        Discover and load plugins from directory.
        
        Args:
            plugin_directory: Directory to search for plugins
            
        Returns:
            Number of plugins loaded
        """
        plugin_path = Path(plugin_directory)
        if not plugin_path.exists():
            self.logger.warning(f"Plugin directory not found: {plugin_directory}")
            return 0
        
        loaded_count = 0
        
        # Search for Python files
        for py_file in plugin_path.glob("*.py"):
            if py_file.stem.startswith("plugin_"):
                # Try to load plugin classes from file
                try:
                    spec = importlib.util.spec_from_file_location("plugin_module", py_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Find classes that implement ValidationPlugin
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if self._implements_validation_plugin(obj) and name != 'ValidationPlugin':
                                plugin_instance = obj()
                                plugin_name = f"{py_file.stem}_{name}"
                                if self.register_plugin(plugin_name, plugin_instance):
                                    loaded_count += 1
                                    
                except Exception as e:
                    self.logger.error(f"Failed to load plugin from {py_file}: {e}")
        
        self.logger.info(f"Discovered and loaded {loaded_count} plugins from {plugin_directory}")
        return loaded_count
    
    def get_plugin_info(self, name: str) -> Optional[Dict[str, str]]:
        """Get metadata for a specific plugin."""
        return self.plugin_metadata.get(name)
    
    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        return list(self.plugins.keys())
    
    def get_plugin_summary(self) -> Dict[str, Dict[str, str]]:
        """Get summary of all registered plugins."""
        summary = {}
        for name, metadata in self.plugin_metadata.items():
            summary[name] = {
                'name': metadata.get('name', name),
                'version': metadata.get('version', 'unknown'),
                'description': metadata.get('description', 'No description'),
                'author': metadata.get('author', 'Unknown')
            }
        return summary
    
    def _validate_plugin_interface(self, plugin: Any) -> bool:
        """Validate that plugin implements required interface."""
        required_methods = ['validate', 'get_plugin_info']
        
        for method in required_methods:
            if not hasattr(plugin, method) or not callable(getattr(plugin, method)):
                return False
        
        return True
    
    def _implements_validation_plugin(self, cls: Type) -> bool:
        """Check if class implements ValidationPlugin protocol."""
        required_methods = ['validate', 'get_plugin_info']
        
        for method in required_methods:
            if not hasattr(cls, method):
                return False
        
        return True


class CustomValidatorPlugin:
    """
    Example custom validation plugin implementation.
    
    This serves as a template for creating custom validation plugins
    that can be integrated with the QBH validation engine.
    """
    
    def __init__(self, validation_rules: Optional[Dict[str, Any]] = None):
        """Initialize custom validator plugin."""
        self.validation_rules = validation_rules or {}
        self.logger = logging.getLogger("CustomValidatorPlugin")
    
    def validate(self, data: Any, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate data using custom rules.
        
        Args:
            data: Data to validate
            schema: Optional validation schema
            
        Returns:
            Validation result dictionary
        """
        try:
            # Apply custom validation logic
            is_valid = True
            confidence = 1.0
            validation_details = {}
            
            # Example custom validation rules
            if 'min_length' in self.validation_rules:
                min_length = self.validation_rules['min_length']
                data_length = len(str(data))
                
                if data_length < min_length:
                    is_valid = False
                    confidence *= 0.5
                    validation_details['length_check'] = f"Length {data_length} < minimum {min_length}"
            
            if 'required_pattern' in self.validation_rules:
                pattern = self.validation_rules['required_pattern']
                data_str = str(data)
                
                if pattern not in data_str:
                    is_valid = False
                    confidence *= 0.7
                    validation_details['pattern_check'] = f"Required pattern '{pattern}' not found"
            
            if 'forbidden_values' in self.validation_rules:
                forbidden = self.validation_rules['forbidden_values']
                
                if data in forbidden:
                    is_valid = False
                    confidence = 0.0
                    validation_details['forbidden_check'] = f"Data contains forbidden value: {data}"
            
            return {
                'is_valid': is_valid,
                'confidence': confidence,
                'validation_details': validation_details,
                'plugin_name': 'CustomValidator'
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'error': str(e),
                'plugin_name': 'CustomValidator'
            }
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Return plugin information."""
        return {
            'name': 'Custom Validator Plugin',
            'version': '1.0.0',
            'description': 'Example custom validation plugin with configurable rules',
            'author': 'QBH Validation Team',
            'type': 'custom_validation'
        }


# Global plugin manager instance
plugin_manager = PluginManager()

# Register default custom plugin
plugin_manager.register_plugin("custom_validator", CustomValidatorPlugin())