import pytest
from sqlalchemy import text
from backend.app.core.database import engine


@pytest.mark.asyncio
async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("SELECT current_database(), current_user")
            )

            row = result.fetchone()

            assert row is not None

            print("Database connection successful!")
            print(row)

    finally:
        await engine.dispose()