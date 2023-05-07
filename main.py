from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Pessoa, Tokens, CONN
from secrets import token_hex
import hashlib
import datetime
import conexao as c

app = FastAPI()

def conectaBanco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, user: str, senha: str):
    session = conectaBanco()
    usuario = session.query(Pessoa).filter_by(usuario=user).all()
    
    if len(usuario) == 0:
        senha = hashlib.sha256(senha.encode()).hexdigest()
        x = Pessoa(nome=nome, usuario=user, senha=senha)
        session.add()
        session.commit()
        return {'status':'Sucesso'}
    elif len(usuario) > 0:
        return {'status':'Usuario já existe'}