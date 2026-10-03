# API Conventions

## Versioning

Current API prefix:

    /api/v1

## Health

    GET /api/v1/health
    GET /api/v1/health/db

## Errors

Standard envelope:

    {
      "error": {
        "code": "...",
        "message": "...",
        "details": {}
      }
    }

## Correlation

Requests receive or generate:

    X-Correlation-ID

The value is returned in the response header and is intended for tracing.
