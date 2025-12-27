# Librilabs Translator Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** 2025-01-27  
**Author:** John (PM)  
**Status:** Draft

---

## Goals and Background Context

### Goals

- Deliver a unified translation and review interface that eliminates the fragmented workflow of using separate tools for translation and editing
- Enable side-by-side comparison of original and translated text with synchronized scrolling for efficient review
- Provide in-place editing capabilities so users can edit translations directly without export/import cycles
- Support progress saving and resumable translation for longform documents
- Create a simple, document-focused workflow optimized for individual users and small teams translating standalone documents
- Establish product-market fit with individual academics, researchers, and writers through MVP validation
- Differentiate from free tools (no review workflow) and enterprise platforms (too complex/expensive) by targeting the underserved individual/SMB segment

### Background Context

Librilabs Translator addresses a significant gap in the translation software market. Current tools either lack review capabilities (free tools like Google Translate, DeepL) or are too complex and expensive for individual users (enterprise platforms like Smartling). This leaves a $500M-$1B serviceable addressable market underserved.

**The Problem:** Users translating longform documents (research papers, academic articles, business reports, books, blog posts) face a fragmented, inefficient workflow requiring multiple tools and manual processes:

1. **Translation Step:** Users upload documents to translation tools (DeepL, Google Translate) or use APIs
2. **Export Step:** Download translated text (often losing formatting or structure)
3. **Review Step:** Open translated text in a separate editor (Word, Google Docs, text editor)
4. **Comparison Step:** Manually compare original and translated versions (switching between windows/tabs)
5. **Editing Step:** Make corrections and refinements in the editor
6. **Re-import Step:** Copy/paste or re-upload if changes needed in translation tool

**Impact:** This fragmented workflow adds 30-50% overhead to translation time, introduces errors through manual copying/pasting, breaks workflow continuity, and forces users to either accept lower quality from raw machine translation or pay $500-2,000 per document for professional services.

**The Solution:** Librilabs Translator combines AI-powered translation quality with an integrated human review workflow, specifically designed for longform document translation. The MVP focuses on TXT file translation with side-by-side comparison, in-place editing, and progress saving—validating the core value proposition before expanding to additional file formats.

**Target Market:** Individual academics and researchers (primary), professional writers and content creators (secondary), and small business teams (tertiary) in English-speaking markets. This represents 4-8 million individuals and 780K-1.95M small businesses with regular document translation needs.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-01-27 | v1.0 | Initial PRD creation | John (PM) |

---

## Requirements

### Functional Requirements

1. FR1: The system must accept TXT file uploads with file format validation and size limits (maximum file size to be determined based on technical constraints)
2. FR2: The system must provide a user interface for selecting source and target languages from supported language pairs before translation begins
3. FR3: The system must process document translation using OpenAI LLMs with additional quality optimization logic, accepting text content and language pair as input
4. FR4: The system must display translation progress during processing, showing real-time status updates to the user
5. FR5: The system must save translation progress and allow users to resume interrupted translations for long documents
6. FR6: The system must provide a side-by-side comparison view displaying original text (left column) and translated text (right column) with synchronized scrolling that keeps both texts aligned by paragraph
7. FR7: The system must include paragraph markers in the side-by-side view for navigation between original and translated content
8. FR8: The system must allow in-place editing of translated text directly in the comparison view, with the original text remaining read-only
9. FR9: The system must automatically save changes made to translated text during editing
10. FR10: The system must provide export functionality to download the final translated text as a TXT file
11. FR11: The system must persist user documents and translation progress in a database to enable resume functionality (Note: User authentication is post-MVP, but data model should support future authentication integration)
12. FR12: The system must support anonymous/session-based document management for MVP (authentication to be added post-MVP)
13. FR13: The system must transform from translation progress view to comparison view automatically when translation completes
14. FR14: The system must handle plain text editing only (no markdown rendering in MVP) for the translated text

### Non-Functional Requirements

1. NFR1: Translation must complete for documents up to 50 pages within 5 minutes under normal load conditions
2. NFR2: The comparison view must load and function smoothly for documents up to 100 pages without performance degradation
3. NFR3: Progress saving and resume operations must have a 90%+ success rate for documents greater than 10 pages
4. NFR4: The system must maintain zero critical bugs (data loss, security issues, complete workflow failures) in production for 30 days post-MVP launch
5. NFR5: The system must use FastAPI for backend API implementation as per technical preferences
6. NFR6: The system must use Next.js for frontend implementation as per technical preferences
7. NFR7: The system must use PostgreSQL for relational database storage as per technical preferences
8. NFR8: The system must support session-based document management for MVP (authentication using email code/magic-link via Resend with JWT will be added post-MVP, but system architecture must allow for future authentication integration)
9. NFR9: The system must ensure all user data and documents are securely stored and transmitted using industry-standard encryption
10. NFR10: The system must provide a responsive web interface that works across desktop and tablet devices (mobile optimization deferred to post-MVP)
11. NFR11: The system must handle concurrent translation requests from multiple users without significant performance degradation
12. NFR12: The system must provide error handling and user-friendly error messages for common failure scenarios (file upload errors, translation failures, network issues)
13. NFR13: The system must maintain translation quality that meets 70%+ user acceptance rate (3+ stars on 5-point scale) as per MVP success criteria
14. NFR14: The system must support the core workflow completion rate of 80%+ of test users successfully completing the full workflow without external tools

---

## User Interface Design Goals

### Overall UX Vision

The interface prioritizes simplicity and workflow integration. The goal is a focused, document-first experience that eliminates tool switching. The UI guides users through: upload → translate → compare → edit → download, with clear progress indicators and minimal cognitive load. Visual design should be clean and uncluttered, emphasizing the side-by-side comparison view as the core interaction. The experience should feel fast and responsive, even for long documents, with clear feedback during translation processing.

### Key Interaction Paradigms

1. **Side-by-Side Comparison with Synchronized Scrolling:** The primary interaction mode displays original and translated text in two columns with synchronized scrolling, keeping paragraphs aligned for efficient comparison.

2. **In-Place Editing:** Users edit translated text directly in the comparison view with auto-save, eliminating export/import cycles.

3. **Progressive Disclosure:** The interface reveals features as needed—upload interface first, then translation progress, then comparison view—avoiding overwhelming users upfront.

4. **Context Preservation:** The interface maintains document context throughout the workflow, with clear navigation and progress indicators so users always know where they are.

5. **Responsive Feedback:** All user actions (upload, translation start, editing, save) provide immediate visual feedback to confirm the system is working.

