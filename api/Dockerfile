# Usar la imagen base de Python 3.12 slim
FROM python:3.12-slim

ARG USER_ID=1000
ARG GROUP_ID=1000

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y curl build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Poetry (gestor de dependencias)
RUN curl -sSL https://install.python-poetry.org | python3 - && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Crear grupo y usuario con UID/GID personalizados
RUN groupadd -g "$GROUP_ID" appgroup && \
  useradd -m -u "$USER_ID" -g appgroup appuser

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* ./

# Argumento para entorno de desarrollo
ARG POETRY_ENV=prod

# Instalar dependencias de Poetry
RUN poetry config virtualenvs.create false && \
  if [ "$POETRY_ENV" = "dev" ]; then \
  poetry install --no-root --no-ansi --no-interaction; \
  else \
  poetry install --only main --no-root --no-ansi --no-interaction; \
  fi

# Copiar todo el código fuente de la aplicación al contenedor
COPY src /app/src

# Cambiar el dueño del directorio
RUN chown -R appuser:appgroup /app

# Exponer el puerto en el que Uvicorn escuchará
EXPOSE 8000

# Cambiar al nuevo usuario
USER appuser

# Comando para ejecutar el servidor Uvicorn con el reloader
CMD ["sh", "-c", "umask 002 && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"]
