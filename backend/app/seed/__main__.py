"""
CLI entry point for seed data.

Usage:
    python -m app.seed
"""

import asyncio
import logging

from app.seed import seed_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    asyncio.run(seed_database())
