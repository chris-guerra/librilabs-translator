/**
 * Session management fixture.
 *
 * Provides session ID management for tests.
 */
import { test as base } from '@playwright/test';
import { v4 as uuidv4 } from 'uuid';

type SessionFixture = {
  sessionId: string;
  setSessionId: (sessionId: string) => Promise<void>;
};

export const test = base.extend<SessionFixture>({
  sessionId: async ({ page, context }, use) => {
    // Generate unique session ID for each test
    const sessionId = uuidv4();

    // Set session ID in sessionStorage before test
    await page.addInitScript((id) => {
      sessionStorage.setItem('session_id', id);
    }, sessionId);

    // Also set as cookie for API requests
    await context.addCookies([
      {
        name: 'session_id',
        value: sessionId,
        domain: 'localhost',
        path: '/',
      },
    ]);

    await use(sessionId);
  },

  setSessionId: async ({ page, context }, use) => {
    const setSession = async (sessionId: string) => {
      await page.addInitScript((id) => {
        sessionStorage.setItem('session_id', id);
      }, sessionId);

      await context.addCookies([
        {
          name: 'session_id',
          value: sessionId,
          domain: 'localhost',
          path: '/',
        },
      ]);
    };

    await use(setSession);
  },
});
