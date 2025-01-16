from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)