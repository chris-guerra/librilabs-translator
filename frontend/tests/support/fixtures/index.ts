/**
 * Merged test fixtures.
 *
 * This file composes all test fixtures using Playwright's mergeTests pattern.
 * Import this file in your tests to access all fixtures.
 */
import { test as base, mergeTests } from '@playwright/test';
import { test as apiFixture } from './api-fixture';
import { test as sessionFixture } from './session-fixture';

// Compose all fixtures
export const test = mergeTests(base, apiFixture, sessionFixture);

export { expect } from '@playwright/test';

