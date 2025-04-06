import traceback
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
import esquemas, repositorio
from banco_de_dados import obter_sessao
from sqlalchemy.orm import Session
import seguranca
from configuracao import logger, configuracoes, API_KEY_HASH

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# ------------------ Rota de Criação de Produto ------------------


@router.post(
    "/",
    response_model=esquemas.ProdutoResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(
    produto: esquemas.ProdutoCriacao,
    db: Session = Depends(obter_sessao),
    api_key_header: str = Security(APIKeyHeader(name="X-API-Key")),
):
    """
    Cria um novo produto. Retorna o produto criado com os dados.
    """
    # Tentando verificar a chave da API
    if not seguranca.verificar_api_key(api_key_header, API_KEY_HASH):
        logger.warning(
            f"Falha na autenticação: API Key inválida ou ausente. Chave recebida: {api_key_header}"
        )
        # Caso a chave da API seja inválida, levantamos uma HTTPException com status 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida ou não fornecida. Por favor, forneça uma chave válida.",
        )

    try:
        novo_produto = repositorio.criar_produto(db, produto)
        # Logando dados importantes
        logger.info(
            f"Produto criado com sucesso: {novo_produto.nome} (ID: {novo_produto.id})"
        )
        return novo_produto
    except Exception as e:
        traceback.print_exc()
        # Logando o erro
        logger.error(f"Erro ao criar produto: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ------------------ Rota para Obter Produto por ID ------------------


@router.get("/{produto_id}", response_model=esquemas.ProdutoResposta)
def obter_produto(produto_id: int, db: Session = Depends(obter_sessao)):
    """
    Retorna os dados de um produto específico. Retorna 404 caso o produto não seja encontrado.
    """
    produto = repositorio.obter_produto_por_id(db, produto_id)
    if not produto:
        logger.warning(f"Produto não encontrado: ID {produto_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    logger.info(f"Produto acessado: {produto.nome} (ID: {produto.id})")
    # Criando a resposta com HATEOAS
    return produto


# ------------------ Rota de Atualização Completa de Produto ------------------


@router.put("/{produto_id}", response_model=esquemas.ProdutoResposta)
def atualizar_produto(
    produto_id: int,
    produto: esquemas.ProdutoAtualizacao,
    db: Session = Depends(obter_sessao),
    api_key_header: str = Security(APIKeyHeader(name="X-API-Key")),
):
    """
    Atualiza os dados de um produto existente. O ID do produto deve ser fornecido.
    Retorna os dados atualizados do produto.
    """

    # Tentando verificar a chave da API
    if not seguranca.verificar_api_key(api_key_header, API_KEY_HASH):
        logger.warning(
            f"Falha na autenticação: API Key inválida ou ausente. Chave recebida: {api_key_header}"
        )
        # Caso a chave da API seja inválida, levantamos uma HTTPException com status 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida ou não fornecida. Por favor, forneça uma chave válida.",
        )

    produto_atualizado = repositorio.atualizar_produto(db, produto_id, produto)
    if not produto_atualizado:
        logger.warning(
            f"Tentativa de atualização de produto não encontrado: ID {produto_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    logger.info(
        f"Produto atualizado com sucesso: {produto_atualizado.nome} (ID: {produto_atualizado.id})"
    )
    return produto_atualizado


# ------------------ Rota para Deletar um Produto ------------------


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(obter_sessao),
    api_key_header: str = Security(APIKeyHeader(name="X-API-Key")),
):
    """
    Deleta um produto existente. O ID do produto deve ser fornecido.
    Retorna HTTP 204 (Sem Conteúdo) se deletado com sucesso.
    """
    # Tentando verificar a chave da API
    if not seguranca.verificar_api_key(api_key_header, API_KEY_HASH):
        logger.warning(
            f"Falha na autenticação: API Key inválida ou ausente. Chave recebida: {api_key_header}"
        )
        # Caso a chave da API seja inválida, levantamos uma HTTPException com status 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida ou não fornecida. Por favor, forneça uma chave válida.",
        )
    if not repositorio.deletar_produto(db, produto_id):
        logger.warning(
            f"Tentativa de deletação de produto não encontrado: ID {produto_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    logger.info(f"Produto deletado com sucesso: ID {produto_id}")
    return {"msg": "Produto deletado com sucesso."}
