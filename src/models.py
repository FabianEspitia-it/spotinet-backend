from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.sql import func

from src.database import engine, Base


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    disney_password = Column(String(255))
    netflix_password = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())


Base.metadata.create_all(bind=engine)
