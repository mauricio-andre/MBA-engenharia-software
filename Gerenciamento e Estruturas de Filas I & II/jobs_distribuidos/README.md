# Jobs Distribuídos

Este diretório contém exemplos de implementação de filas para distribuição de tarefas assíncronas entre várias instâncias de processamento.

## Requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- **Docker**
- **Extensão do Docker para VS Code**

## Como Executar os Exemplos

1. Acesse a pasta do módulo:

sh
cd jobs_distribuidos

2. Inicie os containers com o Docker Compose:

sh
docker-compose up -d

3. Para interromper a execução, utilize:

sh
docker-compose down -v

### Endpoints Disponíveis

- **Flower (Monitoramento do Celery)**: [http://localhost:5555](http://localhost:5555)
- **RabbitMQ**: [http://localhost:15672](http://localhost:15672)
- **Locust (Teste de Carga)**: [http://localhost:8089](http://localhost:8089)
- **API Principal**: [http://localhost:8000](http://localhost:8000)
- **Documentação da API**: [http://localhost:8000/docs](http://localhost:8000/docs)

Caso não consiga acessar um endpoint usando localhost, tente 0.0.0.0 ou 127.0.0.1.
