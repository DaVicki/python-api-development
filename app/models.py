import database
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, text
from sqlalchemy import ForeignKey

class User(database.Base):
    __tablename__ = "users"
    __table_args__ = {'schema': database.SQLALCHEMY_SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Post(database.Base):
    __tablename__ = "posts"
    __table_args__ = {'schema': database.SQLALCHEMY_SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # set behaviour to cascade on delete for the below foreign key
    # so that when a user is deleted, all their posts are deleted as well
    # without having to manually delete them
    user_id = Column(Integer, ForeignKey(f"{database.SQLALCHEMY_SCHEMA_NAME}.users.id", ondelete="CASCADE"), nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
