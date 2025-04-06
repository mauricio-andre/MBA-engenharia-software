from fastapi import FastAPI, Request
import grpc
import usuarios_pb2  # Importa os módulos gerados pelo Protobuf
import usuarios_pb2_grpc  # Importa os stubs gRPC
from pydantic import BaseModel
import time
from uuid import uuid4

# Inicializa a aplicação FastAPI
app = FastAPI()


@app.middleware("http")
async def medir_tempo_requisicao(request: Request, call_next):
    inicio = time.time()
    response = await call_next(request)
    fim = time.time()
    duracao = fim - inicio

    print(f"⏱️ Tempo de resposta para {request.url.path}: {duracao:.4f} segundos")
    return response


# Criar um canal e stub globais para reutilização
grpc_canal = grpc.aio.insecure_channel("servidor:50051")
grpc_stub = usuarios_pb2_grpc.UsuariosStub(grpc_canal)


# Definição do modelo de entrada da API
class UsuarioInput(BaseModel):
    nome: str
    email: str
    senha: str


# Função assíncrona para criar um usuário via gRPC (usando stub global)
async def chamar_grpc_criar_usuario(usuario: UsuarioInput):
    usuario_grpc = usuarios_pb2.Usuario(
        id=str(uuid4()),
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
    )

    resposta = await grpc_stub.CriarUsuario(
        usuarios_pb2.CriarUsuarioRequest(usuario=usuario_grpc)
    )
    return resposta.usuario


# Função assíncrona para buscar os usuários do serviço gRPC (usando stub global)
async def chamar_grpc_obter_usuarios():
    resposta = await grpc_stub.ObterUsuarios(usuarios_pb2.ObterUsuariosRequest())
    return resposta.usuarios


# Rota HTTP para obter a lista de usuários
@app.get("/usuarios")
async def listar_usuarios():
    usuarios = await chamar_grpc_obter_usuarios()
    return {
        "usuarios": [
            {"id": usuario.nome, "nome": usuario.nome, "email": usuario.email}
            for usuario in usuarios
        ]
    }


# Rota HTTP para criar um novo usuário via gRPC
@app.post("/usuarios")
async def criar_usuario(usuario: UsuarioInput):
    usuario_criado = await chamar_grpc_criar_usuario(usuario)
    return {"mensagem": "Usuário criado com sucesso!", "usuario": usuario_criado.nome}
