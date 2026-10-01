import pytest
from sqlalchemy import create_engine, text

@pytest.mark.skipif(not __import__('os').getenv('RUN_DB_TESTS'), reason='Set RUN_DB_TESTS=1 to run PostgreSQL integration tests')
def test_required_extensions():
    engine=create_engine(__import__('os').environ['SYNC_DATABASE_URL'])
    with engine.connect() as c:
        ext={r[0] for r in c.execute(text("select extname from pg_extension"))}
    assert {'vector','btree_gist'} <= ext
