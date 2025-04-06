from fastapi import APIRouter, Depends, HTTPException, status
import esquemas, repositorio
from banco_de_dados import obter_sessao
from sqlalchemy.orm import Session
from oath2 import obter_usuario_atual
import modelos
from configuracao import logger
import traceback
from typing import List
from fastapi import Query


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# ------------------ Rota para Criar Pedido ------------------


@router.post(
    "/",
    response_model=esquemas.PedidoResposta,
    status_code=status.HTTP_201_CREATED,
)
def criar_pedido(
    pedido: esquemas.PedidoCriacao,
    db: Session = Depends(obter_sessao),
    usuario_atual: modelos.Usuario = Depends(obter_usuario_atual),
):
    """
    Cria um novo pedido para o usuário autenticado. Retorna o pedido criado.
    """
    try:
        novo_pedido = repositorio.criar_pedido(db, usuario_atual.id, pedido)
        logger.info(
            f"Pedido criado com sucesso: {novo_pedido.id} (Usuário: {usuario_atual.nome})"
        )

        return esquemas.PedidoResposta(
            id=novo_pedido.id,
            usuario_id=usuario_atual.id,
            produtos=[produto.produto_id for produto in novo_pedido.pedidos_produtos],
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Erro ao criar pedido: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{pedido_id}",
    response_model=esquemas.PedidoRespostaComLinks,
    status_code=status.HTTP_200_OK,
)
def obter_pedido(
    pedido_id: int,
    db: Session = Depends(obter_sessao),
    usuario_atual: modelos.Usuario = Depends(obter_usuario_atual),
):
    """
    Retorna os detalhes de um pedido específico do usuário atual.
    """
    try:
        pedido = repositorio.obter_pedido_por_id(db, pedido_id)
        if not pedido or pedido.usuario_id != usuario_atual.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado."
            )
        # Criando links HATEOAS para o pedido
        return esquemas.PedidoRespostaComLinks(
            id=pedido.id,
            usuario_id=pedido.usuario_id,
            produtos=[produto.produto_id for produto in pedido.pedidos_produtos],
            links=[
                {"rel": "self", "href": f"/pedidos/{pedido.id}", "method": "GET"},
                {"rel": "create", "href": f"/pedidos/", "method": "POST"},
                {"rel": "update", "href": f"/pedidos/{pedido.id}", "method": "PUT"},
                {"rel": "delete", "href": f"/pedidos/{pedido.id}", "method": "DELETE"},
            ],
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Erro ao obter pedido {pedido_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/{pedido_id}",
    response_model=esquemas.PedidoResposta,
    status_code=status.HTTP_200_OK,
)
def atualizar_pedido(
    pedido_id: int,
    pedido: esquemas.PedidoAtualizacao,
    db: Session = Depends(obter_sessao),
    usuario_atual: modelos.Usuario = Depends(obter_usuario_atual),
):
    """
    Atualiza um pedido existente do usuário atual. Retorna os dados do pedido atualizado.
    """
    try:
        pedido_atualizado = repositorio.atualizar_pedido(db, pedido_id, pedido)
        if not pedido_atualizado or pedido_atualizado.usuario_id != usuario_atual.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado."
            )
        return pedido_atualizado
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Erro ao atualizar pedido {pedido_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_pedido(
    pedido_id: int,
    db: Session = Depends(obter_sessao),
    usuario_atual: modelos.Usuario = Depends(obter_usuario_atual),
):
    """
    Deleta um pedido existente do usuário atual. Retorna HTTP 204 (Sem Conteúdo) se deletado com sucesso.
    """
    try:
        if repositorio.deletar_pedido(db, pedido_id):
            logger.info(f"Pedido {pedido_id} deletado com sucesso")
            return {"msg": "Pedido deletado com sucesso."}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado."
            )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Erro ao deletar pedido {pedido_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
