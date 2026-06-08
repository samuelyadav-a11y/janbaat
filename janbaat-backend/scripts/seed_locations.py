"""
Location seed script — populates states, districts, cities.

Data source: https://github.com/dr5hn/countries-states-cities-database
File needed: india_states_districts_cities.json

Usage:
    python scripts/seed_locations.py

Expected counts after run:
    States:    36  (28 states + 8 UTs)
    Districts: ~766
    Cities:    ~8000+
"""
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# ─── Inline data: All 36 Indian States + UTs ─────────────────────────────────
# Full districts/cities loaded from JSON file (see DATA_FILE below)
STATES = [
    ("Andhra Pradesh", "AP"), ("Arunachal Pradesh", "AR"), ("Assam", "AS"),
    ("Bihar", "BR"), ("Chhattisgarh", "CG"), ("Goa", "GA"),
    ("Gujarat", "GJ"), ("Haryana", "HR"), ("Himachal Pradesh", "HP"),
    ("Jharkhand", "JH"), ("Karnataka", "KA"), ("Kerala", "KL"),
    ("Madhya Pradesh", "MP"), ("Maharashtra", "MH"), ("Manipur", "MN"),
    ("Meghalaya", "ML"), ("Mizoram", "MZ"), ("Nagaland", "NL"),
    ("Odisha", "OD"), ("Punjab", "PB"), ("Rajasthan", "RJ"),
    ("Sikkim", "SK"), ("Tamil Nadu", "TN"), ("Telangana", "TS"),
    ("Tripura", "TR"), ("Uttar Pradesh", "UP"), ("Uttarakhand", "UK"),
    ("West Bengal", "WB"),
    # Union Territories
    ("Andaman and Nicobar Islands", "AN"), ("Chandigarh", "CH"),
    ("Dadra and Nagar Haveli and Daman and Diu", "DD"), ("Delhi", "DL"),
    ("Jammu and Kashmir", "JK"), ("Ladakh", "LA"),
    ("Lakshadweep", "LD"), ("Puducherry", "PY"),
]

DATA_FILE = Path(__file__).parent / "india_locations.json"


async def seed(session: AsyncSession) -> None:
    # Check if already seeded
    result = await session.execute(text("SELECT COUNT(*) FROM states"))
    count = result.scalar()
    if count and count > 0:
        print(f"States already seeded ({count} rows). Skipping.")
        return

    print("Seeding states...")
    state_id_map: dict[str, int] = {}
    for name, code in STATES:
        result = await session.execute(
            text("INSERT INTO states (name, code) VALUES (:name, :code) RETURNING id"),
            {"name": name, "code": code},
        )
        state_id_map[code] = result.scalar_one()
    await session.commit()
    print(f"  ✓ {len(STATES)} states inserted")

    if not DATA_FILE.exists():
        print(f"\nWARNING: {DATA_FILE} not found.")
        print("Download from: https://github.com/dr5hn/countries-states-cities-database")
        print("Save as: scripts/india_locations.json")
        print("Format expected: { 'AP': { 'districts': { 'Anantapur': ['Anantapur', ...] } } }")
        print("\nStates seeded. Run again after adding the JSON file for districts/cities.")
        return

    print("Seeding districts and cities from JSON...")
    with open(DATA_FILE) as f:
        data = json.load(f)

    district_count = 0
    city_count = 0

    for state_code, state_data in data.items():
        state_id = state_id_map.get(state_code)
        if not state_id:
            print(f"  WARNING: Unknown state code {state_code}, skipping")
            continue

        for district_name, cities in state_data.get("districts", {}).items():
            result = await session.execute(
                text("INSERT INTO districts (state_id, name) VALUES (:sid, :name) RETURNING id"),
                {"sid": state_id, "name": district_name},
            )
            district_id = result.scalar_one()
            district_count += 1

            for city_name in cities:
                await session.execute(
                    text("INSERT INTO cities (district_id, name) VALUES (:did, :name)"),
                    {"did": district_id, "name": city_name},
                )
                city_count += 1

        await session.commit()

    print(f"  ✓ {district_count} districts inserted")
    print(f"  ✓ {city_count} cities inserted")
    print("\nSeeding complete!")


async def main() -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
