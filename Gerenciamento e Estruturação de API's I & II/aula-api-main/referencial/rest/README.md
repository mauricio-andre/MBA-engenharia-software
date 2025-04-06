# README - API REST e GraphQL

Este diretório contém a implementação de uma API REST e GraphQL utilizando FastAPI. A API está configurada para rodar dentro de um ambiente Docker e se comunica com um banco de dados PostgreSQL.

## Estrutura do Projeto

```
api_rest_graphql/
├── src/
│   ├── main.py  # Ponto de entrada da aplicação
│   ├── rotas/  # Diretório contendo as rotas da API
│   ├── graphql/  # Implementação das queries e mutations GraphQL
│
├── frontend/
│   ├── html/  # Arquivos HTML para interface web
│   ├── nginx/
│   │   ├── default.conf  # Configuração do Nginx
│
├── Dockerfile  # Configuração do contêiner da API
├── docker-compose.yaml  # Orquestração dos serviços
```

## Executando o Projeto

O projeto utiliza `docker-compose` para gerenciar os serviços. Para subir os contêineres, execute o comando:

```sh
docker compose up --build
```

Isso irá iniciar os seguintes serviços:

- **API** (FastAPI) na porta `8000`
- **Banco de Dados** (PostgreSQL) na porta `5434`
- **Frontend** (Nginx) na porta `8080`

Se necessário, para parar os serviços, use:

```sh
docker-compose down
```

## Configuração dos Serviços

### API

- Porta exposta: **8000**
- Implementa endpoints REST e GraphQL.
- Configurada para usar variáveis de ambiente para conexão ao banco.
- Rota GraphQL disponível em: `/graphql`
- Comando de execução: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### PostgreSQL

- Porta exposta: **5434**
- Armazena os dados da aplicação.
- Persistência garantida pelo volume `postgres_volume`.
- Healthcheck automático para garantir que o banco está pronto antes de iniciar a API.

### Frontend

- Porta exposta: **8080**
- Servido via Nginx.
- Arquivos estáticos armazenados em `frontend/html/`.
- Configuração do servidor em `frontend/nginx/default.conf`.

## Configuração das Variáveis de Ambiente

A API utiliza algumas variáveis de ambiente para funcionamento correto. Essas variáveis devem ser definidas no `.env` ou exportadas antes da execução:

```
CONEXAO=...  # String de conexão com o banco
CHAVE_SECRETA=...  # Chave para autenticação JWT
ALGORITMO=HS256  # Algoritmo usado no JWT
TEMPO_DE_EXPIRACAO_TOKEN_DE_ACESSO=3600  # Tempo de expiração do token em segundos
CHAVE_API=...  # Chave de API para integração
POSTGRES_USER=...  # Usuário do banco
POSTGRES_PASSWORD=...  # Senha do banco
POSTGRES_DB=...  # Nome do banco
```

## Considerações Finais

Este projeto combina API REST e GraphQL, permitindo maior flexibilidade para os consumidores da API.
