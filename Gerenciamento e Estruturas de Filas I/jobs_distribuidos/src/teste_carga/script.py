from locust import HttpUser, task, between  # Importa a classe base HttpUser e funções para definir testes de carga
import requests  # Importa a biblioteca para lidar com requisições HTTP

class PerformanceTests(HttpUser):
    """
    Classe de teste de desempenho usando Locust.
    
    - Simula usuários enviando requisições para o endpoint `/start-task`.
    - Define um intervalo aleatório de espera entre as requisições para simular comportamento real de usuários.
    """
    
    # Define um tempo de espera aleatório entre 5 e 10 segundos entre cada requisição
    wait_time = between(5, 10)

    @task(1)
    def trigger_task(self):
        """
        Envia uma requisição POST para o endpoint `/start-task` para iniciar uma tarefa assíncrona.
        
        - Define cabeçalhos apropriados para JSON.
        - Adiciona um timeout de 30 segundos para evitar bloqueios longos.
        - Implementa tratamento de exceções para falhas na requisição.
        """
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = self.client.post("/start-task", headers=headers, timeout=30)
            response.raise_for_status()  # Lança um erro se a resposta não for um código 2xx
        except requests.exceptions.Timeout:
            print("A requisição excedeu o tempo limite de 30 segundos")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
