from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
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

    id_estudiante = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    rut = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    sexo = Column(String(1), nullable=False)
    estado = Column(String, nullable=False)

# Modelo de la tabla Estudiante_Observacion
class EstudianteObservacion(Base):
    __tablename__ = "estudiante_observacion"
    __table_args__ = {"schema": "sgc"}

    id_estudiante_observacion = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("sgc.estudiante.id_estudiante"), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String, nullable=False)

# Modelo de la tabla Estudiante_Calificacion
class EstudianteCalificacion(Base):
    __tablename__ = "estudiante_calificacion"
    __table_args__ = {"schema": "sgc"}

    id_estudiante_calificacion = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("sgc.estudiante.id_estudiante"), nullable=False)
    asignatura = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    calificacion = Column(DECIMAL(4,2), nullable=False)

# Iniciar FastAPI
app = FastAPI()

# Dependencia para manejar sesiones con FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Endpoint para obtener todos los estudiantes
@app.get("/estudiantes")
def obtener_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# ✅ Endpoint para obtener un estudiante en particular por ID
@app.get("/estudiantes/{id_estudiante}")
def obtener_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

# ✅ Endpoint para obtener todas las observaciones de un estudiante
@app.get("/estudiantes/{id_estudiante}/observaciones")
def obtener_observaciones(id_estudiante: int, db: Session = Depends(get_db)):
    observaciones = db.query(EstudianteObservacion).filter(EstudianteObservacion.id_estudiante == id_estudiante).all()
    if not observaciones:
        raise HTTPException(status_code=404, detail="No se encontraron observaciones para este estudiante")
    return observaciones

# ✅ Endpoint para obtener todas las calificaciones de un estudiante
@app.get("/estudiantes/{id_estudiante}/calificaciones")
def obtener_calificaciones(id_estudiante: int, db: Session = Depends(get_db)):
    calificaciones = db.query(EstudianteCalificacion).filter(EstudianteCalificacion.id_estudiante == id_estudiante).all()
    if not calificaciones:
        raise HTTPException(status_code=404, detail="No se encontraron calificaciones para este estudiante")
    return calificaciones

# Ejecutar la API con Uvicorn en el puerto dinámico de Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