### Core Screens and Views

1. **Upload Screen:** File upload interface with drag-and-drop support, file format validation feedback, and language selection (source and target dropdowns). Includes file size and format guidance. Authenticated users land directly on this screen.

2. **Translation Progress Screen:** Real-time progress indicator showing estimated time remaining (e.g., "Estimated time: 2 minutes remaining") with a progress bar or percentage indicator. No paragraph-by-paragraph status—focus on overall progress and time estimate. Allows users to see progress for long documents.

3. **Side-by-Side Comparison/Edit View:** Primary working interface with original text (left, read-only) and translated text (right, editable) in synchronized columns. Includes paragraph markers, scroll synchronization, and editing controls. Transforms from progress view when translation completes. After download, users remain in this view to continue editing if needed.

4. **Download/Export Interface:** Export controls integrated into the comparison view (e.g., download button in header/toolbar) to download the final translated text as TXT.

**MVP Scope Clarifications:**
- Single document focus in MVP (no document history/list view)
- Authenticated users go directly to upload screen
- After download, users stay in comparison view (can continue editing or start new translation)

### Accessibility: WCAG AA

The interface should meet WCAG AA standards, including:
- Keyboard navigation for all interactive elements
- Screen reader compatibility for translation content and UI controls
- Sufficient color contrast for text readability
- Focus indicators for keyboard navigation
- Alt text for icons and non-text elements
- Form labels and error messages accessible to assistive technologies

### Branding

