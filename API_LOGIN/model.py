from sqlalchemy import create_engine, Column, Integer, String ,ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

from traitlets import default
Base = declarative_base()

#Dados para conectar ao BD
def infor_banco():
    USUARIO = ''
    SENHA = ''
    HOST = 'localhost'
    BANCO = 'apilogin'
    PORT = 0
    conn = f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}'
    engine = create_engine(conn, echo=False)
    return engine

#Retornando uma conexão para criar uma instância quando for preciso
def conect_banco():
    Session = sessionmaker(bind=infor_banco())
    return Session()

#TABELA CADASTRO
class Pessoa(Base):
    __tablename__ = 'CADASTRO'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))
    senha = Column(String(100))

#TABELA TOKENS
class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('CADASTRO.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow())

Base.metadata.create_all(infor_banco())
