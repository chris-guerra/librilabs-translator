/**
 * Document factory for creating test documents.
 *
 * Uses faker to generate unique test data and supports overrides for explicit test intent.
 */
import { faker } from '@faker-js/faker';

export type Document = {
  id?: string;
  content: string;
  file_name: string;
  file_size: number;
  source_language: string;
  session_id?: string;
  created_at?: string;
  updated_at?: string;
};

export type DocumentOverrides = Partial<Omit<Document, 'id' | 'created_at' | 'updated_at'>> & {
  content_size?: 'small' | 'medium' | 'large';
};

/**
 * Create a document object with sensible defaults.
 *
 * @param overrides - Partial document data to override defaults
 * @returns Document object
 */
export function createDocument(overrides: DocumentOverrides = {}): Document {
  // Generate default content based on size
  const contentSize = overrides.content_size || 'small';
  let content: string;

  if (contentSize === 'small') {
    content = faker.lorem.paragraphs(3); // ~1 page
  } else if (contentSize === 'medium') {
    content = faker.lorem.paragraphs(30); // ~10 pages
  } else {
    content = faker.lorem.paragraphs(150); // ~50 pages
  }

  // Use provided content or generated default
  content = overrides.content || content;

  // Calculate file size from content
  const fileSize = new Blob([content]).size;

  return {
    content,
    file_name: overrides.file_name || faker.system.fileName({ extensionCount: 0 }) + '.txt',
    file_size: overrides.file_size || fileSize,
    source_language: overrides.source_language || 'en',
    session_id: overrides.session_id || faker.string.uuid(),
  };
}

