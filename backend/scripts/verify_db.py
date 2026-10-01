import asyncio
from sqlalchemy import text, inspect
from backend.app.db.session import engine

EXPECTED_TABLES = 20

async def main():
    async with engine.connect() as conn:
        version=(await conn.execute(text('select version()'))).scalar_one()
        exts=list((await conn.execute(text("select extname from pg_extension where extname in ('vector','btree_gist')"))).scalars())
        tables=list((await conn.execute(text("select tablename from pg_tables where schemaname='public'"))).scalars())
        indexes=int((await conn.execute(text("select count(*) from pg_indexes where schemaname='public'"))).scalar_one())
        print('PostgreSQL:', version)
        print('Extensions:', exts)
        print('Tables:', len(tables), sorted(tables))
        print('Indexes:', indexes)
        print('Expected table count:', EXPECTED_TABLES)
        if 'vector' not in exts or 'btree_gist' not in exts: raise SystemExit('FAILED: required extensions missing')
        if len(tables) < EXPECTED_TABLES: raise SystemExit('FAILED: expected tables missing')
        print('PASSED')

if __name__=='__main__': asyncio.run(main())
