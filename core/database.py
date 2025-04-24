from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://Jhon:Erick2017@localhost:3306/api_user"

# Crea el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Crea la sesión local para la interacción con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la base declarativa
Base = declarative_base()

# Crea la función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()  # Obtiene una sesión nueva de la base de datos
    try:
        yield db  # Devuelve la sesión para usarla en las rutas
    finally:
        db.close()  # Cierra la sesión al final