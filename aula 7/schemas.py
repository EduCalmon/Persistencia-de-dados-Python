from typing import List, Optional

#  Descreve os dados que entram e saem da API. Com isso o pydantic pode validar os dados
from pydantic import BaseModel

"""
    Os campos aqui servem para validar os dados. Quando alguém envia um dado,
    o FastAPI, via os schemas, diz: "Esse nome existe? É string? Esse perfil existe?
"""

class Perfil(BaseModel):
    id: int
    idade: int
    endereco: str

    class Config:
        from_attributes = True

class PerfilCreate(BaseModel):
    idade: int
    endereco: str

# Estudante possui ID pois serve para mostrar ao usuário no DB
class Estudante(BaseModel):
    id: int
    nome: str
    email: str
    perfil: Optional[Perfil] = None # Pode ter um valor, ou pode ser None. Criamos assim

    # Essa configuração é feita pois o db retorna: "estudante.nome"
    # Mas o Pydantic espera um dicionário.
    class Config:
        from_attributes = True # Ele transforma um objeto em resposta de API

# EstudanteCreate não possui ID pois é criado automaticamente no DB
class EstudanteCreate(BaseModel):
    nome: str
    email: str
    perfil: PerfilCreate



class Disciplina(BaseModel):
    id: int
    nome: str

    class Config:
            from_attributes = True

class CreateDisciplina(BaseModel):
    nome: str

class Professor(BaseModel):
    id: int
    nome: str
    disciplina: Optional[Disciplina] = None

    class Config:
        from_attributes = True

class CreateProfessor(BaseModel):
    nome: str
    disciplina: Optional[CreateDisciplina] = None