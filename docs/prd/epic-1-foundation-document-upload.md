# Epic 1: Foundation & Document Upload

**Epic Goal:**
Establish the foundational infrastructure for the application (FastAPI backend, PostgreSQL database, Docker containerization, CI/CD pipeline) and deliver the document upload and language selection functionality. This enables users to upload TXT files and select source/target languages, providing the foundation for the translation workflow while validating the core infrastructure setup.

## Story 1.0: Upgrade Frontend and Set Up Testing Infrastructure

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

## Story 1.1: Set Up FastAPI Backend Structure with Health Check

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

## Story 1.2: Set Up Docker and Deployment Configuration

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

## Story 1.3: Set Up PostgreSQL Database with SQLAlchemy and Alembic

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

## Story 1.4: Create Document Model and Basic Persistence Layer

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

## Story 1.5: Implement Document Upload API Endpoint

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

## Story 1.6: Create Document Upload UI Component

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

## Story 1.7: Implement Language Selection UI and API Integration

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

## Story 1.8: Configure CI/CD Pipeline

As a developer,  
I want a CI/CD pipeline for automated testing and deployment,  
so that code changes are automatically tested and deployed to Railway.

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
