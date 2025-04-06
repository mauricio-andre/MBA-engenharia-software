from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ------------------ Usuário ------------------


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True  # Permite que o modelo seja convertido para o formato ORM


class UsuarioCriacao(UsuarioBase):
    senha: str  # Campo para senha na criação do usuário


class UsuarioAtualizacao(BaseModel):
    nome: Optional[str]  # Pode ser atualizado ou deixado em branco
    email: Optional[EmailStr]  # Pode ser atualizado ou deixado em branco
    senha: Optional[str]  # Pode ser atualizado ou deixado em branco

    class Config:
        orm_mode = True


class UsuarioResposta(UsuarioBase):
    id: int  # ID do usuário que será retornado após criação ou consulta

    class Config:
        orm_mode = True


class UsuarioRespostaComLinks(UsuarioBase):
    id: int
    links: List[dict]

    class Config:
        orm_mode = True


# ------------------ Resposta de Autenticação ------------------


class Token(BaseModel):
    access_token: str
    token_type: str


# ------------------ Produto ------------------


class ProdutoBase(BaseModel):
    nome: str  # Nome do produto
    preco: float  # Preço do produto
    estoque: int  # Quantidade disponível no estoque

    class Config:
        orm_mode = True


class ProdutoCriacao(ProdutoBase):
    pass  # ProdutoCriacao é igual a ProdutoBase, apenas para operações de criação


class ProdutoAtualizacao(BaseModel):
    nome: Optional[str]  # Nome do produto pode ser atualizado
    preco: Optional[float]  # Preço do produto pode ser atualizado
    estoque: Optional[int]  # Estoque do produto pode ser atualizado

    class Config:
        orm_mode = True


class ProdutoResposta(ProdutoBase):
    id: int  # ID do produto para ser retornado após criação ou consulta

    class Config:
        orm_mode = True


class ProdutoRespostaComLinks(ProdutoBase):
    id: int
    links: List[dict]

    class Config:
        orm_mode = True


# ------------------ Pedido ------------------


class PedidoBase(BaseModel):
    produtos: List[int]  # Lista de IDs dos produtos no pedido

    class Config:
        orm_mode = True


class PedidoCriacao(PedidoBase):
    pass  # PedidoCriacao é igual a PedidoBase, apenas para operações de criação


class PedidoAtualizacao(BaseModel):
    produtos: Optional[List[int]]  # Pode atualizar a lista de produtos no pedido

    class Config:
        orm_mode = True


class PedidoResposta(PedidoBase):
    id: int  # ID do pedido para ser retornado após criação ou consulta
    usuario_id: int  # ID do usuário associado ao pedido

    class Config:
        orm_mode = True


class PedidoRespostaComLinks(PedidoBase):
    id: int
    usuario_id: int
    links: List[dict]  # Links HATEOAS

    class Config:
        orm_mode = True
