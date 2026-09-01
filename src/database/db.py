from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgress:567234@localhost:5432/rest_app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autofulush=False, bind=engine)
