from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class Feed(Base):
    __tablename__ = "feed_data"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User")
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    post = relationship("Post")
    action = Column(String)
    time = Column(TIMESTAMP)
