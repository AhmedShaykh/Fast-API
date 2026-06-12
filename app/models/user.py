from sqlalchemy import Column, String, DateTime;
from app.config.db import Base;
from datetime import datetime;
import uuid;

class User(Base):

    __tablename__ = "auth";

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()));

    email = Column(String, unique=True, nullable=False, index=True);

    password = Column(String, nullable=False);

    fullname = Column(String, nullable=False);

    created = Column(DateTime, default=datetime.utcnow);

    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow);