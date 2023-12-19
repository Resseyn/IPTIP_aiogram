from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

from data.orm_classes import Student

engine = create_engine('postgresql://postgres:testtest@localhost:5432/iptip_bot')
connection = engine.connect()

metadata = MetaData()

students = Table('students', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()
