import pytest
from sqlalchemy import create_engine, text

from backend.app.core.config import settings


@pytest.mark.skipif(
    not __import__("os").getenv("RUN_DB_TESTS"),
    reason="Set RUN_DB_TESTS=1 to run PostgreSQL integration tests",
)
def test_required_extensions():
    engine = create_engine(settings.sync_database_url)

    with engine.connect() as connection:
        extensions = {
            row[0]
            for row in connection.execute(
                text("SELECT extname FROM pg_extension")
            )
        }

    assert {"vector", "btree_gist"} <= extensions
    engine.dispose()
