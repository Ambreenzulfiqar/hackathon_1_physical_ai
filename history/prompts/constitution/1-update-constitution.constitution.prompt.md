---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: MP
command: /sp.constitution
labels: [constitution,setup,initial]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course.
The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI
and a fully integrated free-tier RAG chatbot.

Scope:
- 6 short chapters:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Clean UI
- Free-tier friendly
- Lightweight embeddings

Core Principles:
- Simplicity
- Accuracy
- Minimalism
- Fast builds
- Free-tier architecture
- RAG answers ONLY from book text

Key Features:
- Docusaurus textbook
- RAG chatbot (Qdrant + Neon + FastAPI)
- Select-text → Ask AI
- Optional Urdu / Personalize features

Constraints:
- No heavy GPU usage
- Minimal embeddings

Success Criteria:
- Build successful textbook with integrated RAG
```

## Response snapshot

Updated the constitution file with project-specific details for the Physical AI & Humanoid Robotics textbook project. The constitution now includes six core principles (Simplicity, Accuracy, Minimalism, Fast Builds, Free-tier Architecture, Educational Focus) and sections for Additional Constraints, Development Workflow, and Governance that align with the project requirements.

## Outcome

- ✅ Impact: Updated constitution with project-specific principles and constraints
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: None
- 🧠 Reflection: Successfully transformed generic constitution template into project-specific governance document

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A