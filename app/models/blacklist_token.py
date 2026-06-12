from sqlalchemy import Column, String;
from app.config.db import Base;
import uuid;

class BlacklistedToken(Base):

    __tablename__ = "blacklist_tokens";

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()));

    token = Column(String, unique=True, nullable=False, index=True);