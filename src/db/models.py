from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Table, String

Base = declarative_base()


appartment_user_association_table = Table(
    'appartment_seen_by', Base.metadata,
    Column('user_id', ForeignKey('user.id', ondelete='CASCADE')),
    Column('appartment_id', ForeignKey('appartment.id', ondelete='CASCADE'))
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)


class Appartment(Base):
    __tablename__ = 'appartment'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=True)
    czynsz = Column(Integer, nullable=True)
    name = Column(String)
    rooms = Column(Integer)
    scrapped_at = Column(DateTime, server_default=func.NOW())
    users = relationship('User', secondary=appartment_user_association_table, backref='appartments')

    def __str__(self):
        return f"{self.name}\n" \
               f"price: {self.price}\n" \
               f"czynsz: {self.czynsz}\n" \
               f"rooms: {self.rooms}\n" \
               f"when scrapped: {self.scrapped_at}"
