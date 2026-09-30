# Depends: Recebe dependências, como uma conexão ao banco
from fastapi import FastAPI, Depends, HTTPException # HTTP permite devolver erros 404 e 400
from sqlalchemy.orm import Session # sessão de comunicação direta com o banco. Consultar, inserir dados, etc.
import models, schemas
from database import engine, SessionLocal
from typing import List
from sqlalchemy.orm import joinedload # Busca dados relacionados. É como o JOIN

models.Base.metadata.create_all(bind=engine) # "Leia os modelos e crie as tabelas no banco."
# metadata contém informações sobre tabelas (nomes das tabelas, colunas, tipos, etc)

app = FastAPI()

def get_db():
    db = SessionLocal() # Abro uma sessão no DB
    try:
        yield db
    finally: # Usamos finally porque mesmo que dê erro, vai executar. no caso fechar o db
        db.close()

@app.post('/estudantes/',response_model=schemas.Estudante) # Rota da API e validação dos dados
def criar_estudante(
    estudante: schemas.EstudanteCreate, # Parâmetro para criar estudante
    db: Session=Depends(get_db) # Pra entrar no banco de dados, precisa abrir uma sessão
):
    db_estudante = models.Estudante(
        nome = estudante.nome,
        email = estudante.email,
        perfil = models.Perfil(**estudante.perfil.dict())
    )
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante


@app.get('/estudantes/', response_model=List[schemas.Estudante]) # O modelo de resposta é listar os estudantes
def listar_estudantes(db: Session=Depends(get_db)): # Função get preciso apenas acessar o banco de dados
    # "Acesse o banco de dados e me traga todos do modelo Estudante"
    estudantes = (
        db.query(models.Estudante)
        .options(joinedload(models.Estudante.perfil))
        .all()
    )
    return estudantes

@app.post('/professores/', response_model=schemas.Professor)
def criar_professor(
    professor: schemas.CreateProfessor,
    db: Session=Depends(get_db)
):
    db_professor = models.Professor(
        nome=professor.nome
    )
    if professor.disciplina is not None:
        db_professor.disciplina = models.Disciplina(
            **professor.disciplina.dict()
        )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get('/professores/', response_model=List[schemas.Professor])
def listar_professores(db: Session=Depends(get_db)):
    professores = (
        db.query(models.Professor)
        .options(joinedload(models.Professor.disciplina))
        .all()
    )
    return professores