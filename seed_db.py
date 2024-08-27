from app.models import Base, Enemy
from app.db import EnemyData, Database, engine

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config import Config

conf = Config()

db_engine = engine(conf.SQLALCHEMY_DATABASE_URI)

enemy_1_data = EnemyData(
    name='Bandit',
    max_hp=10,
    strength=3,
    potions=1,
)
enemy_2_data = EnemyData(
    name='Heavy Bandit',
    max_hp=30,
    strength=5,
    potions=2,
)

# Create database and tables
Base.metadata.create_all(db_engine)
with Session(db_engine) as session:
    database = Database(session)

# Create record
database.create(enemy_1_data)
database.create(enemy_2_data)
# Read records
# with Session(db_engine) as session:
#     # session.scalars(select(Enemy).where(Enemy.id == record_id)).one()
#     data = session.scalars(select(Enemy)).all()
#     for value in data:
#         print(value.id)
