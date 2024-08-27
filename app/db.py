from sqlalchemy.orm import Session
from .models import Base, Enemy
from .enemy_data import EnemyData
from sqlalchemy import select, create_engine

def engine(uri):
    return create_engine(uri, echo=True)

class Database:
    def __init__(self, session: Session):
        self.session = session

    def create(self, enemy_data: EnemyData) -> int:
        enemy = Enemy(**enemy_data.__dict__)
        self.session.add(enemy)
        self.session.commit()
        return enemy.id

    def read(self, record_id: int) -> Enemy:
        data = self.session.scalars(select(Enemy).where(Enemy.id == record_id)).one()
        return data

    def update(
            self,
            record_id: int,
            enemy_data: EnemyData
    ):
        record = self.read(record_id)
        for attribute, value in enemy_data.__dict__.items():
            if value:
                setattr(record, attribute, value)
        self.session.commit()

    def delete(
            self,
            record_id: int,
    ):
        record = self.read(record_id)
        self.session.delete(record)
        self.session.commit()
