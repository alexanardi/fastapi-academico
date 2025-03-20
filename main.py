from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar la conexión a PostgreSQL en Railway
DATABASE_URL = "postgresql://postgres:mIEqkmRTUmDuTxKhElzSsJclYZZOhRqs@centerbeam.proxy.rlwy.net:20887/academico"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla Estudiante
class estudiante(Base):
    __tablename__ = "estudiante"
    __table_args__ = {"schema": "sgc"}

    idestudiante = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# Iniciar FastAPI
app = FastAPI()

# Dependencia para manejar sesiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener todos los estudiantes
@app.get("/estudiantes")
def obtener_estudiantes():
    db = SessionLocal()
    estudiantes = db.query(estudiante).all()
    db.close()
    return estudiantes

# Endpoint para buscar estudiantes por apellido
@app.get("/estudiantes/{apellido}")
def buscar_por_apellido(apellido: str):
    db = SessionLocal()
    estudiantes = db.query(estudiante).filter(estudiante.apellidos == apellido).all()
    db.close()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes con ese apellido")
    return estudiantes
