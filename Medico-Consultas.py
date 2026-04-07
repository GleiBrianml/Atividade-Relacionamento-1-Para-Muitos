from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import pytz
Base = declarative_base()
data_hora_br = Column(DateTime(timezone=True), nullable=False)
class Medico(Base):
    __tablename__ = "medico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    consultas = relationship("Consulta", back_populates="medico")

    def __repr__(self):
        return f"Medico: ID = {self.id} - NOME = {self.nome}"
    
class Consulta(Base):
    __tablename__ = "consultas"
    br_tz = pytz.timezone('America/Sao_Paulo')
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    sintomas = Column(String(100), nullable=False)
    data_consulta = Column(DateTime, default=datetime.datetime.now(br_tz),onupdate=datetime.datetime.now(br_tz))


    medico_id = Column(Integer, ForeignKey("medico.id"))

    medico = relationship("Medico", back_populates= "consultas")

    def __repr__(self):
        return f"Consultas: ID = {self.id} - nome = {self.nome} - sintomas = {self.sintomas} - data_consulta ={self.data_consulta}"

engine = create_engine("sqlite:///hospital.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def cadastrar_medico():
    nome_medico = input("Digite o nome do Medico: ").strip().capitalize()

    with Session() as session:
        try:
            medico = Medico(nome = nome_medico)
            session.add(medico)
            session.commit()
            print("Medico cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def cadastrar_consultas():
    nome_paciente = input("Digite o nome do paciente: ").strip().capitalize()
    sintoma_paciente = input("Digite o que o paciente as sentindo: ").strip().capitalize()

    buscar_medico = input(f"DIgite o nome do medico da consulta do paciente {nome_paciente}: "). strip().capitalize()

    with Session() as session:
        try:
            medico = session.query(Medico).filter_by(nome=buscar_medico).first()
            if medico == None:
                print("Não foi encontrado nenhum medico com esse nome")
            else:
                consulta = Consulta(nome = nome_paciente, sintomas = sintoma_paciente, medico=medico)
                session.add(consulta)
                session.commit()
                print("Consulta cadastrada com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

            
#cadastrar_medico()

#cadastrar_consultas()

def listar_consulta():
    with Session() as session:
        try:
            consultas =  session.query(Consulta).all()
            for cons in consultas:
                print(f"\n Paciente: {cons.nome} - Medico: {cons.medico.nome} - Sintoma: {cons.sintomas}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# listar_consulta()

def listar_avancada():
    with Session() as session:
        try:
            consultas = session.query(Consulta).filter(Consulta.medico_id == 1).all()
            for cons in consultas:
                print(f"\n Paciente: {cons.nome} - Medico: {cons.medico.nome} - Sintoma: {cons.sintomas}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# listar_avancada()

def atualizar_medico():
    with Session() as session:
        try:
            novo_nome_paciente = input("Digite o nome do paciente: ").strip().capitalize()
            novo_sintoma = input(f"Digite o novo sintoma do paciente {novo_nome_paciente}: ").strip().capitalize()
            novo_medico = input("Digite o nome do novo medico: ").strip().capitalize()


            consulta = session.query(Consulta).filter_by(nome=novo_nome_paciente).first()
            medico = session.query(Medico).filter_by(nome=novo_medico).first()

            consulta.sintomas = novo_sintoma
            consulta.nome = novo_nome_paciente
            consulta.medico = novo_medico

            session.commit()
            print("Consulta atualizada com sucesso!")
            listar_consulta()
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")    

atualizar_medico()
        