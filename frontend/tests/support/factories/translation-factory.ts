/**
 * Translation factory for creating test translations.
 *
 * Uses faker to generate unique test data and supports overrides for explicit test intent.
 */
import { faker } from '@faker-js/faker';

export type Translation = {
  id?: string;
  document_id: string;
  target_language: string;
  translated_content?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress_percentage: number;
  translation_state?: Record<string, any>;
  session_id?: string;
  created_at?: string;
  updated_at?: string;
};

export type TranslationOverrides = Partial<Omit<Translation, 'id' | 'created_at' | 'updated_at'>>;

/**
 * Create a translation object with sensible defaults.
 *
 * @param documentId - ID of the document being translated (required)
 * @param overrides - Partial translation data to override defaults
 * @returns Translation object
 */
export function createTranslation(
  documentId: string,
  overrides: TranslationOverrides = {},
): Translation {
  const status = overrides.status || 'pending';

  // Generate translated content based on status
  let translatedContent: string | undefined;
  let progressPercentage: number;

  if (status === 'completed') {
    translatedContent = overrides.translated_content || faker.lorem.paragraphs(10);
    progressPercentage = 100;
  } else if (status === 'in_progress') {
    translatedContent = overrides.translated_content || faker.lorem.paragraphs(5);
    progressPercentage = overrides.progress_percentage || 50;
  } else {
    translatedContent = overrides.translated_content;
    progressPercentage = overrides.progress_percentage || 0;
  }

  return {
    document_id: documentId,
    target_language: overrides.target_language || 'es',
    translated_content: translatedContent,
    status,
    progress_percentage: progressPercentage,
    translation_state: overrides.translation_state,
    session_id: overrides.session_id || faker.string.uuid(),
  };
}

