import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List
import repositorio, esquemas
from banco_de_dados import obter_sessao


# Definir o modelo de usuário para GraphQL
@strawberry.type
class UsuariosGraphQL:
    id: int
    nome: str
    email: str


# Resolver a query para obter os usuários
@strawberry.type
class Query:
    @strawberry.field
    async def usuarios(self) -> List[UsuariosGraphQL]:
        db = obter_sessao()
        usuarios = repositorio.obter_usuarios(db)
        return [
            UsuariosGraphQL(id=usuario.id, nome=usuario.nome, email=usuario.email)
            for usuario in usuarios
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def criar_usuario(self, nome: str, email: str, senha: str) -> UsuariosGraphQL:
        db = obter_sessao()
        usuario = repositorio.criar_usuario(
            db, usuario=esquemas.UsuarioCriacao(nome=nome, email=email, senha=senha)
        )
        return UsuariosGraphQL(id=usuario.id, nome=usuario.nome, email=usuario.email)


# Configuração do schema GraphQL com Query e Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Configuração do Router GraphQL
graphql_app = GraphQLRouter(schema)
