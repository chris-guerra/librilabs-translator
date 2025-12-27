# Sprint Change Proposal: Move Docker Setup to Story 1.2

**Date:** 2025-01-27  
**Change Type:** Story Reordering & Scope Adjustment  
**Status:** Draft - Awaiting Approval

---

## Analysis Summary

### Identified Issue

Docker containerization is currently planned for Story 1.7 (late in Epic 1), but it should be implemented earlier to enable containerized development workflow from the start. Specifically:

- **Trigger:** Story 1.1 (FastAPI Backend Structure) is complete, and Story 1.2 (PostgreSQL Database Setup) is next
- **Core Problem:** Docker setup should happen now (after Story 1.1) rather than later (Story 1.7), so that Story 1.2 (database setup) can work with containerized services from the beginning
- **Goal:** Have Docker ready before database work begins, with clear backend and frontend images with intuitive names, plus a Makefile for easy development workflow

### Impact Analysis

**Epic Impact:**
- Epic 1 (Foundation & Document Upload) remains achievable with story reordering
- No impact on Epic 2 or Epic 3
- Story sequence needs adjustment: Docker moves from 1.7 → 1.2, all subsequent stories shift by one

**Artifact Impact:**
- PRD: Story renumbering required (1.2-1.7 shift)
- Story 1.2 document: Needs update to reference Docker/containerized environment
- New Story 1.2 document: Create Docker setup story with Makefile requirement
- Architecture docs: Verify alignment (likely minimal changes needed)

**MVP Impact:**
- No scope reduction needed
- No core goal changes
- Same work, different order

### Recommended Path Forward

**Selected Path:** Direct Adjustment / Integration

- Move Docker setup to new Story 1.2
- Renumber current Story 1.2 (PostgreSQL) → Story 1.3
- Renumber Stories 1.3-1.6 → Stories 1.4-1.7
- Keep Story 1.8 (CI/CD) as 1.8 (depends on Docker)
- Update Story 1.3 (PostgreSQL) to work with containerized environment

**Rationale:**
- High feasibility - straightforward reordering
- Low-medium effort - primarily documentation updates
- Low risk - no code changes, just reordering
- No timeline impact - same work, different order
- Better developer experience - containerized workflow from the start

---

## Specific Proposed Edits

### 1. PRD Document (`docs/prd.md`)

#### Edit 1.1: Insert New Story 1.2 (Docker Setup)

**Location:** After Story 1.1, before current Story 1.2

**Change:** Insert new story:

```markdown
### Story 1.2: Set Up Docker and Deployment Configuration

As a developer,  
I want Docker containerization for both frontend and backend with a Makefile for easy development workflow,  
so that I can deploy the application consistently across environments and develop with containerized services.

**Acceptance Criteria:**
1. Dockerfile is created for FastAPI backend with Python 3.14
2. Dockerfile is created for Next.js frontend (or multi-stage build)
3. docker-compose.yml is created for local development (backend, frontend, PostgreSQL)
4. Makefile is created with standard development commands (build, up, down, logs, etc.)
5. Makefile supports volume mounting for development mode (hot-reload for both frontend and backend)
6. Docker images use intuitive names (e.g., `librilabs-translator-backend`, `librilabs-translator-frontend`)
7. Environment variables are properly configured via .env files
8. Docker containers can be built and run locally using Makefile commands
9. Application runs successfully in Docker containers
10. Backend health check endpoint works from containerized backend
11. Frontend can communicate with backend API from containers
12. Development workflow is documented (using Makefile commands)
```

#### Edit 1.2: Renumber Current Story 1.2 → Story 1.3

**Location:** Current Story 1.2 section

**Change:** 
- Change heading from `### Story 1.2: Set Up PostgreSQL Database` to `### Story 1.3: Set Up PostgreSQL Database`
- Update story text to reference Docker setup from Story 1.2
- Update Acceptance Criteria #1 to: "PostgreSQL database is accessible via Docker Compose (local development) or Railway managed Postgres (production)"
- Add note: "**Note:** This story assumes Docker setup from Story 1.2 is complete. Database setup will work with containerized PostgreSQL service."

#### Edit 1.3: Renumber Story 1.3 → Story 1.4

**Location:** Current Story 1.3 section

