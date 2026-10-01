"""initial SPMS Phase 3 database schema"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSTZRANGE

revision='001_initial_schema'
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "btree_gist"')
    # Use SQLAlchemy metadata to create the reconstructed schema.
    from backend.app.db.base import Base
    from backend.app.db.models import models  # noqa
    bind=op.get_bind()
    Base.metadata.create_all(bind=bind)
    # PostgreSQL-native concurrency protection for active booking windows.
    op.execute("""
        ALTER TABLE bookings ADD CONSTRAINT booking_no_overlap
        EXCLUDE USING GIST (
            parking_slot_id WITH =,
            tstzrange(start_at, end_at, '[)') WITH &&
        ) WHERE (status IN ('DRAFT','PENDING','CONFIRMED','ACTIVE'))
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_knowledge_chunks_embedding_hnsw ON knowledge_document_chunks USING hnsw (embedding vector_cosine_ops)")

def downgrade():
    op.execute('DROP INDEX IF EXISTS ix_knowledge_chunks_embedding_hnsw')
    op.execute('ALTER TABLE bookings DROP CONSTRAINT IF EXISTS booking_no_overlap')
    from backend.app.db.base import Base
    from backend.app.db.models import models  # noqa
    Base.metadata.drop_all(bind=op.get_bind())
