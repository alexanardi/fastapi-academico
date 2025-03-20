from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os
import uvicorn

# Configurar la conexión a PostgreSQL en Railway desde variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mIEqkmRTUmDuTxKhElzSsJclYZZOhRqs@centerbeam.proxy.rlwy.net:20887/academico")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla Estudiante
class Estudiante(Base):
    __tablename__ = "estudiante"
    __table_args__ = {"schema": "sgc"}

    idestudiante = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)

# Iniciar FastAPI
app = FastAPI()

# Dependencia para manejar sesiones con FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener todos los estudiantes
@app.get("/estudiantes")
def obtener_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# Endpoint para buscar estudiantes por apellido
@app.get("/estudiantes/{apellido}")
def buscar_por_apellido(apellido: str, db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).filter(Estudiante.apellidos == apellido).all()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes con ese apellido")
    return estudiantes

# Ejecutar la API con Uvicorn en el puerto dinámico de Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
