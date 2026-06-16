from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



engine = create_engine("postgresql://postgres:Root@localhost:5432/postgres")

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)



