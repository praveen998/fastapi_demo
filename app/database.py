from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://nibhasitsolutions:248646@localhost:3306/hhhperfumes"
# Create Engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Initialize Database (Create Tables)
def init_ormdb():
    Base.metadata.create_all(bind=engine)

def get_ormdb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
