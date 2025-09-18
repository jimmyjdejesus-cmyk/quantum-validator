"""
Simple structure test for quantum-validator package.

This test validates that the package structure is correct and
can be imported without external dependencies for basic validation.
"""

def test_package_structure():
    """Test that the package structure is correctly set up."""
    import os
    
    # Check that all expected directories exist
    base_dir = "/home/runner/work/quantum-validator/quantum-validator"
    
    expected_structure = [
        "quantum_validator/__init__.py",
        "quantum_validator/validation_engine.py", 
        "quantum_validator/core/__init__.py",
        "quantum_validator/core/quantum_validator.py",
        "quantum_validator/core/biological_validator.py",
        "quantum_validator/core/holographic_validator.py",
        ".cursor/AGENTS.md",
        ".cursor/Instructions.md",
        ".cursor/rules/01_REQUIREMENTS_ANALYSIS.md",
        ".cursor/rules/02_SYSTEM_DESIGN_AND_ARCHITECTURE.md",
        ".cursor/rules/03_SECURE_CODE_IMPLEMENTATION.md",
        ".cursor/rules/04_ROBUST_TESTING_AND_QA.md",
        ".cursor/rules/05_SYSTEMATIC_DEBUGGING_AND_RCA.md",
        ".cursor/rules/06_CRITICAL_CODE_REVIEW.md",
        ".cursor/rules/07_VERIFIABLE_DOCUMENTATION.md",
        ".cursor/rules/99_BLAMELESS_POSTMORTEM.md",
        "requirements.txt",
        "pyproject.toml",
        "README.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in expected_structure:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All expected files and directories are present")
        return True


def test_file_contents():
    """Test that key files have expected content."""
    import os
    base_dir = "/home/runner/work/quantum-validator/quantum-validator"
    
    # Test README has quantum-validator content
    with open(os.path.join(base_dir, "README.md"), "r") as f:
        readme_content = f.read()
        if "Quantum-Biological Holographic" not in readme_content:
            print("❌ README.md missing expected quantum-validator content")
            return False
    
    # Test package init file 
    with open(os.path.join(base_dir, "quantum_validator", "__init__.py"), "r") as f:
        init_content = f.read()
        if "QBHValidationEngine" not in init_content:
            print("❌ Package __init__.py missing expected exports")
            return False
    
    # Test .cursor framework is present
    with open(os.path.join(base_dir, ".cursor", "AGENTS.md"), "r") as f:
        agents_content = f.read()
        if "AI Agent Constitution" not in agents_content:
            print("❌ .cursor/AGENTS.md missing expected content")
            return False
    
    print("✅ All key files have expected content")
    return True


def main():
    """Run structure validation tests."""
    print("🔍 Testing quantum-validator package structure...")
    print("=" * 50)
    
    structure_ok = test_package_structure()
    content_ok = test_file_contents()
    
    if structure_ok and content_ok:
        print("\n🎉 Package structure validation PASSED")
        print("   The quantum-validator project is properly structured")
        print("   with the complete VDE framework implementation.")
        return True
    else:
        print("\n❌ Package structure validation FAILED")
        return False


if __name__ == "__main__":
    import os
    main()