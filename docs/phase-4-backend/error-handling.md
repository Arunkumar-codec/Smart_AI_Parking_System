# Error Handling

SPMS uses centralized application exception handling.

Domain/application errors include:

- NotFoundError
- ValidationError
- ConflictError
- AuthorizationError
- BusinessRuleError
- DatabaseError
- ExternalServiceError

Unexpected database and application exceptions are logged internally while clients receive sanitized responses.

Do not expose:
- passwords
- tokens
- API keys
- SQL credentials
- stack traces
- internal SQL/database details
