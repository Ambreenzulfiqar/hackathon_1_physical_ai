# Data Model: Physical AI & Humanoid Robotics — Essentials

**Feature**: 001-ai-humanoid-textbook
**Date**: 2025-12-17
**Status**: Draft

## Textbook Chapter

**Description**: Represents one of the 6 planned chapters of the Physical AI & Humanoid Robotics textbook

**Fields**:
- `id` (string): Unique identifier for the chapter
- `title` (string): Title of the chapter (e.g., "Introduction to Physical AI")
- `slug` (string): URL-friendly identifier for the chapter
- `content` (string): The full text content of the chapter
- `order` (integer): Chapter number in the sequence (1-6)
- `word_count` (integer): Number of words in the chapter content
- `estimated_reading_time` (integer): Estimated reading time in minutes
- `created_at` (datetime): Timestamp of chapter creation
- `updated_at` (datetime): Timestamp of last update

**Relationships**:
- Contains multiple `textbook_sections` (one-to-many)

**Validation Rules**:
- Title must be 5-200 characters
- Content must not be empty
- Order must be between 1-6
- Slug must be unique

## Textbook Section

**Description**: A section within a textbook chapter

**Fields**:
- `id` (string): Unique identifier for the section
- `chapter_id` (string): Reference to the parent chapter
- `title` (string): Title of the section
- `content` (string): Content of the section
- `order` (integer): Section number within the chapter
- `heading_level` (integer): HTML heading level (1-6)

**Relationships**:
- Belongs to one `textbook_chapter` (many-to-one)
- Contains multiple `textbook_paragraphs` (one-to-many)

## AI Chat Session

**Description**: Represents a user's interaction session with the AI chatbot

**Fields**:
- `id` (string): Unique identifier for the chat session
- `user_id` (string): Identifier for the user (optional for anonymous sessions)
- `created_at` (datetime): Timestamp of session creation
- `updated_at` (datetime): Timestamp of last interaction
- `is_active` (boolean): Whether the session is currently active

**Relationships**:
- Contains multiple `ai_chat_messages` (one-to-many)

## AI Chat Message

**Description**: A single message in an AI chat session

**Fields**:
- `id` (string): Unique identifier for the message
- `session_id` (string): Reference to the parent chat session
- `role` (string): "user" or "assistant"
- `content` (string): The text content of the message
- `timestamp` (datetime): When the message was created
- `context_used` (string): The textbook content that was used as context for the response

**Relationships**:
- Belongs to one `ai_chat_session` (many-to-one)

## User Preference

**Description**: Configuration settings for optional features

**Fields**:
- `id` (string): Unique identifier for the preference set
- `user_id` (string): Identifier for the user
- `language` (string): Preferred language (default: "en", optional: "ur" for Urdu)
- `theme` (string): UI theme preference ("light" or "dark")
- `text_size` (string): Preferred text size ("small", "normal", "large")
- `personalization_enabled` (boolean): Whether personalization features are enabled
- `created_at` (datetime): Timestamp of preference creation
- `updated_at` (datetime): Timestamp of last update

**Validation Rules**:
- Language must be one of the supported languages
- Theme must be "light" or "dark"
- Text size must be "small", "normal", or "large"

## Text Embedding

**Description**: Vector representation of text content for RAG functionality

**Fields**:
- `id` (string): Unique identifier for the embedding
- `content_id` (string): Reference to the original content (could be chapter, section, or paragraph)
- `content_type` (string): Type of content ("chapter", "section", "paragraph")
- `text_content` (string): The original text that was embedded
- `embedding_vector` (array of floats): The vector representation
- `embedding_model` (string): The model used to generate the embedding
- `created_at` (datetime): Timestamp of embedding creation

**Relationships**:
- References original content (many-to-one with different content types)

## State Transitions

### AI Chat Session
- **Active** → **Inactive**: When user stops interacting for 30+ minutes
- **Inactive** → **Active**: When user sends a new message

## Constraints

- All timestamps use ISO 8601 format
- Text content is limited to 10,000 characters per field to ensure efficient processing
- Embedding vectors are normalized to unit length
- User preferences are stored with appropriate privacy considerations