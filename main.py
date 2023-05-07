from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Pessoa, Tokens, CONN
from secrets import token_hex
import hashlib
import datetime

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
        session.add(x)
        session.commit()
        
        return {'status':'Sucesso'}
    
    elif len(usuario) > 0:
        return {'status':'Usuario já existe'}

@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()
    
    senha = hashlib.sha256(senha.encode()).hexdigest()
    logado = session.query(Pessoa).filter_by(usuario=usuario, senha=senha).all()
    
    if len(logado) == 0:
        return {'status':'Usuario já existe'}
    
    while True:
        token = token_hex(50)
        isToken = session.query(Tokens).filter_by(token=token).all()
        
        if len(isToken) == 0:
            isPessoa = session.query(Tokens).filter_by(id_pessoa=logado[0].id).all()
            if len(isPessoa) == 0:
                novoToken = Tokens(id_pessoa=logado[0].id, token=token)
                session.add(novoToken)
                session.commit()
            elif len(isPessoa) > 0:
                isPessoa[0].token = token
                
            session.commit()
            break
    return token