**Color Palette:**
- **Background Colors:** Primary (#FFFFFF), Secondary (#F4F5F7), Sidebar (#F7F8FA)
- **Text Colors:** Primary (#111827), Secondary (#6B7280)
- **Border Colors:** Light (#E5E7EB)
- **Accent Colors:** Orange (#F97316 - primary accent), Orange Soft (#FFF7ED), Blue Soft (#EEF2FF), Green (#16A34A - success), Red (#DC2626 - error)
- **Interactive States:** Hover (#F3F4FF), Active (#FFF7ED)

**Typography:**
- **Font Family:** System font stack (-apple-system, BlinkMacSystemFont, system-ui, Segoe UI, sans-serif)
- **Font Sizes:** xs (12px), sm (13px), md (14px - base), lg (16px), xl (20px), display (24px)
- **Font Weights:** regular (400), medium (500), semibold (600), bold (700)

**Logo & Brand Identity:**
- **Text Logo:** "Librilabs" (18px, semibold/600, #111827)
- **Brand Color:** Orange (#F97316) as primary accent
- **Tone of Voice:** Professional

**Implementation Note:** All branding elements must be implemented using Untitled UI components exclusively (no custom components). Colors and typography should be applied through Tailwind CSS configuration to match the Untitled UI design system while respecting the brand palette where possible.

### Target Device and Platforms: Web Responsive

The MVP targets web-responsive design supporting:
- **Desktop:** Windows, macOS, Linux (Chrome, Firefox, Safari, Edge - latest 2 versions)
- **Tablet:** iPad, Android tablets (responsive web interface)
- **Mobile:** iOS Safari, Android Chrome (responsive web, not native apps for MVP)

The interface should adapt to different screen sizes, with the side-by-side view optimized for desktop/tablet landscape orientation. Mobile view may require a stacked or tabbed layout for smaller screens.

---

## Technical Assumptions

### Repository Structure: Monorepo

The project uses a monorepo structure with:
- `frontend/` - Next.js application (independent, can be moved separately)
- `backend/` - FastAPI application (to be created, independent)
- `docs/` - Documentation directory
- Shared types/interfaces if needed (TypeScript definitions)

**Rationale:** Monorepo structure is already established in the project. It simplifies development, enables code sharing, and maintains consistency across frontend and backend. Both applications remain independent and can be extracted to separate repositories if needed in the future.

### Service Architecture: Monolith

The MVP uses a **Monolith FastAPI service with modular design**:

**Frontend (Next.js 16.0.4):**
- Client-side application
- API calls to backend using native `fetch` + TanStack Query
- React Server Components where beneficial
- Server-side rendering where beneficial

**Backend (FastAPI Monolith):**
- Single FastAPI application (Python 3.14) with modular design
- **API Routers:** `/auth/*`, `/users/*`, `/documents/*`, `/translations/*`
- **Modular Packages:**
  - `services.translation` - Translation logic (OpenAI integration, chunking, progress tracking) - extractable to separate service
  - `services.auth` - Authentication logic (email code/magic-link, JWT) - post-MVP
  - `services.persistence` - Database operations (SQLAlchemy models, queries)
- **Design Philosophy:** Modular structure allows future extraction to microservices if translation load requires it

**Database Layer:**
- PostgreSQL (Railway's managed Postgres)
- SQLAlchemy 2.0 with declarative mappings and AsyncSession
- Alembic for database migrations
- asyncpg driver for async database operations
- JSON fields for flexible translation state storage

**File Storage (MVP):**
- No separate storage service for MVP (TXT files only)
- Store TXT content directly in PostgreSQL (TEXT column or `document_chunks` table - to be determined during technical design)
- Max file size: ~10MB (suitable for text in Postgres)

**Rationale:** Monolith architecture is optimal for MVP - simpler infrastructure, easier debugging, simpler observability, and faster development. The modular design allows extraction of `services.translation` into a separate translation worker service if translation load explodes in the future. This balances MVP simplicity with future scalability.

### Testing Requirements: Full Testing Pyramid

**Frontend Testing:**
- **Unit/Integration:** Vitest + React Testing Library
- **E2E:** Playwright

**Backend Testing:**
- **Unit/Integration:** Pytest for FastAPI + httpx test client

**Testing Strategy:**
- Unit tests for individual components and functions
- Integration tests for API endpoints and database interactions
- E2E tests for critical user workflows (upload → translate → edit → download)

**Rationale:** Full testing pyramid ensures quality across all layers. Vitest provides fast unit testing for React components, Playwright ensures end-to-end workflow validation, and Pytest with httpx provides comprehensive backend API testing. This approach catches bugs early and maintains code quality as the product evolves.

### Additional Technical Assumptions and Requests

1. **Component Library:** Untitled UI exclusively (no custom components) - all UI components must use Untitled UI to maintain design consistency and reduce maintenance burden.

2. **Styling:** Tailwind CSS for styling consistency - apply brand colors and typography through Tailwind configuration to match Untitled UI design system.

3. **State Management (Frontend):**
   - **Server State:** TanStack Query (React Query) for API data caching, loading/error states, retries, pagination
   - **UI/Local State:** Minimal approach - useState/useReducer or Zustand for cross-page UI state (selected document, modals)

4. **Form Handling (Frontend):** React Hook Form - lightweight, TypeScript-friendly, good performance, works well with Untitled UI.

5. **API Client (Frontend):** Native `fetch` API (Next.js optimized) combined with TanStack Query for caching and status management.

6. **Hosting/Infrastructure:**
   - **Primary Platform:** Railway for application hosting
   - Containerization (Docker) for consistent deployments
   - CI/CD pipeline for automated testing and deployment
   - Environment-based configuration (dev, staging, production)

7. **Email Service:** Resend for email delivery - email code/magic-link authentication (post-MVP, not part of MVP), user notifications and transactional emails.

8. **Translation Service:** OpenAI API integration with additional logic layer in `services.translation` package - handles chunking, progress tracking, and quality optimization.

9. **Authentication (Post-MVP):** Custom FastAPI implementation with Resend - flow: User enters email → FastAPI generates code/magic-link → Resend sends email → User submits → FastAPI issues JWT/session → User record stored in Postgres. **Important:** While authentication is post-MVP, the data model and API design must be structured to allow seamless addition of authentication without major refactoring. Documents and translations should be designed with user_id fields (nullable for MVP) to support future authentication integration.

10. **API Documentation:** OpenAPI/Swagger for FastAPI backend - enables API exploration and documentation.

11. **Security/Compliance:**
    - GDPR compliance considerations (user data, document content)
    - Rate limiting, CORS configuration, input validation
    - Encrypt sensitive data at rest and in transit (HTTPS, database encryption)
    - Secure file upload validation
    - User authentication and authorization for document access

12. **Performance Requirements:**
    - Translation API response time: <30 seconds for 10-page document (50,000 characters)
    - Comparison view load time: <3 seconds for documents up to 100 pages
    - Side-by-side scrolling: Smooth, 60fps performance
    - File upload: Support up to 10MB files (TXT format)
    - Progress saving: <1 second save/load time

13. **Future Scalability Considerations:**
    - Current: Monolith FastAPI for MVP and early growth
    - Future (if translation load explodes): Can extract `services.translation` into separate "translation worker" service consuming jobs from queue (Redis, RabbitMQ, or DB-backed job queue)

14. **Browser/OS Support:**
    - Modern browsers (Chrome, Firefox, Safari, Edge) - latest 2 versions
    - Desktop: Windows, macOS, Linux
    - Mobile: iOS Safari, Android Chrome (responsive web, not native apps for MVP)

15. **Post-MVP Integrations (Not in MVP):**
    - Payment Processing: Stripe or similar for subscription management
    - Analytics: Basic usage analytics (PostHog, Mixpanel, or similar)
    - File Storage Service: Consider separate storage service for larger files and multiple formats (PDF, Word, EPUB)

---

## Epic List

### Epic 1: Foundation & Document Upload
Establish project infrastructure (frontend upgrade, testing infrastructure, FastAPI backend, Next.js frontend, PostgreSQL database, Docker setup, CI/CD) and deliver document upload with language selection, enabling users to upload TXT files and select source/target languages.

### Epic 2: Translation Processing & Side-by-Side Comparison
Implement translation API with OpenAI integration, progress tracking with time estimates, and side-by-side comparison view with synchronized scrolling, enabling users to translate documents and view original and translated text side-by-side.

### Epic 3: Editing, Progress Saving & Export
Implement in-place editing with auto-save, progress saving and resume functionality for long documents, and download/export capability, enabling users to edit translations, save progress, and export final translated documents.

---

## Epic 1: Foundation & Document Upload

**Epic Goal:**
Establish the foundational infrastructure for the application (FastAPI backend, PostgreSQL database, Docker containerization, CI/CD pipeline) and deliver the document upload and language selection functionality. This enables users to upload TXT files and select source/target languages, providing the foundation for the translation workflow while validating the core infrastructure setup.

### Story 1.0: Upgrade Frontend and Set Up Testing Infrastructure

As a developer,  
I want the frontend upgraded to the required versions and testing infrastructure configured,  
so that I can develop with the correct tech stack and have testing capabilities from the start.

**Acceptance Criteria:**
1. Frontend Next.js is upgraded from 14.2.5 to 16.0.4
2. React is upgraded from 18.3.1 to 19 (as required by Next.js 16.0.4)
3. All frontend dependencies are updated and compatible with new versions
4. Frontend application runs successfully after upgrade
5. Frontend testing framework (Vitest) is installed and configured
6. React Testing Library is installed and configured for component testing
7. Playwright is installed and configured for E2E testing
8. Basic test setup files are created (vitest.config.ts, playwright.config.ts)
9. Example test files demonstrate testing patterns for frontend components
10. Frontend test scripts are added to package.json (test, test:e2e)
11. Backend testing framework (Pytest) setup is documented in backend setup guide
12. Backend testing with httpx is configured (will be implemented in Story 1.1)
13. Testing infrastructure is verified to work (can run example tests successfully)

**Note:** This story should be completed before Story 1.1 to ensure the correct tech stack is in place from the beginning.

### Story 1.1: Set Up FastAPI Backend Structure with Health Check

As a developer,  
I want a FastAPI backend application with a health check endpoint,  
so that I can verify the backend is running and establish the foundation for API development.

**Acceptance Criteria:**
1. FastAPI application is created in `backend/` directory with proper project structure
2. Health check endpoint `/health` returns 200 status with basic system information
3. Application runs locally and responds to health check requests
4. OpenAPI/Swagger documentation is accessible at `/docs`
5. CORS is configured to allow frontend connections
6. Basic error handling middleware is in place
7. Application can be run with `uvicorn` command
8. OpenAI API key setup process is documented (developer guide or README)
9. Environment variable template (.env.example) includes OPENAI_API_KEY placeholder
10. Instructions for obtaining OpenAI API key are provided (account creation, key generation, usage limits)
11. Secure storage of API key is configured (environment variables, not hardcoded)
12. Backend testing framework (Pytest) is installed and configured
13. httpx test client is configured for API endpoint testing
14. Example test demonstrates testing FastAPI endpoints (e.g., health check test)
15. Backend test scripts are configured (pytest command works)

### Story 1.2: Set Up Docker and Deployment Configuration

As a developer,  
I want Docker containerization for both frontend and backend with a Makefile for easy development workflow,  
so that I can deploy the application consistently across environments and develop with containerized services.

**Acceptance Criteria:**
1. Dockerfile is created for FastAPI backend with latest stable Python version
2. Dockerfile is created for Next.js frontend (or multi-stage build)
3. docker-compose.yml is created for local development (backend, frontend, PostgreSQL)
4. Makefile is created with standard development commands (build, up, down, logs, clean, etc.)
5. Makefile supports volume mounting for development mode (hot-reload for both frontend and backend)
6. Docker images use intuitive names (e.g., `librilabs-translator-backend`, `librilabs-translator-frontend`)
7. Environment variables are properly configured via .env files
8. Docker containers can be built and run locally using Makefile commands
9. Application runs successfully in Docker containers
10. Backend health check endpoint works from containerized backend
11. Frontend can communicate with backend API from containers
12. Development workflow is documented (using Makefile commands)

### Story 1.3: Set Up PostgreSQL Database with SQLAlchemy and Alembic

As a developer,  
I want PostgreSQL database connection with SQLAlchemy ORM and Alembic migrations configured,  
so that I can store and manage application data with proper schema versioning.

**Note:** This story assumes Docker setup from Story 1.2 is complete. Database setup will work with containerized PostgreSQL service.

**Acceptance Criteria:**
1. PostgreSQL database is accessible via Docker Compose (local development) or Railway managed Postgres (production)
2. SQLAlchemy 2.0 is configured with asyncpg driver and AsyncSession
3. Database connection pooling is configured
4. Alembic is set up for database migrations
5. Initial migration creates base schema structure
6. Database connection can be established and tested
7. Environment variables for database configuration are properly managed

### Story 1.4: Create Document Model and Basic Persistence Layer

As a developer,  
I want a document data model with persistence operations,  
so that I can store and retrieve uploaded documents in the database.

**Acceptance Criteria:**
1. Document SQLAlchemy model is created with fields: id, content (TEXT), file_name, file_size, source_language, created_at, updated_at
2. Document model does NOT include target_language (since a document can be translated into multiple target languages)
3. Alembic migration creates `documents` table in database
4. Basic CRUD operations are implemented (create, read by id)
5. Document content is stored as TEXT in PostgreSQL
6. File validation constraints are enforced (max size 10MB)
7. Model includes proper indexes and constraints
8. Async database operations work correctly with AsyncSession

**Note:** Translation entities (with target_language and translated_content) will be created in a later story/epic as separate models that reference the document.

### Story 1.5: Implement Document Upload API Endpoint

As a user,  
I want to upload a TXT file through an API endpoint,  
so that I can submit my document for translation.

**Acceptance Criteria:**
1. POST `/documents/upload` endpoint accepts file upload with multipart/form-data
2. Endpoint validates file is TXT format (content-type or extension check)
3. Endpoint validates file size is within 10MB limit
4. File content is extracted and stored in database using document model
5. Endpoint returns document ID and metadata (file_name, file_size) on success
6. Appropriate error responses are returned for invalid files (wrong format, too large, etc.)
7. Endpoint includes proper input validation and error handling
8. API documentation in Swagger shows correct request/response schemas

### Story 1.6: Create Document Upload UI Component

As a user,  
I want to upload a TXT file through a web interface,  
so that I can easily submit my document for translation without using API tools.

**Acceptance Criteria:**
1. Upload component is created using Untitled UI components
2. Component supports drag-and-drop file upload
3. Component displays file validation feedback (format, size)
4. Component shows upload progress indicator
5. Component integrates with TanStack Query for API calls
6. Success state displays file name and size after upload
7. Error states display user-friendly error messages
8. Component follows brand styling (colors, typography) via Tailwind CSS
9. Component is accessible (keyboard navigation, screen reader support)

### Story 1.7: Implement Language Selection UI and API Integration

As a user,  
I want to select source and target languages for translation,  
so that I can specify which languages to translate between.

**Acceptance Criteria:**
1. Language selection component is created using Untitled UI dropdown/select components
2. Component displays list of supported languages: English, Spanish, French
3. Source language and target language are selected independently from the same list
4. Component validates that source and target languages are different (user cannot select the same language for both source and target)
5. Selected languages are stored with document (via API update or during upload)
6. Language selection integrates with document upload flow
7. Component follows brand styling and accessibility requirements
8. Selected languages persist during the session/workflow

### Story 1.8: Configure CI/CD Pipeline

As a developer,  
I want a CI/CD pipeline for automated testing and deployment,  
so that code changes are automatically tested and deployed to Railway.

**Note:** This story depends on Docker setup from Story 1.2. Pipeline will build and deploy Docker images.

**Acceptance Criteria:**
1. CI/CD configuration is set up (GitHub Actions or Railway native)
2. Pipeline runs automated tests (backend and frontend) on pull requests
3. Pipeline builds Docker images on successful tests
4. Pipeline deploys to Railway staging/production environments
5. Environment variables are properly configured in Railway
6. Deployment process is documented
7. Failed deployments are reported with error details
8. Pipeline includes basic security checks (dependencies, secrets)

---

## Epic 2: Translation Processing & Side-by-Side Comparison

**Epic Goal:**
Implement the core translation functionality using OpenAI integration with progress tracking, and deliver the side-by-side comparison view with synchronized scrolling. This enables users to translate their uploaded documents and view the original and translated text side-by-side for efficient review, validating the core value proposition of integrated translation and comparison.

### Story 2.1: Create Translation Model and Persistence Layer

As a developer,  
I want a translation data model that references documents and stores translated content,  
so that I can persist translations and associate them with their source documents.

**Acceptance Criteria:**
1. Translation SQLAlchemy model is created with fields: id, document_id (foreign key), target_language, translated_content (TEXT), status (pending/in_progress/completed/failed), progress_percentage, estimated_time_remaining, created_at, updated_at
2. Translation model has foreign key relationship to Document model
3. Alembic migration creates `translations` table in database with proper indexes
4. Basic CRUD operations are implemented (create, read by id, update status/progress)
5. Translation content is stored as TEXT in PostgreSQL
6. Model supports querying translations by document_id and target_language
7. Async database operations work correctly with AsyncSession
8. Model includes proper constraints (unique constraint on document_id + target_language if needed)

### Story 2.2: Implement OpenAI Translation Service Module

As a developer,  
I want a translation service module that integrates with OpenAI API and preserves original paragraph structure information,  
so that I can translate document content with quality optimization while maintaining alignment capabilities.

**Acceptance Criteria:**
1. `services.translation` package is created with modular structure
2. OpenAI API client is configured with proper authentication
3. Translation function accepts text content, source_language, and target_language
4. Translation includes chunking logic for long documents (split into manageable segments)
5. Translation preserves or tracks original paragraph boundaries for alignment purposes
6. Translation includes additional quality optimization logic beyond basic API calls
7. Service handles API errors and retries appropriately
8. Service implements API rate limit handling (respects rate limits, implements exponential backoff, handles 429 responses)
9. Service includes rate limit monitoring/logging to track API usage and prevent quota exhaustion
10. Service returns translated text with proper formatting preservation
11. Service maintains information about original paragraph structure to support side-by-side alignment
12. Service is designed to be extractable to separate microservice if needed
13. Translation service is testable with mocked OpenAI responses
14. Service supports offline development mode via USE_MOCK_OPENAI environment variable (returns deterministic mock translations for local testing without API costs or rate limits)
15. Mock mode is disabled in production/staging environments (enforced by environment check)

### Story 2.3: Implement Translation API Endpoint with Progress Tracking

As a user,  
I want to initiate translation through an API endpoint that tracks progress,  
so that I can translate my uploaded documents and monitor the translation status.

**Acceptance Criteria:**
1. POST `/translations/create` endpoint accepts document_id and target_language
2. Endpoint validates document exists and target_language is valid
3. Endpoint creates translation record with status "pending"
4. Translation processing happens asynchronously (background task or async processing)
5. Endpoint returns translation_id immediately (non-blocking)
6. GET `/translations/{translation_id}/status` endpoint returns current status, progress_percentage, and estimated_time_remaining
7. Status updates are persisted to database during translation
8. Translation status transitions: pending → in_progress → completed (or failed)
9. Error handling returns appropriate error responses for failures
10. API documentation in Swagger shows correct request/response schemas

### Story 2.4: Implement Translation Progress UI Component

As a user,  
I want to see translation progress with estimated time remaining,  
so that I know how long the translation will take for long documents.

**Acceptance Criteria:**
1. Progress component is created using Untitled UI components
2. Component displays progress percentage (progress bar or similar)
3. Component displays estimated time remaining (e.g., "Estimated time: 2 minutes remaining")
4. Component polls translation status endpoint at appropriate intervals
5. Component shows "Translating..." status message
6. Component transitions to comparison view when translation completes
7. Component handles error states with user-friendly error messages
8. Component integrates with TanStack Query for status polling
9. Component follows brand styling and accessibility requirements
10. Component does NOT show paragraph-by-paragraph progress (only overall progress and time estimate)

### Story 2.5: Create Side-by-Side Comparison View Layout

As a user,  
I want to view original and translated text side-by-side in two columns,  
so that I can compare the original and translation efficiently.

**Acceptance Criteria:**
1. Side-by-side layout component is created using Untitled UI components
2. Layout displays original text in left column (read-only)
3. Layout displays translated text in right column (read-only initially, editable in next story)
4. Both columns are scrollable independently
5. Layout is responsive and works on desktop/tablet (mobile optimization deferred)
6. Layout includes proper spacing and typography following brand guidelines
7. Component receives document content and translation content as props
8. Component handles loading states while fetching content
9. Component follows accessibility requirements (keyboard navigation, screen reader support)
10. Layout transforms from progress view when translation completes

### Story 2.6: Implement Synchronized Scrolling Between Columns

As a user,  
I want synchronized scrolling between original and translated text columns,  
so that corresponding paragraphs stay aligned while I scroll.

**Acceptance Criteria:**
1. Synchronized scrolling is implemented between left and right columns
2. Scrolling one column automatically scrolls the other to keep paragraphs aligned
3. Paragraph alignment is based on original document's paragraph boundaries (original text structure dictates alignment)
4. Even if translated text has different paragraph breaks (e.g., 3 \n in translation vs. 1 in original), alignment follows original paragraph structure
5. Scrolling performance is smooth (60fps) even for long documents (up to 100 pages)
6. Synchronization works in both directions (scrolling left affects right, scrolling right affects left)
7. Scrolling handles edge cases (beginning/end of document, different content lengths, translation paragraph breaks that don't match original)
8. Performance is optimized for documents up to 100 pages
9. Scrolling does not cause layout shifts or visual glitches

### Story 2.7: Add Paragraph Markers for Navigation

As a user,  
I want paragraph markers in the side-by-side view based on the original document structure,  
so that I can navigate between paragraphs and see alignment between original and translated text.

**Acceptance Criteria:**
1. Paragraph markers are based on the original document's paragraph structure (original text dictates marker placement)
2. Markers are displayed in both columns, but alignment follows original paragraph boundaries
3. If translation splits a single original paragraph into multiple paragraphs (e.g., 3 \n in translation), they still align to the single original paragraph marker
4. Markers indicate paragraph boundaries clearly based on original structure
5. Markers help users identify corresponding content between columns, even when translation has different paragraph breaks
6. Markers are visually distinct but not intrusive
7. Markers are accessible (visible to screen readers, keyboard navigable)
8. Markers work with synchronized scrolling (scrolling aligns to original paragraph boundaries)
9. Markers are styled consistently with brand guidelines
10. Markers handle edge cases (single paragraph documents, very long paragraphs, mismatched paragraph breaks between original and translation)

**Note:** The original document's paragraph structure is the source of truth for alignment. Translation paragraph breaks may differ, but markers and scrolling alignment follow the original structure.

---

## Epic 3: Editing, Progress Saving & Export

**Epic Goal:**
Implement in-place editing capabilities with auto-save, progress saving and resume functionality for long documents, and download/export capability. This enables users to edit translations directly in the comparison view, save their progress for long documents, and export the final translated text, completing the core MVP workflow and delivering the full integrated review experience.

### Story 3.1: Implement In-Place Editing in Comparison View

As a user,  
I want to edit translated text directly in the side-by-side comparison view,  
so that I can make corrections and refinements without switching to external tools.

**Acceptance Criteria:**
1. Translated text column in comparison view becomes editable (original text remains read-only)
2. Editing uses plain text editing (no markdown rendering in MVP)
3. Users can click on translated text to edit it directly in place
4. Editing preserves paragraph alignment with original text (editing doesn't break alignment)
5. Edited content is visually distinct (e.g., shows as modified/unsaved)
6. Editing works smoothly with synchronized scrolling
7. Component uses Untitled UI editable components or textarea/input components
8. Editing follows brand styling and accessibility requirements
9. Keyboard navigation works correctly in edit mode
10. Editing handles edge cases (very long paragraphs, special characters, line breaks)

### Story 3.2: Implement Auto-Save for Edited Translations

As a user,  
I want my edits to be automatically saved,  
so that I don't lose my work and don't need to manually save changes.

**Acceptance Criteria:**
1. Auto-save functionality saves edited translation content automatically
2. Auto-save triggers after a debounce period (e.g., 2-3 seconds after user stops typing)
3. Auto-save updates translation record in database via API endpoint
4. Visual indicator shows save status (saving, saved, error)
5. Auto-save works reliably without disrupting user editing experience
6. Failed saves are retried automatically with user notification if retries fail
7. Auto-save integrates with TanStack Query for API calls
8. Save status indicator is unobtrusive but visible
9. Auto-save handles network errors gracefully
10. Edited content persists across page refreshes (if user navigates away and returns)

### Story 3.3: Implement Translation Progress Saving

As a user,  
I want to save translation progress for long documents,  
so that I can pause and resume translation work on lengthy content.

**Acceptance Criteria:**
1. Translation progress is saved automatically during translation processing
2. Progress includes: current chunk/segment being translated, percentage complete, translated content so far
3. Progress is persisted to database (stored in translation record or separate progress table)
4. Progress saving happens incrementally (not just at completion)
5. Progress saving has <1 second save/load time as per NFR
6. Progress data is stored efficiently (JSON field or normalized structure)
7. Progress saving works reliably for documents up to 100 pages
8. Progress is associated with specific document_id and target_language combination
9. Progress can be queried and retrieved via API endpoint

### Story 3.4: Implement Translation Resume Functionality

As a user,  
I want to resume an interrupted translation,  
so that I can continue translating long documents from where I left off.

**Acceptance Criteria:**
1. Resume functionality detects incomplete translations (status: in_progress or failed)
2. Resume endpoint accepts translation_id and continues from saved progress
3. Resume functionality loads saved progress (translated content, current position)
4. Translation continues from last saved chunk/segment
5. Resume works correctly even if translation was interrupted mid-chunk
6. Resume functionality has 90%+ success rate for documents >10 pages (per NFR)
7. Resume handles edge cases (corrupted progress, missing chunks, network interruptions)
8. User can manually trigger resume via UI (e.g., "Resume Translation" button)
9. Resume status is clearly communicated to user
10. Resume functionality integrates with translation progress UI

### Story 3.5: Create Download/Export API Endpoint

As a user,  
I want to download my translated document as a TXT file,  
so that I can use the final translation outside the application.

**Acceptance Criteria:**
1. GET `/translations/{translation_id}/download` endpoint returns translated content as TXT file
2. Endpoint validates translation exists and is completed
3. Endpoint returns file with appropriate Content-Type header (text/plain)
4. Endpoint returns file with appropriate Content-Disposition header (filename)
5. Filename is derived from original document name (e.g., "document_translated.txt")
6. Endpoint handles error cases (translation not found, translation incomplete)
7. Endpoint returns appropriate HTTP status codes
8. Translated content includes all user edits (final edited version, not just raw translation)
9. API documentation in Swagger shows correct response schema

### Story 3.6: Implement Download/Export UI Component

As a user,  
I want to download my translated document through the web interface,  
so that I can easily export the final translation.

**Acceptance Criteria:**
1. Download button/component is created using Untitled UI components
2. Component is integrated into comparison view (header/toolbar area)
3. Component triggers download API call when clicked
4. Component shows download state (downloading, complete, error)
5. Component handles file download in browser (triggers browser download)
6. Component displays user-friendly error messages if download fails
7. Component is accessible (keyboard navigable, screen reader support)
8. Component follows brand styling
9. Component is visible and accessible from comparison view
10. After download, user remains in comparison view (can continue editing if needed)

### Story 3.7: Implement Progress Saving for Edited Content

As a user,  
I want my editing progress to be saved,  
so that I can resume editing long documents even if I close the browser.

**Acceptance Criteria:**
1. Edited translation content is saved to database (updates translation record)
2. Save includes full edited content, not just changes/diffs
3. Edited content persists across browser sessions (if user closes and reopens)
4. Resume editing loads last saved edited content
5. Progress saving for edits works in conjunction with translation progress saving
6. Edited content is stored efficiently in database
7. Save/load operations have acceptable performance (<1 second as per NFR)
8. Edited content is associated with specific translation_id
9. System distinguishes between raw translation and edited translation
10. User can see when content was last saved

---

## Checklist Results Report

### Executive Summary

**Overall PRD Completeness:** 85%  
**MVP Scope Appropriateness:** Just Right  
**Readiness for Architecture Phase:** Ready  
**Most Critical Gaps:** Minor clarifications needed on authentication scope and language support details

The PRD is comprehensive and well-structured, with clear problem definition, well-scoped MVP features, detailed requirements, and complete epic/story breakdown. The document demonstrates strong alignment between problem statement, solution approach, and technical implementation. Minor gaps exist in authentication scope clarification (FR11 mentions authentication but it's marked post-MVP in technical assumptions) and specific language pairs supported.

### Category Analysis

| Category                         | Status | Critical Issues |
| -------------------------------- | ------ | --------------- |
| 1. Problem Definition & Context  | PASS   | None            |
| 2. MVP Scope Definition          | PASS   | None            |
| 3. User Experience Requirements  | PASS   | None            |
| 4. Functional Requirements       | PASS   | Minor: FR11 scope clarification needed |
| 5. Non-Functional Requirements  | PASS   | None            |
| 6. Epic & Story Structure        | PASS   | None            |
| 7. Technical Guidance            | PASS   | None            |
| 8. Cross-Functional Requirements | PARTIAL | Authentication scope needs clarification |
| 9. Clarity & Communication       | PASS   | None            |

### Detailed Category Analysis

#### 1. Problem Definition & Context: PASS (95%)

**Strengths:**
- Clear problem statement with quantified impact (30-50% overhead, 2-4 hours vs 1-2 hours)
- Well-defined target users (academics/researchers primary, writers secondary, SMBs tertiary)
- Comprehensive competitive analysis showing gaps in existing solutions
- Quantified market opportunity ($500M-$1B SAM)
- Clear urgency and importance justification

**Minor Gaps:**
- User research findings could be more explicitly referenced (though present in Project Brief)
- Baseline measurements for success metrics could be more specific

**Recommendation:** No blockers. PRD references Project Brief which contains detailed user research.

#### 2. MVP Scope Definition: PASS (90%)

**Strengths:**
- Clear distinction between core features and out-of-scope items
- MVP scope is truly minimal (TXT only, no markdown rendering, no team features)
- Each feature directly addresses the problem statement
- Clear rationale for scope decisions
- MVP success criteria are measurable and specific

**Minor Gaps:**
- Could benefit from explicit "nice-to-have" vs "must-have" prioritization within MVP
- Timeline expectations could be more explicit (though implied in Epic structure)

**Recommendation:** No blockers. Scope is appropriately minimal and well-justified.

#### 3. User Experience Requirements: PASS (90%)

**Strengths:**
- Core screens and views clearly defined
- User flows are implicit in epic/story structure (upload → translate → compare → edit → download)
- Accessibility requirements specified (WCAG AA)
- Performance expectations from user perspective defined
- Branding guidelines comprehensive

**Minor Gaps:**
- Primary user flows could be explicitly documented as flow diagrams or step-by-step
- Error handling approaches could be more detailed (though mentioned in NFR12)
- Edge cases in user flows could be more explicitly called out

**Recommendation:** No blockers. UX requirements are comprehensive. Flow documentation can be added during architecture phase.

#### 4. Functional Requirements: PASS (95%)

**Strengths:**
- All required features for MVP documented (14 functional requirements)
- Requirements are testable and verifiable
- Requirements focus on WHAT not HOW
- Consistent terminology throughout
- Clear acceptance criteria in stories

**Critical Issue:**
- **FR11** mentions "user authentication (email-based with code/magic-link via Resend)" but Technical Assumptions section notes "Authentication (Post-MVP): Custom FastAPI implementation with Resend" and "email code/magic-link authentication (post-MVP, not part of MVP)". This is a scope contradiction that needs resolution.

**Recommendation:** **HIGH PRIORITY** - Clarify authentication scope. If authentication is needed for progress saving (FR12), it should be in MVP. If not, FR11 should be removed or marked post-MVP.

#### 5. Non-Functional Requirements: PASS (95%)

**Strengths:**
- Performance requirements clearly defined (14 NFRs)
- Response time expectations specified (<30 seconds for 10-page doc, <3 seconds for comparison view)
- Security requirements comprehensive (encryption, GDPR, authentication)
- Reliability requirements specified (90%+ success rate for resume, zero critical bugs)
- Technical constraints clearly documented

**Minor Gaps:**
- Scalability needs could be more explicit (though future considerations are mentioned)
- Load handling expectations could be quantified (concurrent users)

**Recommendation:** No blockers. NFRs are comprehensive and measurable.

#### 6. Epic & Story Structure: PASS (95%)

**Strengths:**
- Epics represent cohesive units of functionality
- Epics focus on user/business value delivery
- Epic goals clearly articulated
- Stories are appropriately sized (2-4 hours each)
- Stories have clear, independent value
- Acceptance criteria are testable and comprehensive
- Story dependencies and sequence documented
- First epic includes all necessary setup steps

**Minor Gaps:**
- Some stories could benefit from local testability requirements (e.g., CLI testing for backend stories)
- Story 1.7 mentions "supported language pairs (to be determined)" - should be specified before development

**Recommendation:** No blockers. Epic/story structure is excellent. Language pairs should be specified before Epic 1 development begins.

#### 7. Technical Guidance: PASS (95%)

**Strengths:**
- Architecture direction clearly provided (Monolith with modular design)
- Technical constraints clearly communicated (FastAPI, Next.js, PostgreSQL, Untitled UI)
- Integration points identified (OpenAI, Resend, Railway)
- Performance considerations highlighted
- Security requirements articulated
- Technical decision rationale provided

**Minor Gaps:**
- Areas of high complexity could be explicitly flagged (e.g., synchronized scrolling, paragraph alignment)
- Technical debt approach could be more explicit

**Recommendation:** No blockers. Technical guidance is comprehensive. Architecture phase can identify complexity areas.

#### 8. Cross-Functional Requirements: PARTIAL (75%)

**Strengths:**
- Data entities and relationships identified (Document, Translation models)
- Data storage requirements specified (PostgreSQL, TEXT columns)
- External system integrations identified (OpenAI, Resend)
- API requirements documented (RESTful with OpenAPI/Swagger)
- Future authentication integration considered (user_id fields nullable for MVP)

**Critical Issues:**
- ~~**Authentication scope contradiction**~~ **RESOLVED:** Authentication is post-MVP, but system designed to allow future integration
- ~~Language pairs supported not specified~~ **RESOLVED:** English, Spanish, French (cannot select same language for both sides)
- Data retention policies not specified
- Schema change approach not explicitly tied to stories

**Recommendation:** **HIGH PRIORITY** - Resolve authentication scope. **MEDIUM PRIORITY** - Specify supported language pairs and data retention policies.

#### 9. Clarity & Communication: PASS (95%)

**Strengths:**
- Documents use clear, consistent language
- Documents are well-structured and organized
- Technical terms are defined where necessary
- Documentation is versioned (Change Log included)
- Rationale provided for key decisions

**Minor Gaps:**
- Could benefit from diagrams/visuals (user flows, architecture diagrams)
- Some sections reference Project Brief - could include key excerpts

**Recommendation:** No blockers. Documentation quality is excellent. Visuals can be added during architecture phase.

### Top Issues by Priority

#### BLOCKERS: None

No issues that block architect from proceeding.

#### HIGH PRIORITY

1. ~~**Authentication Scope Contradiction**~~ **RESOLVED**
   - **Resolution:** Authentication is post-MVP. System will use session-based document management for MVP. Data model and API design must support future authentication integration (user_id fields nullable for MVP).

2. ~~**Language Pairs Specification**~~ **RESOLVED**
   - **Resolution:** Supported languages for MVP: English, Spanish, French. Users cannot select the same language for both source and target. Language selection component validates this constraint.

#### MEDIUM PRIORITY

3. **Data Retention Policies**
   - **Issue:** No explicit data retention or deletion policies specified
   - **Impact:** GDPR compliance and user data management unclear
   - **Recommendation:** Specify data retention period (e.g., 90 days for free tier, 1 year for paid) and deletion policies

4. **User Flow Documentation**
   - **Issue:** Primary user flows are implicit but not explicitly documented
   - **Impact:** UX Expert may need to infer flows from stories
   - **Recommendation:** Add explicit user flow section or ensure UX Expert has access to Project Brief

#### LOW PRIORITY

5. **Visual Diagrams**
   - **Issue:** No architecture or flow diagrams included
   - **Impact:** Minor - diagrams helpful but not essential
   - **Recommendation:** Add during architecture phase

6. **Concurrent User Load Specification**
   - **Issue:** NFR11 mentions "concurrent translation requests" but doesn't quantify
   - **Impact:** Minor - can be specified during architecture
   - **Recommendation:** Specify expected concurrent user load (e.g., 50-100 concurrent translations)

### MVP Scope Assessment

**Features That Might Be Cut for True MVP:**
- None identified - current scope is appropriately minimal

**Missing Features That Are Essential:**
- None identified - all essential features are included

**Complexity Concerns:**
- Synchronized scrolling with paragraph alignment (Story 2.6) - technically complex but core differentiator
- Progress saving and resume (Stories 3.3, 3.4) - complex but essential for long documents
- Paragraph alignment based on original structure (Story 2.7) - requires careful implementation

**Timeline Realism:**
- 3 epics with 22 stories total
- Estimated 44-88 hours of development work (2-4 hours per story)
- Timeline appears realistic for MVP scope
- First epic (infrastructure) may take longer than estimated

### Technical Readiness

**Clarity of Technical Constraints:** Excellent
- All major technology choices specified
- Constraints clearly communicated
- Rationale provided for key decisions

**Areas of High Complexity (Explicitly Flagged):**

1. **Synchronized Scrolling with Paragraph Alignment (Story 2.6, 2.7)**
   - **Complexity:** High - Requires real-time synchronization between two scrollable columns while maintaining paragraph alignment based on original document structure
   - **Technical Challenges:** 
     - Performance optimization for 100-page documents (60fps requirement)
     - Paragraph boundary detection and mapping
     - Handling mismatched paragraph breaks between original and translation
     - Virtual scrolling vs. full DOM rendering trade-offs
   - **Risk Level:** High - Core differentiator, technically complex
   - **Recommendation:** Architect should investigate implementation approaches early, consider virtual scrolling libraries, prototype performance early

2. **Progress Saving and Resume Functionality (Stories 3.3, 3.4)**
   - **Complexity:** High - Requires reliable state persistence and recovery for long-running translations
   - **Technical Challenges:**
     - Incremental progress saving during translation processing
     - Resume from mid-chunk interruption
     - Data structure design (JSON field vs. normalized chunks table)
     - 90%+ success rate requirement for documents >10 pages
   - **Risk Level:** High - Essential for long documents, complex edge cases
   - **Recommendation:** Architect should design robust data model and error recovery mechanisms

3. **Paragraph Alignment Algorithm (Story 2.7)**
   - **Complexity:** High - Original document structure must dictate alignment even when translation has different paragraph breaks
   - **Technical Challenges:**
     - Mapping original paragraph boundaries to translated content
     - Handling cases where translation splits/merges paragraphs
     - Maintaining alignment during editing
   - **Risk Level:** High - Core UX feature, algorithmically complex
   - **Recommendation:** Architect should design and prototype alignment algorithm early

**Identified Technical Risks:**
1. Synchronized scrolling performance for 100-page documents
2. Paragraph alignment algorithm complexity
3. Progress saving/resume reliability for long documents
4. OpenAI API rate limits and cost management
5. Database performance with large TEXT fields

**Areas Needing Architect Investigation:**
1. Synchronized scrolling implementation approach (virtual scrolling vs. full DOM)
2. Paragraph boundary detection and alignment algorithm
3. Progress saving data structure (JSON field vs. normalized chunks table)
4. Translation chunking strategy for long documents
5. Database schema optimization for large text storage
6. Future authentication integration points (user_id fields, API design)

### Recommendations

**Immediate Actions (Before Architecture Phase):**
1. ~~**Resolve authentication scope**~~ **COMPLETED** - Authentication is post-MVP, system designed for future integration
2. ~~**Specify language pairs**~~ **COMPLETED** - English, Spanish, French (cannot select same for both sides)
3. **Clarify data retention** - Specify retention policies for GDPR compliance (can be done during architecture phase)

**During Architecture Phase:**
1. **HIGH PRIORITY:** Investigate synchronized scrolling implementation approaches (virtual scrolling vs. full DOM)
2. **HIGH PRIORITY:** Design paragraph alignment algorithm (original structure as source of truth)
3. **HIGH PRIORITY:** Design progress saving data structure and resume mechanism
4. Optimize database schema for large text storage
5. Plan translation chunking strategy
6. Design data model to support future authentication (user_id fields, nullable for MVP)

**For UX Expert:**
1. Review Project Brief for detailed user research
2. Create explicit user flow diagrams
3. Design error state handling
4. Plan mobile responsive layout strategy

**For Development:**
1. Establish local testability requirements for backend stories
2. Set up development environment early (Epic 1, Story 1.1) and Docker containerization (Story 1.2)
3. Plan for technical debt (synchronized scrolling, paragraph alignment)

### Final Decision

**READY FOR ARCHITECT**: The PRD and epics are comprehensive, properly structured, and ready for architectural design. All critical clarifications have been resolved. The document is ready for architecture phase.

**Next Steps:**
1. ✅ Authentication scope resolved - post-MVP with future integration support
2. ✅ Language pairs specified - English, Spanish, French
3. Proceed to architecture phase
4. UX Expert can begin work in parallel with architecture
5. Architect should prioritize investigation of high-complexity areas (synchronized scrolling, paragraph alignment, progress saving)

---

## Next Steps

### UX Expert Prompt

Create a front-end specification document for Librilabs Translator using the PRD at `docs/prd.md` as input. Focus on the core screens (Upload, Translation Progress, Side-by-Side Comparison/Edit, Download) and ensure the design addresses the high-complexity areas: synchronized scrolling with paragraph alignment, progress saving UI, and in-place editing. Use Untitled UI components exclusively and follow the brand guidelines specified in the PRD. Pay special attention to the paragraph alignment requirements where the original document structure dictates alignment, not the translation structure.

**Command:** `@ux-expert *create-front-end-spec`

### Architect Prompt

Create a full-stack architecture document for Librilabs Translator using the PRD at `docs/prd.md` as input. Prioritize investigation of the high-complexity areas flagged in the PRD: synchronized scrolling implementation, paragraph alignment algorithm, and progress saving data structure. Design the system to support future authentication integration (user_id fields nullable for MVP). Ensure the architecture supports the monolith FastAPI + Next.js structure with PostgreSQL, and addresses performance requirements for documents up to 100 pages.

**Command:** `@architect *create-full-stack-architecture`

