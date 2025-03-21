from fastapi import FastAPI
from celery.result import AsyncResult
from app.celery.worker import celery  # Importa a instância do Celery configurada
from app.celery.tasks import task_with_high_latency  # Importa a tarefa de longa duração
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Define um modelo de saída para representar o status da tarefa no retorno da API
class CeleryTaskOutputDto(BaseModel):
    state: str  # Estado atual da tarefa (pendente, em execução, concluída, etc.)
    output: Optional[str] = None  # Resultado da tarefa, se disponível

# Inicializa a aplicação FastAPI
app = FastAPI()

@app.post("/start-task")
def start_task():
    """Inicia uma tarefa Celery assíncrona e retorna seu ID."""
    task = task_with_high_latency.delay(enqueued_time=datetime.utcnow().isoformat())
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    """Obtém o status e resultado (se disponível) de uma tarefa Celery pelo ID."""
    task_result = AsyncResult(task_id, app=celery)
    return CeleryTaskOutputDto(state=task_result.state, output=task_result.info)
