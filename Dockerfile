# 1. Usa uma imagem oficial do Python, muito mais leve que o Ubuntu completo
FROM python:3.12-slim

# 2. Instala dependências do sistema necessárias (como git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ARGUMENTO PARA QUEBRAR O CACHE DO GIT (Substitua por qualquer valor/data ao dar build para forçar o pull)
ARG CACHEBUST=1

# 3. Clona o repositório garantindo que ele baixe as atualizações
RUN git clone https://github.com/CauaGoms/Hemotec.git .

# 4. Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Em produção, use mais de um worker para aguentar requisições simultâneas
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]