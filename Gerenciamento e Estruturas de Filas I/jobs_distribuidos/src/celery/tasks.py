from app.celery.worker import celery, logger  # Importa a instância do Celery e o logger configurado
import time
import random
import datetime

@celery.task(name="task_with_high_latency")
def task_with_high_latency(enqueued_time=None):
    """ 
    Simula uma tarefa de longa duração no Celery.
    
    - Calcula o tempo que a tarefa ficou na fila antes de iniciar a execução.
    - Aguarda um tempo aleatório entre 17 e 20 segundos para simular uma operação lenta.
    - Registra logs do tempo total de execução e do tempo de espera na fila.
    """
    task_id = task_with_high_latency.request.id  # Obtém o ID da tarefa no Celery

    # Se a hora de enfileiramento não foi passada, assume o horário atual como referência
    if enqueued_time:
        enqueued_time = datetime.datetime.fromisoformat(enqueued_time)
    else:
        enqueued_time = datetime.datetime.utcnow()

    start_time = datetime.datetime.utcnow()  # Registra o momento em que a tarefa inicia

    # Calcula o tempo que a tarefa ficou na fila antes de ser executada
    queue_wait_time = (start_time - enqueued_time).total_seconds()

    # Define um tempo de espera aleatório para simular uma execução demorada
    delay = random.uniform(17, 20)

    try:
        time.sleep(delay)  # Simula o tempo de processamento
        logger.info(
            f"Tarefa {task_id} concluída após {delay:.2f} segundos, com {queue_wait_time:.2f} segundos na fila."
        )
        return f"Tarefa {task_id} concluída após {delay:.2f} segundos, com {queue_wait_time:.2f} segundos na fila."
    except Exception as e:
        logger.error(f"Erro na tarefa {task_id}: {e}")
        raise e  # Relança a exceção para que o Celery possa tratá-la corretamente
