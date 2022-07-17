from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db.models import Base


engine = create_engine('sqlite:///scrapper.db?check_same_thread=False')

Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))
