import database
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, text

class Post(database.Base):
    __tablename__ = "posts"
    __table_args__ = {'schema': database.SQLALCHEMY_SCHEMA_NAME}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))