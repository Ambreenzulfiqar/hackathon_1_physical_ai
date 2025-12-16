<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A
Added sections: All principles and sections added
Removed sections: None
Templates requiring updates: N/A
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity
Keep all implementations simple and minimal. Solutions must be lightweight and avoid unnecessary complexity. Every feature should have a clear, essential purpose that contributes to the core learning objectives.

### II. Accuracy
All content and code examples must be technically accurate and verified. Information presented in the textbook and implemented in the RAG system must be factually correct and represent best practices in Physical AI and Humanoid Robotics.

### III. Minimalism
Adhere to minimal viable implementations. Focus on core concepts without extraneous features. Prioritize essential functionality that serves the educational purpose over comprehensive but complex implementations.

### IV. Fast Builds
Maintain fast build and deployment cycles. All components (Docusaurus UI, RAG backend, simulation interfaces) must be optimized for quick iteration and development cycles.

### V. Free-tier Architecture
Design all systems to operate within free-tier constraints. This includes minimal computational requirements, lightweight embeddings, and architectures that don't require expensive GPU resources.

### VI. Educational Focus

All development must prioritize educational value and learning outcomes. Every feature should enhance the student's understanding of Physical AI and Humanoid Robotics concepts.

## Additional Constraints

Technology stack requirements: Docusaurus for textbook UI, Qdrant + Neon + FastAPI for RAG chatbot, ROS 2 for robotics fundamentals, Gazebo/Isaac for digital twin simulation. All components must be compatible with free-tier hosting and minimal computational requirements. No heavy GPU usage allowed; implementations must work with CPU-based processing where possible.

## Development Workflow

All code must be testable and documented. Each chapter implementation requires functional validation. Code reviews must verify compliance with simplicity and minimalism principles. Pull requests must demonstrate educational value and technical accuracy.

## Governance

This constitution governs all development activities for the Physical AI & Humanoid Robotics textbook project. All code, documentation, and architectural decisions must comply with these principles. Amendments require explicit documentation and approval from project stakeholders.

**Version**: 1.0.0 | **Ratified**: 2025-12-17 | **Last Amended**: 2025-12-17
