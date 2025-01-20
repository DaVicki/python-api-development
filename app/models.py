import database
from config import settings
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(database.Base):
    __tablename__ = "users"
    __table_args__ = {'schema': settings.database_schema}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Post(database.Base):
    __tablename__ = "posts"
    __table_args__ = {'schema': settings.database_schema}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # set behaviour to cascade on delete for the below foreign key
    # so that when a user is deleted, all their posts are deleted as well
    # without having to manually delete them
    owner_id = Column(Integer, ForeignKey(f"{settings.database_schema}.users.id", ondelete="CASCADE"), nullable=False)
    # user
    owner = relationship("User")
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(database.Base):
    __tablename__ = "votes"
    __table_args__ = {'schema': settings.database_schema}

    post_id = Column(Integer, ForeignKey(f"{settings.database_schema}.posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey(f"{settings.database_schema}.users.id", ondelete="CASCADE"), primary_key=True)
