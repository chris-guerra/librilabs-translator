/**
 * Example E2E test demonstrating test framework usage.
 *
 * This test shows how to use fixtures, factories, and API helpers.
 */
import { test, expect } from '../support/fixtures';
import { createDocument } from '../support/factories';

test.describe('Document Upload', () => {
  test('should upload document via API and display in UI', async ({ page, apiRequest, sessionId }) => {
    // Create test document using factory
    const testDoc = createDocument({
      content: 'This is a test document for translation.',
      file_name: 'test-document.txt',
      source_language: 'en',
    });

    // Upload document via API (fast setup)
    const uploadedDoc = await apiRequest.createDocument(
      testDoc.content,
      testDoc.file_name,
      testDoc.source_language,
    );

    // Verify document was created
    expect(uploadedDoc.id).toBeTruthy();
    expect(uploadedDoc.file_name).toBe(testDoc.file_name);

    // Navigate to UI and verify document is displayed
    await page.goto('/');
    // Add assertions based on your UI implementation
    // await expect(page.getByText(testDoc.file_name)).toBeVisible();
  });

  test('should validate file format and size', async ({ apiRequest }) => {
    // Test invalid file format
    await expect(
      apiRequest.createDocument('Content', 'test.pdf', 'en'),
    ).rejects.toThrow();

    // Test file size limit (10MB)
    const largeContent = 'x'.repeat(11 * 1024 * 1024); // 11MB
    await expect(
      apiRequest.createDocument(largeContent, 'large.txt', 'en'),
    ).rejects.toThrow();
  });
});

