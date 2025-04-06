from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configuracao import configuracoes

motor = create_engine(configuracoes.CONEXAO)

SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

Base = declarative_base()


def obter_sessao():
    db = SessaoLocal()
    try:
        return db
    finally:
        db.close()
