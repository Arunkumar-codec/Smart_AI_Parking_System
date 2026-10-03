# Phase 4 Verification

Run from the project root after merging these files with the Phase 3 repository.

## Start

    uvicorn backend.app.main:app --reload

## API

    GET /api/v1/health
    GET /api/v1/health/db
    GET /docs
    GET /api/v1/openapi.json

## Tests

    pytest tests/api/ -v
    pytest tests/db/ -v

## Migration

    alembic upgrade head

Expected Phase 3 regression baseline from the supplied implementation report:

    pytest tests/db/ -v
    14 passed

The actual result must be verified in the real merged repository; this archive does not claim to have executed against the missing Phase 3 repository.
