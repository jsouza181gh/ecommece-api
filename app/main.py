import config
import asyncio
from infrastructure.database.base import createDataBase

if __name__ == '__main__':
    asyncio.run(createDataBase())