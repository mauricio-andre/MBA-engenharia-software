# Gerenciamento e Estruturas de APIs

## 📌 Descrição

Este material faz parte da aula de Gerenciamento e Estruturas de APIs, incluindo configuração de ambientes Docker para diferentes tipos de APIs. Existem dois diretórios principais:

- **aula/**: Contém o ambiente de desenvolvimento prático da aula.
- **referencial/**: Contém exemplos de referência para estudo e acompanhamento.

Cada diretório possui os subdiretórios:

- **grpc/**: Para APIs baseadas em gRPC.
- **rest/**: Para APIs REST convencionais e GraphQL.

Todos os subdiretórios contêm um arquivo `docker-compose.yaml` para facilitar o provisionamento dos containers.

---

## 📦 Requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados:

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- [VS Code](https://code.visualstudio.com/)
- Extensão **Docker** para VS Code
- [Thunder Client] (para testes de APIs REST)
- [vscode-proto3] (suporte ao Protobuf 3 no VS Code)

---

## 🚀 Como Executar

1. **Entre no diretório da aula ou do referencial**

   ```sh
   cd aula  # ou "cd referencial"
   ```

2. **Suba os containers**

   ```sh
   docker compose up -d
   ```

3. **Verifique os containers em execução**

   ```sh
   docker ps
   ```

4. **Acesse as APIs**

   - Para REST, use o Thunder Client ou o `curl`

5. **Para parar os containers**
   ```sh
   docker compose down
   ```

---

## 📚 Estrutura do Projeto

```
/aula/
│   ├── grpc/
│   │   ├── docker-compose.yaml
│   ├── rest/
│   │   ├── docker-compose.yaml
│
/referencial/
│   ├── grpc/
│   │   ├── docker-compose.yaml
│   ├── rest/
│   │   ├── docker-compose.yaml
```

---
