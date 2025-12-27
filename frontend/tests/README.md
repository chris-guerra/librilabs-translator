# Frontend Test Framework

This directory contains the test framework for the Librilabs Translator frontend (Next.js).

## Directory Structure

```
frontend/tests/
├── e2e/                    # End-to-end tests (Playwright)
│   └── example.spec.ts
├── unit/                   # Unit tests (Vitest)
│   └── components/
│       └── Example.test.tsx
├── support/                # Test infrastructure
│   ├── fixtures/          # Playwright fixtures
│   │   ├── index.ts      # Merged fixtures
│   │   ├── api-fixture.ts
│   │   └── session-fixture.ts
│   └── factories/         # Data factories (faker-based)
│       ├── document-factory.ts
│       └── translation-factory.ts
└── setup.ts               # Vitest setup file
```

## Setup

### Prerequisites

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Install Playwright browsers:
```bash
npx playwright install
```

3. Set up environment variables (optional):
```bash
# Create .env.test (optional)
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
```

### Running Tests

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npx playwright test --ui

# Run E2E tests in headed mode
npx playwright test --headed

# Run specific test file
npx playwright test tests/e2e/example.spec.ts

# Run tests with debug
npx playwright test --debug
```

## Test Architecture

### Fixtures

The test framework uses Playwright's `mergeTests` pattern for composable fixtures:

```typescript
import { test, expect } from './support/fixtures';

test('example test', async ({ page, apiRequest, sessionId }) => {
  // Use fixtures
  const document = await apiRequest.createDocument('Test content');
  // ...
});
```

Available fixtures:
- **`apiRequest`**: Helper functions for API requests
- **`sessionId`**: Unique session ID for each test
- **`setSessionId`**: Function to set custom session ID

### Data Factories

Factories use `@faker-js/faker` to generate unique test data:

```typescript
import { createDocument, createTranslation } from './support/factories';

// Create document with defaults
const document = createDocument();

// Create document with overrides
const document = createDocument({
  content: 'Custom content',
  source_language: 'fr',
  content_size: 'large', // small, medium, large
});

// Create translation
const translation = createTranslation(documentId, {
  status: 'completed',
  target_language: 'es',
});
```

### API Fixture

The `apiRequest` fixture provides helper functions:

```typescript
test('example', async ({ apiRequest }) => {
  // Create document
  const doc = await apiRequest.createDocument('Content', 'test.txt', 'en');
  
  // Get document
  const fetched = await apiRequest.getDocument(doc.id);
  
  // Create translation
  const translation = await apiRequest.createTranslation(doc.id, 'es');
  
  // Get translation status
  const status = await apiRequest.getTranslationStatus(translation.id);
  
  // Update translation
  await apiRequest.updateTranslation(translation.id, 'Updated content');
});
```

## Best Practices

1. **Use Factories**: Always use factories for test data (not hardcoded values)
2. **Parallel Safety**: All factories use faker for unique data (no collisions)
3. **API-First Setup**: Use `apiRequest` fixture for data setup (faster than UI)
4. **Explicit Assertions**: Keep assertions visible in test bodies
5. **Network-First**: Intercept network requests before navigation for deterministic waits

## Test Organization

- **Unit Tests**: Test React components in isolation (Vitest + React Testing Library)
- **E2E Tests**: Test complete user journeys (Playwright)

## Configuration

### Playwright Config

Configuration is in `playwright.config.ts`:

- **Timeouts**: Test 60s, assertion 15s, action 15s, navigation 30s
- **Artifacts**: Screenshots on failure, videos on failure, traces on failure
- **Reporters**: HTML, JUnit XML, list
- **Web Server**: Auto-starts Next.js dev server

### Vitest Config

Configuration is in `vitest.config.ts`:

- **Environment**: jsdom (for React component testing)
- **Setup**: `tests/setup.ts` (for test utilities)

## CI Integration

Tests run automatically in CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: npm ci

- name: Install Playwright browsers
  run: npx playwright install --with-deps

- name: Run tests
  run: |
    npm test
    npm run test:e2e
```

## Knowledge Base References

- `fixture-architecture.md` - Pure function → fixture → mergeTests pattern
- `data-factories.md` - Factory patterns with faker
- `network-first.md` - Network-first testing safeguards
- `test-quality.md` - Test design principles

