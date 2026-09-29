# Define os endpoints

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

# Cria as tabela no PostgreSQL caso não exista
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db(): # Usamos essa função para abrir um endpoint e depois que terminar, fechar ele.
    db = SessionLocal() # Abre sessão com o banco de dados
    try:
        yield db # Entrega o db para o FastAPI.
    finally:
        db.close() # Sem isso eu teria que fechar cada endpoint manualmente

@app.post(
        '/estudantes/',
        response_model=schemas.EstudanteResponse # Valida se a Resposta está de acordo com o padrão
        )
def create_student(
    student: schemas.EstudanteCreate, # Valida se a resposta é de acordo. Se não, retorna erro
    db: Session = Depends(get_db)): # Abre a sessão com o banco de dados, envia e fecha conexão

    # Usa dado do navegador. o model_dump é pra converter HTTP em dicionário
    db_student = models.Estudante(**student.model_dump()) # O ** é para: Estudante(nome='Eduardo', idade=18).
    db.add(db_student) # Avisa o que vai ser adicionado
    db.commit() # Adiciona de fato
    db.refresh(db_student) # Atualização
    return db_student

                        # Modelo de resposta recebe uma lista (que é a do chemas)
@app.get('/estudantes/', response_model= List[schemas.EstudanteResponse]) # List serve para dizer que aquilo é uma lista
def read_students(db: Session = Depends(get_db)):

    # Como se fosse SQL. O alchemy traduz. Pega o db, BUSQUE nos (parâmetros) todas as ocorrências
    students = db.query(models.Estudante).all()
    return students  

@app.post('/matriculas/', response_model=schemas.MatriculaResponse)
def create_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    db_matricula = models.Matricula(**matricula.model_dump())
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@app.get('/matriculas/', response_model= List[schemas.MatriculaResponse])
def read_matriculas(db: Session = Depends(get_db)):
    matriculas = db.query(models.Matricula).all()
    return matriculas