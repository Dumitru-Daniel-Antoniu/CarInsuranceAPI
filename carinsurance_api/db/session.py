from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from carinsurance_api.core.config import Settings

configuration = Settings()
engine = create_engine(configuration.database_url, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
