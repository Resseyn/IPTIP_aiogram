from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from data.configs import postgres_query


engine = create_engine(postgres_query)
connection = engine.connect()

metadata = MetaData()

students = Table('students', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()
