# System-Level Test Design

**Date:** 2025-01-27  
**Author:** Librilabs  
**Status:** Draft  
**Project:** librilabs-translator  
**Phase:** Solutioning (Phase 2)

---

## Executive Summary

This document provides a system-level testability review for the Librilabs Translator application. The assessment evaluates architecture decisions against testability criteria (controllability, observability, reliability), identifies architecturally significant requirements (ASRs), defines test levels strategy, and outlines NFR testing approaches. This review informs the solutioning gate check and guides test framework setup in Sprint 0.

**Key Findings:**
- **Testability Status:** PASS with minor concerns
- **Critical ASRs:** 3 identified (Performance, Security, Reliability)
- **Test Levels Strategy:** 40% Unit, 30% Integration, 30% E2E
- **Testability Concerns:** 2 minor concerns (OpenAI API mocking, async translation testing)

---

## Testability Assessment

### Controllability: PASS

**Assessment:** System state can be controlled for testing through multiple mechanisms.

**Strengths:**
- ✅ **Database Control:** SQLAlchemy with AsyncSession enables test database setup/teardown via Alembic migrations
- ✅ **API Seeding:** FastAPI test client (httpx) allows direct API calls for data setup (faster than UI)
- ✅ **Dependency Injection:** FastAPI dependencies enable mocking of external services (OpenAI API, Resend)
- ✅ **Session Management:** Session-based architecture allows test isolation via unique session_ids
- ✅ **Repository Pattern:** Data access layer abstracted through repositories (testable with in-memory DB)

**Evidence:**
- Backend architecture uses repository pattern (`DocumentRepository`, `TranslationRepository`)
- FastAPI dependencies (`get_db`, `get_session_id`) can be overridden in tests
- Database models support test fixtures via SQLAlchemy factories
- Frontend uses TanStack Query with mockable API client

**Recommendations:**
- Create test factories for Document and Translation models (faker-based, auto-cleanup)
- Implement test database fixtures with auto-rollback (pytest fixtures)
- Document OpenAI API mocking strategy (use `responses` library or mock OpenAI client)

---

### Observability: CONCERNS

**Assessment:** System state can be inspected, but some gaps exist for NFR validation.

**Strengths:**
- ✅ **API Response Inspection:** FastAPI test client provides full response inspection (status, body, headers)
- ✅ **Database State:** SQLAlchemy queries allow direct database state validation
- ✅ **Frontend State:** React Testing Library enables component state inspection
- ✅ **Error Responses:** Structured error responses with codes and messages

**Concerns:**
- ⚠️ **Performance Metrics:** No built-in performance monitoring (response times, throughput) - requires k6 for load testing
- ⚠️ **Translation Progress:** Async translation progress tracking exists, but testability depends on polling implementation
- ⚠️ **Health Check:** `/health` endpoint exists but may need expansion for comprehensive service monitoring

**Evidence:**
- Health check endpoint documented in architecture (`/health`)
- Translation progress stored in database (`progress_percentage` field)
- No APM (Application Performance Monitoring) tools specified in architecture

**Recommendations:**
- Expand `/health` endpoint to include database connectivity, OpenAI API status, and service dependencies
- Add Server-Timing headers to API responses for performance validation in tests
- Implement structured logging with correlation IDs (trace IDs) for request tracing
- Document k6 load testing setup for performance NFR validation

---

### Reliability: PASS

**Assessment:** Tests can be isolated and run in parallel without state pollution.

**Strengths:**
- ✅ **Test Isolation:** Session-based architecture enables parallel test execution (unique session_ids per test)
- ✅ **Database Isolation:** Test database fixtures with rollback prevent state pollution
- ✅ **Stateless Design:** API endpoints are stateless (except session_id), enabling parallel execution
- ✅ **Cleanup Mechanisms:** Repository pattern supports explicit cleanup operations

**Evidence:**
- Backend uses async operations with AsyncSession (no shared state)
- Frontend components are stateless (TanStack Query manages server state)
- Docker Compose setup allows isolated test environments

