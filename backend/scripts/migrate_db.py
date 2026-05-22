import asyncio

from sqlalchemy import text

from src.api.dependencies.session import get_session


async def migrate_db() -> None:
    async for session in get_session():
        await session.execute(
            text("""
                ALTER TABLE projects_reports
                DROP CONSTRAINT projects_reports_pkey;
            """)
        )
        await session.execute(
            text("""
                ALTER TABLE projects_reports
                DROP COLUMN id;
            """)
        )
        await session.execute(
            text("""
                ALTER TABLE projects_reports
                ADD PRIMARY KEY (project_id, date_str);
            """)
        )
        await session.commit()

    print("Migration has been completed.")


if __name__ == "__main__":
    asyncio.run(migrate_db())
