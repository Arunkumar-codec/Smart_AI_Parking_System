from sqlalchemy.types import TypeDecorator, CHAR
from uuid import UUID

class GUID(TypeDecorator):
    """Portable UUID/GUID type; PostgreSQL uses native UUID."""
    impl = CHAR
    cache_ok = True
    def load_dialect_impl(self, dialect):
        from sqlalchemy.dialects.postgresql import UUID as PGUUID
        return dialect.type_descriptor(PGUUID(as_uuid=True)) if dialect.name == "postgresql" else dialect.type_descriptor(CHAR(36))
    def process_bind_param(self, value, dialect):
        if value is None: return None
        return value if isinstance(value, UUID) else UUID(str(value))
    def process_result_value(self, value, dialect):
        return value