**Recommendations:**
- Implement test fixtures with auto-cleanup (pytest fixtures with `yield` for teardown)
- Use faker for unique test data generation (prevent parallel collisions)
- Document parallel test execution strategy (Playwright workers, pytest-xdist)

---

## Architecturally Significant Requirements (ASRs)

ASRs are quality requirements that drive architecture decisions and pose testability challenges. Each ASR is scored using risk matrix (probability × impact).

### ASR-001: Translation Performance (Score: 6 - HIGH)

**Requirement:** Translation must complete for documents up to 50 pages within 5 minutes under normal load conditions (NFR1).

**Architecture Impact:**
- Drives async translation processing (prevents blocking API requests)
- Requires chunking strategy for large documents (OpenAI token limits)
- Progress tracking needed for user feedback

**Testability Challenges:**
- Async processing requires polling mechanism testing
- Large document testing (50 pages = ~25,000 words) requires realistic test data
- Performance testing requires k6 load testing (not Playwright)

**Risk Score:** Probability: 2 (Possible - async processing complexity), Impact: 3 (Critical - core feature)

**Mitigation Strategy:**
- Implement k6 load tests for translation endpoint (50 concurrent requests)
- Create test data factories for large documents (10, 25, 50 pages)
- Mock OpenAI API responses for deterministic testing (use `responses` library)
- Validate progress tracking accuracy (polling interval, progress percentage)

**Owner:** QA Lead  
**Timeline:** Sprint 0 (test framework setup)

---

### ASR-002: Security - Session Isolation (Score: 6 - HIGH)

**Requirement:** System must ensure all user data and documents are securely stored and transmitted using industry-standard encryption (NFR9). Session-based document management for MVP (NFR8).

**Architecture Impact:**
- Session-based authentication (session_id header) for MVP
- Database queries filter by session_id (prevent cross-session access)
- Future JWT authentication support (post-MVP)