**Change:**
- Change heading from `### Story 1.3: Create Document Model` to `### Story 1.4: Create Document Model`

#### Edit 1.4: Renumber Story 1.4 → Story 1.5

**Location:** Current Story 1.4 section

**Change:**
- Change heading from `### Story 1.4: Implement Document Upload API` to `### Story 1.5: Implement Document Upload API`

#### Edit 1.5: Renumber Story 1.5 → Story 1.6

**Location:** Current Story 1.5 section

**Change:**
- Change heading from `### Story 1.5: Create Document Upload UI` to `### Story 1.6: Create Document Upload UI`

#### Edit 1.6: Renumber Story 1.6 → Story 1.7

**Location:** Current Story 1.6 section

**Change:**
- Change heading from `### Story 1.6: Implement Language Selection` to `### Story 1.7: Implement Language Selection`

#### Edit 1.7: Remove Old Story 1.7 (Docker)

**Location:** Current Story 1.7 section

**Change:**
- Delete entire Story 1.7 section (Docker setup) - it's now Story 1.2

#### Edit 1.8: Update Story 1.8 Reference

**Location:** Story 1.8 section

**Change:**
- Update any references to Docker setup to note it's now in Story 1.2
- Keep Story 1.8 as-is (CI/CD depends on Docker from Story 1.2)

---

### 2. Story Documents

#### Edit 2.1: Create New Story 1.2 Document

**File:** `docs/stories/1.2.set-up-docker-and-deployment-configuration.md`

**Content:** Create new story document with:
- Status: Draft
- Story text (as shown in PRD Edit 1.1)
- Acceptance Criteria (as shown in PRD Edit 1.1)
- Tasks/Subtasks covering:
  - Backend Dockerfile creation
  - Frontend Dockerfile creation
  - docker-compose.yml setup
  - Makefile creation with standard commands (build, up, down, logs, clean, etc.)
  - Makefile dev mode with volume mounting
  - Environment variable configuration
  - Testing containerized setup
  - Documentation
- Dev Notes referencing Story 1.1 completion
- Technical constraints from architecture docs
- Testing requirements

#### Edit 2.2: Update Current Story 1.2 Document

**File:** `docs/stories/1.2.set-up-postgresql-database-with-sqlalchemy-and-alembic.md`

**Change:**
- Rename file to: `docs/stories/1.3.set-up-postgresql-database-with-sqlalchemy-and-alembic.md`
- Update title: `# Story 1.3: Set Up PostgreSQL Database with SQLAlchemy and Alembic`
- Update Status section (keep as Draft)
- Add to Dev Notes section:
  - **Previous Story Insights:**
    - Story 1.2 (Docker Setup) must be completed first
    - Docker Compose provides PostgreSQL service for local development
    - Database connection should work with containerized PostgreSQL from docker-compose.yml
    - Use `make up` or `docker-compose up` to start database service
- Update Acceptance Criteria #1 to reference Docker Compose
- Update Task 2 (Configure Database Connection) to include:
  - Note that DATABASE_URL should work with docker-compose PostgreSQL service
  - Document connection string format for containerized environment: `postgresql+asyncpg://librilabs:librilabs_dev@postgres:5432/librilabs_translator`
- Update Testing Requirements to note database will be containerized

#### Edit 2.3: Renumber Story 1.3 Document → Story 1.4

**File:** `docs/stories/1.3.create-document-model-and-basic-persistence-layer.md` (if exists)

**Change:**
- Rename to: `docs/stories/1.4.create-document-model-and-basic-persistence-layer.md`
- Update title to Story 1.4

#### Edit 2.4: Renumber Story 1.4 Document → Story 1.5

**File:** `docs/stories/1.4.implement-document-upload-api-endpoint.md` (if exists)

**Change:**
- Rename to: `docs/stories/1.5.implement-document-upload-api-endpoint.md`
- Update title to Story 1.5

#### Edit 2.5: Renumber Story 1.5 Document → Story 1.6

**File:** `docs/stories/1.5.create-document-upload-ui-component.md` (if exists)

**Change:**
- Rename to: `docs/stories/1.6.create-document-upload-ui-component.md`
- Update title to Story 1.6

#### Edit 2.6: Renumber Story 1.6 Document → Story 1.7

