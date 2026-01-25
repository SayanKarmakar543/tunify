import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.initial_data import create_initial_admin

if __name__ == "__main__":
    asyncio.run(create_initial_admin())
