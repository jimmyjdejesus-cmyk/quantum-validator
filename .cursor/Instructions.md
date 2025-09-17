# **Project Context & Instructions for AI Agent**

This document provides the high-level, stable context required for effective AI assistance on this project. The AI agent will reference this file to understand our goals, standards, and technical environment.

## **1. Project High-Level Objective**

The Quantum-Biological Holographic (QBH) Validation Engine is an advanced verification system that leverages quantum computing principles and biological algorithms to validate complex data structures and processes. Its primary goal is to provide ultra-high precision validation for scientific, financial, and critical infrastructure applications where traditional validation methods are insufficient. The system aims to achieve validation accuracy beyond classical computational limits by employing quantum-inspired algorithms and bio-mimetic validation patterns.

## **2. Core Technologies & Tech Stack**

* **Frontend**: React.js with TypeScript, Quantum visualization libraries, D3.js for data visualization
* **Backend**: Python (primary), Node.js microservices, Quantum computing libraries (Qiskit, Cirq)
* **Database**: PostgreSQL (primary), Redis (caching), InfluxDB (time-series data)
* **Infrastructure/Deployment**: Docker, Kubernetes, AWS/GCP quantum computing services
* **Key Libraries/Services**: 
  - Quantum simulation: Qiskit, Cirq, PennyLane
  - Bio-inspired algorithms: NetworkX, NumPy, SciPy
  - Validation frameworks: Pydantic, Marshmallow
  - Machine Learning: TensorFlow Quantum, PyTorch

## **3. Architectural Principles**

We adhere to a quantum-classical hybrid architecture with event-driven validation pipelines. All validation components must be deterministic when classical and probabilistic when quantum-enhanced. We prioritize:
- **Quantum-First Design**: Leverage quantum advantages where applicable, fall back to classical methods gracefully
- **Bio-Inspired Resilience**: Implement fault-tolerance patterns based on biological systems
- **Immutable Validation Chains**: All validation results are cryptographically signed and immutable
- **Real-time Quantum State Management**: Maintain coherent quantum states throughout validation processes
- **Holographic Data Distribution**: Information is distributed across multiple dimensions for redundancy

## **4. Key Repositories & Codebases**

* **Primary Application Repo**: https://github.com/jimmyjdejesus-cmyk/quantum-validator
* **Infrastructure as Code Repo**: TBD - Quantum infrastructure automation
* **Shared Libraries Repo**: TBD - Quantum validation primitives and bio-algorithms

## **5. Team Coding Standards & Conventions**

* **Code Style Guide**: PEP 8 for Python, ESLint + Prettier for JavaScript/TypeScript
* **Git Branching Strategy & Commit Message Format**: 
  - Feature branches: `feature/quantum-enhancement-description`
  - Conventional commits: `type(scope): description`
  - All commits must pass quantum simulation tests
* **API Design Guide (e.g., RESTful principles)**: 
  - RESTful APIs with GraphQL for complex quantum state queries
  - All endpoints must support both classical and quantum response modes
* **Testing Philosophy (e.g., TDD, BDD)**: 
  - Quantum-TDD: Test-driven development with quantum state verification
  - Bio-inspired testing: Evolutionary test generation and mutation testing
  - Property-based testing for quantum algorithms