# README - Diretório grpc

Este diretório contém a implementação de um sistema baseado em gRPC, dividido em dois componentes principais: **cliente** e **servidor**. Ambos utilizam **protobuf** para definir as mensagens e serviços utilizados na comunicação.

## Estrutura do Projeto

O diretório `grpc` está organizado da seguinte forma:

```
grpc/
├── cliente/
│   ├── app/
│   ├── proto/
│   │   ├── usuarios.proto
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── servidor/
│   ├── app/
│   ├── proto/
│   │   ├── usuarios.proto
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker-compose.yml
```

### Descrição das Pastas

- **cliente/**: Contém a implementação do cliente gRPC que consome os serviços do servidor.

  - `proto/`: Contém os arquivos `.proto` que definem as mensagens e os serviços gRPC.
  - `app/`: Diretório contendo a implementação principal do cliente.
  - `main.py`: Arquivo de entrada do cliente.
  - `requirements.txt`: Dependências do cliente.
  - `Dockerfile`: Configuração para a construção do contêiner do cliente.

- **servidor/**: Contém a implementação do servidor gRPC.

  - `proto/`: Contém os arquivos `.proto`, os quais definem os serviços e as mensagens trocadas.
  - `app/`: Implementação principal do servidor.
  - `main.py`: Arquivo de entrada do servidor.
  - `requirements.txt`: Dependências do servidor.
  - `Dockerfile`: Configuração para a construção do contêiner do servidor.

- **docker-compose.yml**: Arquivo de configuração para orquestrar os serviços utilizando Docker Compose.

## Gerando os Arquivos gRPC a partir do Proto

Antes de rodar o cliente e o servidor, é necessário gerar os arquivos Python a partir dos arquivos `.proto`. Para isso, execute o seguinte comando dentro de cada diretório (`cliente/` e `servidor/`):

```sh
python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/usuarios.proto
```

Este comando:

- Especifica o diretório onde os arquivos `.proto` estão localizados (`-I./proto`).
- Gera os arquivos Python necessários para a comunicação gRPC (`--python_out=.` e `--grpc_python_out=.`).

## Configuração dos Serviços

O projeto é configurado utilizando `docker-compose.yaml`. Abaixo está um resumo dos serviços definidos:

### Cliente

- Porta exposta: **8000**
- Executa um servidor FastAPI para comunicação via HTTP com o usuário.
- Se conecta ao servidor gRPC.
- Comando de execução: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### Servidor

- Porta exposta: **50051**
- Implementa os serviços gRPC definidos no arquivo `usuarios.proto`.
- Utiliza Redis para armazenamento temporário.
- Comando de execução: `python main.py`

### Redis

- Porta exposta: **6379**
- Utilizado pelo servidor como cache.
- Configurado para reiniciar automaticamente em caso de falha.

## Executando o Projeto

Para rodar todos os serviços utilizando Docker Compose, execute o seguinte comando na raiz do projeto:

```sh
docker compose up --build
```

Isso irá compilar e iniciar os serviços do cliente, servidor e Redis.

Caso queira executar os serviços separadamente:

1. **Rodar o servidor:**

   ```sh
   cd servidor
   python main.py
   ```

2. **Rodar o cliente:**
   ```sh
   cd cliente
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Considerações Finais

Este projeto utiliza gRPC para comunicação eficiente entre microsserviços. A estrutura modular permite fácil manutenção e escalabilidade.
