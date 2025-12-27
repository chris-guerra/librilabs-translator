/**
 * API request fixture.
 *
 * Provides helper functions for making API requests in tests.
 */
import { test as base } from '@playwright/test';

type ApiFixture = {
  apiRequest: {
    createDocument: (fileContent: string, fileName?: string, sourceLanguage?: string) => Promise<any>;
    getDocument: (documentId: string) => Promise<any>;
    createTranslation: (documentId: string, targetLanguage?: string) => Promise<any>;
    getTranslationStatus: (translationId: string) => Promise<any>;
    updateTranslation: (translationId: string, translatedContent: string) => Promise<any>;
  };
};

export const test = base.extend<ApiFixture>({
  apiRequest: async ({ request }, use) => {
    const baseURL = process.env.API_BASE_URL || 'http://localhost:8000';
    let sessionId: string | null = null;

    const getSessionId = () => {
      // Generate new session ID if not set
      if (!sessionId) {
        sessionId = crypto.randomUUID();
      }
      return sessionId;
    };

    const apiHelpers = {
      async createDocument(
        fileContent: string,
        fileName: string = 'test.txt',
        sourceLanguage: string = 'en',
      ) {
        const session = getSessionId();

        const response = await request.post(`${baseURL}/api/v1/documents/upload`, {
          headers: {
            'X-Session-Id': session,
          },
          multipart: {
            file: {
              name: fileName,
              mimeType: 'text/plain',
              buffer: Buffer.from(fileContent, 'utf-8'),
            },
            source_language: sourceLanguage,
          },
        });

        if (!response.ok()) {
          throw new Error(`Failed to create document: ${response.status()} ${await response.text()}`);
        }

        return response.json();
      },

      async getDocument(documentId: string) {
        const session = getSessionId();
        const response = await request.get(`${baseURL}/api/v1/documents/${documentId}`, {
          headers: {
            'X-Session-Id': session,
          },
        });

        if (!response.ok()) {
          throw new Error(`Failed to get document: ${response.status()} ${await response.text()}`);
        }

        return response.json();
      },

      async createTranslation(documentId: string, targetLanguage: string = 'es') {
        const session = getSessionId();
        const response = await request.post(`${baseURL}/api/v1/translations/create`, {
          headers: {
            'Content-Type': 'application/json',
            'X-Session-Id': session,
          },
          data: {
            document_id: documentId,
            target_language: targetLanguage,
          },
        });

        if (!response.ok()) {
          throw new Error(`Failed to create translation: ${response.status()} ${await response.text()}`);
        }

        return response.json();
      },

      async getTranslationStatus(translationId: string) {
        const session = getSessionId();
        const response = await request.get(`${baseURL}/api/v1/translations/${translationId}/status`, {
          headers: {
            'X-Session-Id': session,
          },
        });

        if (!response.ok()) {
          throw new Error(`Failed to get translation status: ${response.status()} ${await response.text()}`);
        }

        return response.json();
      },

      async updateTranslation(translationId: string, translatedContent: string) {
        const session = getSessionId();
        const response = await request.put(`${baseURL}/api/v1/translations/${translationId}`, {
          headers: {
            'Content-Type': 'application/json',
            'X-Session-Id': session,
          },
          data: {
            translated_content: translatedContent,
          },
        });

        if (!response.ok()) {
          throw new Error(`Failed to update translation: ${response.status()} ${await response.text()}`);
        }

        return response.json();
      },
    };

    await use(apiHelpers);
  },
});