**Testability Challenges:**
- Session isolation testing (verify users cannot access other sessions' documents)
- Security testing requires OWASP validation (SQL injection, XSS)
- Rate limiting testing (100 req/min general, 10 req/min translation, 5 req/min upload)

**Risk Score:** Probability: 2 (Possible - session management complexity), Impact: 3 (Critical - security breach)

**Mitigation Strategy:**
- E2E tests for session isolation (Playwright: attempt cross-session document access)
- Security tests for OWASP Top 10 (SQL injection, XSS, CSRF)
- Rate limiting tests (verify 429 responses after threshold)
- Input validation tests (Pydantic schema validation)

**Owner:** Security Team / QA Lead  
**Timeline:** Sprint 0 (security test suite)

---

### ASR-003: Reliability - Progress Saving (Score: 4 - MEDIUM)

**Requirement:** Progress saving and resume operations must have a 90%+ success rate for documents greater than 10 pages (NFR3).

**Architecture Impact:**
- Auto-save with debouncing (2 seconds) for editing workflow
- Database persistence for translation state (JSON field)
- Resume functionality requires session_id persistence

**Testability Challenges:**
- Auto-save timing testing (debounce behavior, network failures)
- Resume functionality testing (session persistence across browser sessions)
- Large document state persistence (JSON field size limits)

**Risk Score:** Probability: 2 (Possible - async save complexity), Impact: 2 (Degraded - feature impaired)

**Mitigation Strategy:**
- E2E tests for auto-save behavior (Playwright: edit, wait, verify save)
- Resume tests (simulate browser close/reopen, verify state restoration)
- Database state validation (verify translation_state JSON persistence)
- Error handling tests (network failures during save, retry logic)

**Owner:** QA Lead  
**Timeline:** Epic 3 (Editing, Progress Saving & Export)

---

## Test Levels Strategy

Based on architecture (monolith FastAPI + Next.js frontend, API-heavy with async processing):

### Recommended Split: 40% Unit, 30% Integration, 30% E2E

**Rationale:**
- **40% Unit Tests:** Business logic (translation chunking, text parsing, validation), pure functions
- **30% Integration Tests:** API endpoints (FastAPI routers), database operations (repositories), service layer
- **30% E2E Tests:** Critical user journeys (upload → translate → compare → edit → download), cross-system workflows

**Test Level Breakdown:**

| Level | Scope | Tools | Examples |
|-------|-------|-------|----------|
| **Unit** | Business logic, utilities, pure functions | Vitest (frontend), Pytest (backend) | `chunking.py`, `fileValidation.ts`, `priceCalculator.ts` |
| **Integration** | API endpoints, database operations, service layer | Pytest + httpx (backend), Playwright API (frontend) | `test_documents.py`, `test_translations.py`, `test_repositories.py` |
| **E2E** | Complete user journeys, cross-system workflows | Playwright | `upload-workflow.spec.ts`, `translation-workflow.spec.ts`, `editing-workflow.spec.ts` |

**Technology-Specific Testing:**
- **Frontend (Next.js):** Playwright for E2E, Vitest + React Testing Library for components
- **Backend (FastAPI):** Pytest + httpx for API tests, Pytest for unit tests
- **Database (PostgreSQL):** Integration tests with test database (Docker Compose)
- **Performance:** k6 for load/stress testing (NOT Playwright)

**Avoid Duplicate Coverage:**
- Don't test business logic at E2E level (use unit tests)
- Don't test API contracts at E2E level (use integration tests)
- Use E2E only for critical user journeys (upload → translate → edit → download)

---

## NFR Testing Approach

### Security NFR Testing

**Approach:** Playwright E2E tests + Security tools (OWASP ZAP, npm audit)

**Test Coverage:**
- **Authentication/Authorization:** Session isolation (users cannot access other sessions' documents)
- **Input Validation:** SQL injection, XSS, file upload validation
- **Rate Limiting:** Verify 429 responses after threshold (100 req/min general, 10 req/min translation, 5 req/min upload)
- **Secret Handling:** OpenAI API key never exposed in errors or logs

**Tools:**
- Playwright for E2E security tests (session isolation, input validation)
- OWASP ZAP for automated security scanning (optional, post-MVP)
- npm audit for dependency vulnerability scanning (CI)

**Test Examples:**
```typescript
// tests/e2e/security/session-isolation.spec.ts
test('users cannot access other sessions documents', async ({ page, request }) => {
  // Create document with session A
  const sessionA = 'session-a-uuid';
  const docA = await request.post('/api/v1/documents/upload', {
    headers: { 'X-Session-Id': sessionA },
    files: { file: 'test.txt' },
  });

  // Attempt access with session B
  const sessionB = 'session-b-uuid';
  const response = await request.get(`/api/v1/documents/${docA.id}`, {
    headers: { 'X-Session-Id': sessionB },
  });

  expect(response.status()).toBe(403); // Forbidden
});
```

**NFR Criteria:**
- ✅ PASS: All security tests green (session isolation, input validation, rate limiting)
- ⚠️ CONCERNS: Minor gaps with clear mitigation plans
- ❌ FAIL: Critical exposure (cross-session access, SQL injection succeeds)

---

### Performance NFR Testing

**Approach:** k6 load testing (NOT Playwright)

**Test Coverage:**
- **Load Testing:** System behavior under expected load (50 concurrent users)
- **Stress Testing:** Breaking point identification (100+ concurrent users)
- **Spike Testing:** Sudden load increases (traffic spikes)
- **SLO/SLA Validation:** Translation completes in <5 minutes for 50-page documents (NFR1)

**Tools:**
- k6 for load/stress/spike testing
- Lighthouse for Core Web Vitals (frontend performance)

**Test Examples:**
```javascript
// tests/nfr/performance/translation-load.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 }, // Ramp up to 50 users
    { duration: '3m', target: 50 }, // Stay at 50 users
    { duration: '1m', target: 100 }, // Spike to 100 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests <500ms
    errors: ['rate<0.01'], // Error rate <1%
  },
};

export default function () {
  // Upload document
  const uploadResponse = http.post(`${__ENV.BASE_URL}/api/v1/documents/upload`, {
    files: { file: 'test-document.txt' },
    headers: { 'X-Session-Id': `session-${__VU}` },
  });

  check(uploadResponse, {
    'upload status is 201': (r) => r.status === 201,
    'upload completes in <2s': (r) => r.timings.duration < 2000,
  });

  const docId = JSON.parse(uploadResponse.body).id;

  // Start translation
  const translationResponse = http.post(`${__ENV.BASE_URL}/api/v1/translations/create`, {
    json: { document_id: docId, target_language: 'es' },
    headers: { 'X-Session-Id': `session-${__VU}` },
  });

  check(translationResponse, {
    'translation status is 201': (r) => r.status === 201,
    'translation starts in <1s': (r) => r.timings.duration < 1000,
  });

  sleep(1);
}
```

**NFR Criteria:**
- ✅ PASS: SLO/SLA targets met with k6 evidence (p95 <500ms, error rate <1%, translation <5min)
- ⚠️ CONCERNS: Trending toward limits or missing baselines
- ❌ FAIL: SLO/SLA breached (p95 >500ms, error rate >1%)

---

### Reliability NFR Testing

**Approach:** Playwright E2E tests + API tests

**Test Coverage:**
- **Error Handling:** Graceful degradation (500 errors → user-friendly messages)
- **Retries:** API client retries on transient failures (3 attempts)
- **Health Checks:** `/health` endpoint returns service status
- **Progress Saving:** Auto-save with debouncing (2 seconds), resume functionality

**Tools:**
- Playwright for E2E error handling tests
- Pytest + httpx for API error handling tests

**Test Examples:**
```typescript
// tests/e2e/reliability/error-handling.spec.ts
test('app remains functional when API returns 500 error', async ({ page, context }) => {
  // Mock API failure
  await context.route('**/api/v1/documents/upload', (route) => {
    route.fulfill({ status: 500, body: JSON.stringify({ error: 'Internal Server Error' }) });
  });

  await page.goto('/');
  await page.getByRole('button', { name: 'Upload' }).click();

  // User sees error message (not blank page)
  await expect(page.getByText('Unable to upload document. Please try again.')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();

  // App navigation still works (graceful degradation)
  await page.getByRole('link', { name: 'Home' }).click();
  await expect(page).toHaveURL('/');
});
```

**NFR Criteria:**
- ✅ PASS: Error handling, retries, health checks verified (all tests green)
- ⚠️ CONCERNS: Partial coverage or missing telemetry
- ❌ FAIL: No recovery path (500 error crashes app)

---

### Maintainability NFR Testing

**Approach:** CI tools (GitHub Actions) + Playwright for observability validation

**Test Coverage:**
- **Test Coverage:** ≥80% code coverage (from CI coverage report)
- **Code Duplication:** <5% duplication (from jscpd CI job)
- **Vulnerability Scanning:** No critical/high vulnerabilities (from npm audit CI job)
- **Observability:** Structured logging with trace IDs (Playwright validates telemetry headers)

**Tools:**
- GitHub Actions for coverage, duplication, audit checks
- Playwright for observability validation (trace IDs, Server-Timing headers)

**NFR Criteria:**
- ✅ PASS: Clean code (80%+ coverage, <5% duplication), observability validated, no critical vulnerabilities
- ⚠️ CONCERNS: Duplication >5%, coverage 60-79%, unclear ownership
- ❌ FAIL: Absent tests (<60%), tangled code (>10% duplication), no observability

---

## Test Environment Requirements

### Local Development Environment

**Infrastructure:**
- Docker Compose for local services (backend, frontend, PostgreSQL)
- Test database (separate from dev database)
- Mock OpenAI API (use `responses` library or mock OpenAI client)

**Configuration:**
- Environment variables for test configuration (`.env.test`)
- Test data factories (faker-based, auto-cleanup)
- Test fixtures with auto-rollback (pytest fixtures)

---

### CI/CD Environment

**Infrastructure:**
- GitHub Actions for automated testing
- Test database (ephemeral, created per test run)
- k6 cloud or self-hosted runner for performance tests

**Configuration:**
- Parallel test execution (Playwright workers, pytest-xdist)
- Test artifact storage (screenshots, traces, coverage reports)
- Test result reporting (JUnit XML, HTML reports)

---

### Staging Environment

**Infrastructure:**
- Railway staging environment (mirrors production)
- Test OpenAI API key (separate from production)
- Test database (can be shared or isolated)

**Configuration:**
- E2E tests run against staging (smoke tests before production deploy)
- Performance tests run against staging (validate SLO/SLA before production)

---

## Testability Concerns

### Concern 1: OpenAI API Mocking Strategy (MINOR)

**Issue:** Async translation processing depends on OpenAI API. Testing requires deterministic mocking strategy.

**Impact:** Medium - affects integration and E2E test reliability

**Mitigation:**
- Use `responses` library (Python) or mock OpenAI client for deterministic responses
- Create test fixtures with pre-defined OpenAI responses (translated chunks)
- Document mocking strategy in test framework setup guide

**Owner:** QA Lead  
**Timeline:** Sprint 0 (test framework setup)

---

### Concern 2: Async Translation Progress Testing (MINOR)

**Issue:** Translation progress tracking requires polling mechanism. Testing async progress updates may be flaky.

**Impact:** Medium - affects E2E test reliability

**Mitigation:**
- Use deterministic waits (wait for specific progress percentage, not time-based)
- Mock translation service for E2E tests (skip actual OpenAI calls)
- Implement progress update events (WebSocket or Server-Sent Events) for more reliable testing (post-MVP)

**Owner:** QA Lead  
**Timeline:** Epic 2 (Translation Processing)

---

## Recommendations for Sprint 0

### Test Framework Setup (`*framework` workflow)

**Actions:**
1. **Install Testing Tools:**
   - Playwright for E2E tests (frontend)
   - Pytest + httpx for API tests (backend)
   - Vitest + React Testing Library for component tests (frontend)
   - k6 for performance tests

2. **Configure Test Infrastructure:**
   - Set up test database fixtures (pytest fixtures with auto-rollback)
   - Create test data factories (faker-based, auto-cleanup)
   - Configure Playwright test environment (browser setup, base URL)

3. **Create Test Utilities:**
   - API client helpers (test request wrappers)
   - Database helpers (seed, cleanup)
   - Mock OpenAI API helpers (deterministic responses)

4. **Document Test Patterns:**
   - Test organization structure (unit, integration, e2e)
   - Test naming conventions
   - Test data management (factories, fixtures)

---

### CI/CD Quality Pipeline (`*ci` workflow)

**Actions:**
1. **Set Up GitHub Actions:**
   - Run tests on pull requests (backend + frontend)
   - Run E2E tests on merge to main
   - Run performance tests nightly (k6)

2. **Configure Quality Gates:**
   - Test coverage threshold (≥80%)
   - Code duplication threshold (<5%)
   - Vulnerability scanning (npm audit, no critical/high)

3. **Set Up Test Reporting:**
   - Coverage reports (HTML, upload to coverage service)
   - Test result reports (JUnit XML)
   - Performance test results (k6 JSON output)

---

### Test Data Management

**Actions:**
1. **Create Test Factories:**
   - Document factory (faker-based, various sizes: 1 page, 10 pages, 50 pages)
   - Translation factory (with progress states: pending, in_progress, completed)
   - Session factory (unique session_ids)

2. **Implement Auto-Cleanup:**
   - Pytest fixtures with `yield` for teardown
   - Playwright fixtures with auto-cleanup
   - Database rollback after each test

---

## Summary

**Testability Status:** PASS with minor concerns

**Key Strengths:**
- Strong controllability (repository pattern, dependency injection, test database)
- Good reliability (session isolation, stateless design, parallel-safe)
- Clear test levels strategy (40/30/30 split)

**Areas for Improvement:**
- Observability gaps (performance metrics, structured logging)
- OpenAI API mocking strategy needs documentation
- Async translation progress testing needs deterministic approach

**Next Steps:**
1. Execute `*framework` workflow to set up test infrastructure
2. Execute `*ci` workflow to configure CI/CD quality pipeline
3. Begin Epic 1 implementation with test-first approach (`*atdd` workflow)

---

**Generated by:** BMad TEA Agent - Test Architect Module  
**Workflow:** `_bmad/bmm/testarch/test-design`  
**Version:** 4.0 (BMad v6)

