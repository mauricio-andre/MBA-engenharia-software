from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from rotas import rotas_usuarios, rotas_autenticacao, rotas_produtos, rotas_pedidos
from banco_de_dados import motor, Base
from ql_app import graphql_app
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from configuracao import limiter, logger

# Inicializando a aplicação FastAPI
app = FastAPI(
    title="API de Exemplo - FastAPI",
    version="1.0",
    description="Esta é uma API de exemplo utilizando FastAPI para demonstrar boas práticas.",
    openapi_url="/api/v1/openapi.json",
)

# Adicionando o handler para rate limit excedido
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Tratamento customizado para quando o limite for excedido
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(
        f"Rate limit excedido para {request.client.host} no endpoint {request.url.path}"
    )  # Log de aviso
    return JSONResponse(
        status_code=429,
        content={"message": "Muitas requisições, tente novamente mais tarde."},
    )


# Configuração CORS
origins = [
    "http://frontend:80",  # Para acesso dentro do Docker
    "http://localhost:8080",  # Para acesso do navegador no host
]

# Adiciona o middleware de CORS para permitir requisições de origens externas.
# - `allow_origins`: Define quais origens podem acessar a API. No caso, usamos a lista `origins`.
# - `allow_credentials`: Se `True`, permite o envio de cookies e credenciais na requisição.
# - `allow_methods`: Define quais métodos HTTP são permitidos (GET, POST, PUT, etc.). Usamos `["*"]` para permitir todos.
# - `allow_headers`: Define quais cabeçalhos podem ser incluídos na requisição. `["*"]` permite todos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rota para verificação de saúde da aplicação
@app.get("/healthz")
def healthz():
    return {"mensagem": "Aplicação está em saudável."}


# Evento de startup para log
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=motor)
    logger.info("Tabelas do banco de dados criadas com sucesso.")
    logger.info(f"CORS configurado para permitir origens: {origins}")
    logger.info("Inicialização da aplicação FastAPI...")


# Incluir as rotas
app.include_router(rotas_autenticacao.router)
app.include_router(rotas_usuarios.router)
app.include_router(rotas_produtos.router)
app.include_router(rotas_pedidos.router)
app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])
