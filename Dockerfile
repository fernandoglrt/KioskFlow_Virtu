# Usa Python 3.12 (A versão estável que combinamos)
FROM python:3.12-slim

# Evita que o Python crie arquivos .pyc e força logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copia o requirements e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . /app/

# Expõe a porta 8000
EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]