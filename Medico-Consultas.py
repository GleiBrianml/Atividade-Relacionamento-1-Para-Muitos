from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

Base = declarative_base()

class Medico(Base):
    __tablename__ = "medico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    consultas = relationship("Consulta", back_populates="medico")

    def __repr__(self):
        return f"Medico: ID = {self.id} - NOME = {self.nome}"
    
class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    nome_paciente = Column(String(100), nullable=False)
    idade_paciente = Column(Integer, nullable=False)
    data_consulta = Column(DateTime, default=datetime.datetime.utcnow )


    medico_id = Column(Integer, ForeignKey("medico.id"))

    medico = relationship("Medico", back_populates= "consultas")

    def __repr__(self):
        return f"Consultas: ID = {self.id} - nome_paciente = {self.nome_paciente} idade_paciente = {self.idade_paciente} - data_consulta ={self.data_consulta}"
