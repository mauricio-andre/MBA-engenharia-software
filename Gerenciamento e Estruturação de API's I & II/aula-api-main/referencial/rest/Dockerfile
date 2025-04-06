# Usa a imagem oficial do Python 3.9 do Docker Hub
FROM python:3.9-alpine

# Copia todo o diretório da máquina host para dentro do container na pasta raíz
COPY . .

# Atualiza o pip e o setuptools para as versões mais recentes e instala o Cython
RUN pip3 install --upgrade pip

# Instala as dependências do Python listadas no requirements.txt
RUN pip install -r requirements.txt

# Define o comando padrão a ser executado quando o container iniciar
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
