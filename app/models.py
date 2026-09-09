from sqlalchemy import TIMESTAMP, Column , Integer , String , Float, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer , primary_key=True , nullable=False)
    name = Column(String , nullable=False)
    age = Column(Integer , nullable=False)
    major = Column(String , nullable=False)
    gpa = Column(Float , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") , nullable=False)

    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True , nullable=False)
    email = Column(String , nullable=False, unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False, server_default=text('now()'))
    phone = Column(String, nullable=False)

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer , ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    stu_id = Column(Integer , ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)