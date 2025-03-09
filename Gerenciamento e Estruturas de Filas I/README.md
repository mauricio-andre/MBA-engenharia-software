# README - Estruturas e Gerenciamento de Filas

Este repositório está organizado em três módulos distintos, cada um abordando um aspecto específico do uso de filas em sistemas distribuídos.

## Estrutura do Repositório

O repositório está dividido nas seguintes pastas:

- **comunicacao_microsservicos**: Exemplos e práticas sobre filas aplicadas à comunicação entre microsserviços.
- **ingestao_dados**: Demonstração do uso de filas em pipelines de ingestão e processamento de dados.
- **jobs_distribuidos**: Implementação de filas para distribuição de tarefas assíncronas entre várias instâncias de processamento.

Cada pasta possui seu próprio **README.md**, onde você encontrará instruções específicas para executar os exemplos.

## Requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- **Docker**
- **Extensão do Docker para VS Code**

## Como Executar os Exemplos

Cada módulo possui um arquivo `docker-compose.yaml`, permitindo a execução simplificada dos conteúdos. Para rodar um dos módulos:

1. Acesse a pasta correspondente, por exemplo:
   ```sh
   cd comunicacao_microsservicos
   ```
2. Inicie os containers com o Docker Compose:
   ```sh
   docker-compose up -d
   ```
3. Para interromper a execução, utilize:
   ```sh
   docker-compose down -v
   ```

## Se houver detalhes adicionais, eles serão incluídos no **README.md** de cada pasta.
