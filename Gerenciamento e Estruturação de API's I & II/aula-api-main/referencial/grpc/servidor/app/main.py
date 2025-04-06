from concurrent import futures
import logging
import grpc
import usuarios_pb2  # Importa os módulos gerados pelo Protobuf
import usuarios_pb2_grpc  # Importa os stubs gRPC
from repositorio import criar_usuario, obter_todos_usuarios


# Implementação do serviço gRPC
class UsuariosServico(usuarios_pb2_grpc.UsuariosServicer):

    # Método para criar um novo usuário
    def CriarUsuario(self, request, context):
        # Chama a função que armazena o usuário no Redis
        resposta = criar_usuario(request.usuario)

        # Retorna a resposta contendo o usuário criado
        return usuarios_pb2.CriarUsuarioResponse(usuario=request.usuario)

    # Método para obter todos os usuários do Redis
    def ObterUsuarios(self, request, context):
        # Obtém todos os usuários armazenados no Redis
        usuarios_redis = obter_todos_usuarios()

        # Converte os usuários do Redis para a estrutura esperada pelo gRPC
        usuarios_proto = [
            usuarios_pb2.Usuario(
                id=usuario["id"],
                nome=usuario["nome"],
                email=usuario["email"],
                senha=usuario["senha"],  # ⚠️ Cuidado ao expor senhas!
            )
            for usuario in usuarios_redis
        ]

        # Retorna a resposta contendo todos os usuários
        return usuarios_pb2.ObterUsuariosResponse(usuarios=usuarios_proto)


# Função para iniciar o servidor gRPC
def iniciar_servidor():
    # Cria um servidor gRPC com um pool de threads para processar múltiplas requisições simultaneamente
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Registra o serviço UsuariosServico na instância do servidor
    usuarios_pb2_grpc.add_UsuariosServicer_to_server(UsuariosServico(), servidor)

    # Define a porta na qual o servidor irá escutar as requisições
    servidor.add_insecure_port("[::]:50051")  # Usa uma conexão não segura (para testes)

    # Inicia o servidor
    servidor.start()
    print("Servidor gRPC iniciado em: localhost:50051")

    # Mantém o servidor em execução aguardando requisições
    servidor.wait_for_termination()


if __name__ == "__main__":
    # Configuração básica de logs
    logging.basicConfig()

    # Inicia o servidor gRPC
    iniciar_servidor()
