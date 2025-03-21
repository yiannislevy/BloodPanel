from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base # fix in case of alembic revision to backend.database

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    height = Column(Float, nullable=True)

    sessions = relationship("TestSession", back_populates="user", cascade="all, delete-orphan")

class TestSession(Base):
    __tablename__ = "test_sessions"
    
    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    test_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    weight = Column(Float, nullable=True)

    user = relationship("User", back_populates="sessions")
    blood_tests = relationship("BloodTest", back_populates="session", cascade="all, delete-orphan")

class BloodTest(Base):
    __tablename__ = "blood_tests"
    
    test_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.session_id"), nullable=False)
    test_name = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    normal_range = Column(String, nullable=True)

    session = relationship("TestSession", back_populates="blood_tests")
