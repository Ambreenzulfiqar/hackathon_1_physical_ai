# Implementation Plan: Physical AI & Humanoid Robotics — Essentials

**Branch**: `001-ai-humanoid-textbook` | **Date**: 2025-12-17 | **Spec**: specs/001-ai-humanoid-textbook/spec.md
**Input**: Feature specification from `/specs/001-ai-humanoid-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Physical AI & Humanoid Robotics textbook with Docusaurus UI and RAG chatbot. The system will provide access to 6 chapters of educational content with an integrated AI assistant that answers questions based only on textbook content. The architecture uses Docusaurus for the frontend and Qdrant + Neon + FastAPI for the RAG backend, designed to operate within free-tier constraints.

## Technical Context

**Language/Version**: JavaScript/TypeScript (Node.js 18+), Python 3.11 for backend services
**Primary Dependencies**: Docusaurus 3.x, FastAPI 0.104+, Qdrant 1.5+, Neon PostgreSQL
**Storage**: Vector database (Qdrant) for embeddings, PostgreSQL (Neon) for metadata, static files for content
**Testing**: Jest for frontend, pytest for backend, Playwright for E2E tests
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <2s page load times, <3s AI response times, support 100 concurrent users
**Constraints**: Free-tier resource limits ($50/month max), minimal GPU usage, lightweight embeddings
**Scale/Scope**: 6 textbook chapters, 100+ concurrent users, 99% uptime requirement

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Simplicity**: Architecture must remain simple and minimal, avoiding unnecessary complexity
2. **Accuracy**: All content and AI responses must be technically accurate and factually correct
3. **Minimalism**: Implementation should focus on core educational functionality without extraneous features
4. **Fast Builds**: Build and deployment cycles must be optimized for quick iteration
5. **Free-tier Architecture**: All components must operate within free-tier constraints with minimal computational requirements
6. **Educational Focus**: Every feature must enhance the student's understanding of Physical AI and Humanoid Robotics concepts

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-humanoid-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── textbook_chapter.py
│   │   ├── ai_chat_session.py
│   │   └── user_preference.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   └── content_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── textbook.py
│   │   │   ├── chat.py
│   │   │   └── search.py
│   │   └── main.py
│   └── config/
│       ├── settings.py
│       └── database.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── TextbookViewer/
│   │   ├── ChatInterface/
│   │   └── TextSelector/
│   ├── pages/
│   │   ├── Chapter/
│   │   └── Home/
│   └── services/
│       ├── api-client.js
│       └── text-selection.js
├── docs/
│   ├── 01-intro-to-physical-ai/
│   ├── 02-basics-humanoid-robotics/
│   ├── 03-ros2-fundamentals/
│   ├── 04-digital-twin-simulation/
│   ├── 05-vision-language-action/
│   └── 06-capstone-ai-robot-pipeline/
├── docusaurus.config.js
└── package.json

tests/
├── e2e/
│   └── textbook-flow.spec.js
└── accessibility/
    └── wcag-checks.spec.js
```

**Structure Decision**: Web application structure selected with separate backend (FastAPI) and frontend (Docusaurus) to maintain clear separation of concerns while enabling the RAG functionality. The frontend uses Docusaurus for documentation presentation with custom React components for AI interaction, while the backend handles AI processing and content management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dual architecture (frontend+backend) | Required for RAG functionality | Single-page app cannot handle AI processing and vector storage |
| Multiple service dependencies | Required for textbook + AI features | Simplified approach would not meet core feature requirements |