**File:** `docs/stories/1.6.implement-language-selection-ui-and-api-integration.md` (if exists)

**Change:**
- Rename to: `docs/stories/1.7.implement-language-selection-ui-and-api-integration.md`
- Update title to Story 1.7

---

### 3. Architecture Documents

#### Edit 3.1: Verify Docker Documentation Alignment

**Files to Check:**
- `docs/architecture/deployment-architecture.md`
- `docs/architecture/unified-project-structure.md`
- `docs/architecture.md`

**Action:** Review and verify:
- Docker Compose configuration aligns with new Story 1.2 placement
- Image naming conventions match requirement (intuitive names)
- Makefile is mentioned or should be added to development workflow documentation
- No conflicts with story reordering

**Expected Result:** Likely minimal changes needed - architecture already documents Docker setup. May need to add Makefile reference to development workflow docs.

---

### 4. QA Gates

#### Edit 4.1: Update QA Gate for Story 1.2

**File:** `docs/qa/gates/1.2-set-up-docker-and-deployment-configuration.yml` (new file)

**Action:** Create new QA gate file for Story 1.2 (Docker setup) following the pattern from Story 1.1 gate.

#### Edit 4.2: Renumber QA Gate for Story 1.3

**File:** `docs/qa/gates/1.2-set-up-postgresql-database-with-sqlalchemy-and-alembic.yml` (if exists)

**Change:**
- Rename to: `docs/qa/gates/1.3-set-up-postgresql-database-with-sqlalchemy-and-alembic.yml`
- Update any internal references to story number

---

## High-Level Action Plan

### Immediate Next Steps

1. **User Approval:** Obtain explicit approval for this Sprint Change Proposal
2. **PRD Updates:** Apply all PRD edits (story renumbering and new Story 1.2)
3. **Story Document Creation:** Create new Story 1.2 document with Docker setup details
4. **Story Document Updates:** Renumber and update existing story documents
5. **Architecture Review:** Verify architecture docs alignment, add Makefile references if needed
6. **QA Gate Updates:** Create/renumber QA gate files

### Implementation Order

1. Update PRD (`docs/prd.md`) - all story renumbering
2. Create new Story 1.2 document (`docs/stories/1.2.set-up-docker-and-deployment-configuration.md`)
3. Renumber Story 1.2 → 1.3 document
4. Renumber other story documents (1.3→1.4, 1.4→1.5, etc.) if they exist
5. Review and update architecture docs
6. Create/update QA gate files

### Validation

- All story numbers are sequential (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
- No duplicate story numbers
- Docker setup is now Story 1.2 (before database setup)
- Story 1.3 (PostgreSQL) references Docker setup from Story 1.2
- Makefile requirement is included in Story 1.2 acceptance criteria
- All cross-references are updated

---

## Agent Handoff Plan

**PM Agent (Current):** Complete this change proposal and obtain user approval

**After Approval:**
- **PM Agent:** Apply PRD and story document edits
- **Architect Agent (if needed):** Review architecture docs for Makefile workflow documentation
- **Dev Agent:** Will implement Story 1.2 (Docker setup) when ready

**No fundamental replanning required** - this is a straightforward reordering that maintains all existing scope and goals.

---

## Success Criteria

- [x] Change proposal document created
- [x] User approval obtained
- [x] PRD updated with story renumbering
- [x] New Story 1.2 (Docker) document created
- [x] Story 1.2 (PostgreSQL) → Story 1.3 document updated and renamed
- [x] Other story documents renumbered if they exist
- [x] Architecture docs reviewed and updated if needed
- [x] QA gate files created/renumbered
- [x] All cross-references validated
- [x] Story sequence validated (1.0 → 1.1 → 1.2 → 1.3 → ... → 1.8)

---

## Notes

- This change does not affect Epic 2 or Epic 3
- No code changes required - documentation updates only
- Story 1.2 (Docker) will enable containerized development for all subsequent stories
- Makefile requirement ensures easy developer workflow with volume mounting for hot-reload
- Intuitive image names improve developer experience and deployment clarity

---

**Proposal Status:** ✅ APPROVED AND IMPLEMENTED  
**Implementation Date:** 2025-01-27  
**Next Action:** Story 1.2 (Docker setup) is ready for development

