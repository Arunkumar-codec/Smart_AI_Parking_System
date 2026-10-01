import os
import pytest

@pytest.fixture
def database_url():
    return os.getenv('SYNC_DATABASE_URL','postgresql://spms:spms@localhost:5432/spms')
