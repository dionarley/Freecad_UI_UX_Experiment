# Container mínimo para rodar os testes do Freecad_UI_UX_Experiment
FROM python:3.11-slim

ENV QT_QPA_PLATFORM=offscreen \
    PIP_NO_CACHE_DIR=1 \
    UV_NO_CACHE=1

WORKDIR /app

# Instala uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copia apenas os arquivos de dependência primeiro (cache de camada)
COPY pyproject.toml uv.lock ./

# Instala dependências de dev (pytest)
RUN uv sync --frozen --group dev

# Copia o restante do projeto
COPY . .

# Roda os testes por padrão
CMD ["uv", "run", "pytest", "-q"]
