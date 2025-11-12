FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y git curl python3-venv pip && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y default-jre curl unzip

# Instalar git
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Instalar FreeTXL 10.8b
RUN curl -L -o /tmp/freetxl.tar.gz https://txl.ca/download/25536-txl10.8b.linux64.tar.gz && \
    mkdir -p /opt/txl && \
    tar -xzf /tmp/freetxl.tar.gz -C /opt/txl --strip-components=1 && \
    chmod +x /opt/txl/bin/txl && \
    ln -sf /opt/txl/bin/txl /usr/local/bin/txl && \
    rm /tmp/freetxl.tar.gz

# Instalar Poetry (método recomendado)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . .

# Desabilitar criação de virtualenv
RUN poetry config virtualenvs.create false

# Instalar dependências do projeto a partir do pyproject.toml
RUN poetry lock
RUN poetry install --no-interaction --no-ansi

# Expor porta da API Flask
EXPOSE 5000

# Comando padrão para iniciar a app
CMD ["python3", "main.py"]



