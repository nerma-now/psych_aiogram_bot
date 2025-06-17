FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "-m", "bot.__main__"]