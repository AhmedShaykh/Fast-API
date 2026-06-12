from sqlalchemy import Column, String, Boolean, ForeignKey;
from sqlalchemy.orm import relationship;
from app.config.db import Base;
import uuid;

class Product(Base):

    __tablename__ = "product";

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()));

    title = Column(String, nullable=False);

    desc = Column(String, nullable=False);

    complete = Column(Boolean, default=False, nullable=False);

    user_id = Column(String, ForeignKey("auth.id"), nullable=False);

    user = relationship("User", backref="products");