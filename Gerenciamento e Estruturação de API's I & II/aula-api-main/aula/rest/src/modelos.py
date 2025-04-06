from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from banco_de_dados import Base


class Usuario(Base):
    __tablename__ = "tb_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)

    pedidos = relationship("Pedido", back_populates="usuario")


class Produto(Base):
    __tablename__ = "tb_produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    estoque = Column(Integer)

    pedidos_produtos = relationship("PedidoProduto", back_populates="produto")


class Pedido(Base):
    __tablename__ = "tb_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("tb_usuarios.id"))
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="pedidos")
    pedidos_produtos = relationship("PedidoProduto", back_populates="pedido")


class PedidoProduto(Base):
    __tablename__ = "tb_pedidos_produtos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("tb_pedidos.id"))
    produto_id = Column(Integer, ForeignKey("tb_produtos.id"))
    preco = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="pedidos_produtos")
    produto = relationship("Produto", back_populates="pedidos_produtos")
