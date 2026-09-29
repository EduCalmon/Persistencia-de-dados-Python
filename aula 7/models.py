from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship # cria a relação entre objetos Python e tabelas.
from database import Base # classe base do SQLAlchemy, que toda tabela/modelo precisa herdar.

class Estudante(Base):
    __tablename__ = 'estudantes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    # Aqui diz: "Um estudante tem um perfil" e " Um perfil pertence a um estudante"
    perfil = relationship('Perfil', back_populates='estudante', # O perfil saberá qual Estudante ele pertence
                          uselist=False, # relação 1 para 1, não é lista
                          cascade='all, delete-orphan') # Quando você apagar ou alterar um estudante, o perfil também será
class Perfil(Base):
    __tablename__ = 'perfis'
    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    estudante_id = Column(Integer,
                          ForeignKey('estudantes.id'),
                          unique=True) # Estudante id é único. Não posso criar outro perfil com o estudante
    estudante = relationship(
        "Estudante",
        back_populates='perfil',
        uselist=False)

    