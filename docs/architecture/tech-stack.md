# Tech Stack

This is the DEFINITIVE technology selection for the entire project. All development must use these exact technologies and versions.

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| Frontend Language | TypeScript | Latest stable | Type-safe frontend development | Provides compile-time error checking, improves developer experience, and ensures type safety across the React codebase |
| Frontend Framework | Next.js | 16.0.4 | React framework with SSR capabilities | Provides server-side rendering, optimized routing, and built-in performance optimizations. Note: Current frontend uses 14.2.5 - upgrade required |
| UI Component Library | Untitled UI | Latest | All UI components | Exclusively used to maintain design consistency and reduce maintenance burden. No custom components allowed per PRD |
| State Management | TanStack Query | Latest | Server state management | Handles API data caching, loading/error states, retries, and pagination automatically. Reduces boilerplate and improves UX |
| State Management (UI) | React useState/useReducer or Zustand | Latest | Local/UI state | Minimal approach for cross-page UI state (selected document, modals). Zustand optional for complex state needs |
| Form Handling | React Hook Form | Latest | Form management | Lightweight, TypeScript-friendly, good performance, works well with Untitled UI components |
| CSS Framework | Tailwind CSS | Latest | Styling | Apply brand colors and typography through Tailwind configuration to match Untitled UI design system |
| Backend Language | Python | Latest stable | Backend development | Modern Python version with latest features. FastAPI requires Python 3.8+ |
| Backend Framework | FastAPI | Latest | REST API framework | High-performance async framework, automatic OpenAPI/Swagger documentation, type hints support, excellent for latest stable Python |
| API Style | REST | N/A | API architecture | Standard RESTful endpoints organized by resource. FastAPI provides automatic OpenAPI documentation |
| Database | PostgreSQL | Latest (Railway managed) | Primary data store | Relational database for structured data. Railway managed provides automatic backups, connection pooling, high availability |
| Database ORM | SQLAlchemy | 2.0 | Database abstraction | Declarative mappings with AsyncSession support. Enables async database operations with asyncpg driver |
| Database Driver | asyncpg | Latest | PostgreSQL async driver | High-performance async PostgreSQL driver for SQLAlchemy AsyncSession |
| Database Migrations | Alembic | Latest | Schema versioning | Standard migration tool for SQLAlchemy, enables version-controlled database schema changes |
| Cache | None (MVP) | N/A | Caching layer | No caching layer for MVP. Can add Redis post-MVP if needed for performance optimization |
| File Storage | PostgreSQL TEXT | N/A | Document storage | TXT content stored directly in PostgreSQL for MVP simplicity. Max file size ~10MB |
| Authentication | Session-based (MVP) | N/A | User sessions | Anonymous session management for MVP. Post-MVP: Custom FastAPI + Resend (email code/magic-link + JWT) |
| Frontend Testing | Vitest | Latest | Unit/integration testing | Fast unit testing for React components. Vite-based for speed |
| Frontend Testing | React Testing Library | Latest | Component testing | Testing utilities for React components, works with Vitest |
| Frontend Testing | Playwright | Latest | E2E testing | End-to-end testing for critical user workflows (upload → translate → edit → download) |
| Backend Testing | Pytest | Latest | Unit/integration testing | Standard Python testing framework, excellent FastAPI integration |
| Backend Testing | httpx | Latest | API testing | Async HTTP client for testing FastAPI endpoints, provides test client functionality |
| E2E Testing | Playwright | Latest | End-to-end testing | Same tool used for frontend E2E testing, provides full browser automation |
| Build Tool | Next.js built-in | 16.0.4 | Frontend build | Next.js provides built-in build system with optimizations |
| Build Tool | Python build tools | Standard | Backend build | Standard Python packaging (setuptools, pip) for FastAPI application |
| Bundler | Next.js Webpack/Turbopack | 16.0.4 | Frontend bundling | Next.js handles bundling internally. Turbopack (experimental) may be available in 16.0.4 |
| IaC Tool | Docker | Latest | Containerization | Docker containers for consistent deployments across environments. Railway uses Docker for deployments |
| CI/CD | Railway GitHub Integration | N/A | Continuous deployment | Railway's built-in GitHub integration for automated deployments. Additional CI can use GitHub Actions if needed |
| Monitoring | TBD (Post-MVP) | N/A | Application monitoring | Monitoring solution to be determined post-MVP. Options: Railway metrics, external services (Sentry, Datadog) |
| Logging | Python logging + Railway logs | Standard | Application logging | Python standard logging library. Railway provides log aggregation and viewing |

**Note:** Current frontend package.json shows Next.js 14.2.5 and React 18.3.1. The frontend must be upgraded to Next.js 16.0.4 and React 19 to match this tech stack.

---
