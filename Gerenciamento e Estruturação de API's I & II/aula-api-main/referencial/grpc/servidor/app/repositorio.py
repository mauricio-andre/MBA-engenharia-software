import redis
import json
import usuarios_pb2
import os

# Obtém a URL do Redis da variável de ambiente (ou usa um valor padrão)
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Conecta ao Redis usando a URI completa
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)


# Função para criar um usuário no Redis
def criar_usuario(usuario: usuarios_pb2.Usuario):
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha,
    }

    # Converte o dicionário para JSON
    usuario_json = json.dumps(usuario_dict)

    # Salva o usuário no Redis com a chave sendo o ID
    redis_client.set(usuario.id, usuario_json)

    return {"mensagem": f"Usuário {usuario.id} criado com sucesso no Redis!"}


# Função para obter todos os usuários do Redis
def obter_todos_usuarios():
    usuarios = []

    # Percorre todas as chaves armazenadas no Redis
    for chave in redis_client.keys():
        # Obtém o JSON armazenado e converte para dicionário
        usuario_json = redis_client.get(chave)
        if usuario_json:
            usuarios.append(
                json.loads(usuario_json)
            )  # Converte de JSON para dicionário

    return usuarios  # Retorna a lista de usuários
