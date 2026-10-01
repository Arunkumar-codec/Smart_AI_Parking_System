from sqlalchemy.types import TypeDecorator, DateTime

class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True
    def load_dialect_impl(self, dialect):
        from sqlalchemy.dialects.postgresql import TIMESTAMP
        return dialect.type_descriptor(TIMESTAMP(timezone=True)) if dialect.name == "postgresql" else dialect.type_descriptor(DateTime(timezone=True))
