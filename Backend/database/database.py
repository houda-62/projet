"""""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données (PostgreSQL ou SQLite)
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://projet1user:Tile62@localhost:5432/projet1db"

# Crée le moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crée une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""