import pytest
from sqlalchemy import create_engine, inspect

from backend.app.core.config import settings


@pytest.mark.skipif(
    not __import__("os").getenv("RUN_DB_TESTS"),
    reason="Set RUN_DB_TESTS=1 to run PostgreSQL integration tests",
)
def test_expected_tables():
    engine = create_engine(settings.sync_database_url)

    expected = {
        "organizations",
        "users",
        "roles",
        "employees",
        "locations",
        "parking_areas",
        "floors",
        "zones",
        "parking_slots",
        "vehicles",
        "bookings",
        "payments",
        "parking_sessions",
        "audit_records",
        "knowledge_documents",
        "knowledge_document_chunks",
        "employee_location_assignments",
        "idempotency_records",
        "booking_status_history",
        "payment_attempts",
    }

    try:
        actual = set(inspect(engine).get_table_names())
        assert expected.issubset(actual)
    finally:
        engine.dispose()
