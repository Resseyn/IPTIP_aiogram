from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, Sequence('students_student_id_seq'), primary_key=True)
    telegram_nickname = Column(String(256), nullable=False)
    surname = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    telephone_number = Column(String(16), nullable=False)
    group = Column(String(10), nullable=False)
    institution = Column(String(10), nullable=False)
    status = Column(String(30), nullable=False)
    tg_chat_id = Column(Integer, nullable=False)
