# API Contract: Textbook Service

**Feature**: 001-ai-humanoid-textbook
**Version**: 1.0
**Date**: 2025-12-17

## Base URL
`/api/v1`

## Authentication
No authentication required for textbook content access. Optional authentication for personalized features.

## Endpoints

### GET /textbook/chapters
Retrieve list of all textbook chapters

**Request**:
- Method: GET
- Path: `/api/v1/textbook/chapters`
- Headers: None required

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "chapters": [
    {
      "id": "string",
      "title": "string",
      "slug": "string",
      "order": "integer",
      "word_count": "integer",
      "estimated_reading_time": "integer"
    }
  ]
}
```

### GET /textbook/chapters/{slug}
Retrieve content of a specific chapter

**Request**:
- Method: GET
- Path: `/api/v1/textbook/chapters/{slug}`
- Headers: None required

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "id": "string",
  "title": "string",
  "slug": "string",
  "content": "string",
  "order": "integer",
  "sections": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "order": "integer",
      "heading_level": "integer"
    }
  ]
}
```

### POST /chat/session
Create a new AI chat session

**Request**:
- Method: POST
- Path: `/api/v1/chat/session`
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "user_id": "string (optional)"
}
```

**Response**:
- Status: 201 Created
- Content-Type: application/json
- Body:
```json
{
  "session_id": "string",
  "created_at": "datetime"
}
```

### POST /chat/{session_id}/message
Send a message to the AI chatbot and receive a response

**Request**:
- Method: POST
- Path: `/api/v1/chat/{session_id}/message`
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "message": "string",
  "context": "string (optional selected text)"
}
```

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "response": "string",
  "context_used": "string",
  "timestamp": "datetime"
}
```

### GET /search
Search textbook content using RAG

**Request**:
- Method: GET
- Path: `/api/v1/search`
- Query Parameters:
  - q: search query string
  - limit: number of results (default: 5, max: 10)

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "content_snippet": "string",
      "relevance_score": "float",
      "url": "string"
    }
  ]
}
```

### GET /preferences
Retrieve user preferences

**Request**:
- Method: GET
- Path: `/api/v1/preferences`
- Headers: None required (uses session-based identification)

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "language": "string",
  "theme": "string",
  "text_size": "string",
  "personalization_enabled": "boolean"
}
```

### PUT /preferences
Update user preferences

**Request**:
- Method: PUT
- Path: `/api/v1/preferences`
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "language": "string",
  "theme": "string",
  "text_size": "string",
  "personalization_enabled": "boolean"
}
```

**Response**:
- Status: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "success": "boolean",
  "updated_at": "datetime"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "string",
  "code": "string",
  "details": "object (optional)"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "code": "RESOURCE_NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "code": "INTERNAL_ERROR"
}
```

## Rate Limiting
- Anonymous users: 100 requests per hour per IP
- Authenticated users: 500 requests per hour per user
- AI chat endpoints: 20 messages per hour per session

## Content Validation
- All text inputs are sanitized using HTML escaping
- Content length limits enforced per endpoint
- Special characters handled according to UTF-8 standards