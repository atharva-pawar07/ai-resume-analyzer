
import asyncio
from sqlalchemy import text
from backend.app.core.database import engine


async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("SELECT current_database(), current_user")
            )

            print("Database connection successful!")
            print(result.fetchone())

    except Exception as error:
        print("Database connection failed!")
        print(error)

    finally:
        await engine.dispose()


asyncio.run(test_connection())
