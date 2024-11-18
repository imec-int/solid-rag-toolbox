FROM python:3.12-slim AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y curl jq && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/config && \
    if [ "${TARGETARCH}" = "amd64" ]; then \
      curl -L -o pkl https://github.com/apple/pkl/releases/download/0.25.3/pkl-linux-amd64 && chmod +x pkl && mv pkl /usr/local/bin/; \
    elif [ "${TARGETARCH}" = "arm64" ]; then \
      curl -L -o pkl https://github.com/apple/pkl/releases/download/0.25.3/pkl-linux-aarch64 && chmod +x pkl && mv pkl /usr/local/bin/; \
    else \
        echo "Unknown architecture: ${TARGETARCH}"; \
      exit 1; \
    fi && \
    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
ARG PIP_VERSION=24
ARG POETRY_VERSION=1.8
RUN python -m pip install --no-cache-dir -U \
"pip==$PIP_VERSION" \
"poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/home/.cache/pypoetry/cache \
    --mount=type=cache,target=/home/.cache/pypoetry/artifacts \
    poetry config virtualenvs.in-project true && \
    poetry install --without dev --no-interaction --no-ansi

COPY taskfile.yaml Schema.pkl Application.pkl ./
RUN task generate-datamodel

FROM python:3.12-slim AS release
RUN addgroup --gid 1001 app && adduser --uid 1000 --gid 1001 app
USER app
COPY --from=builder --chown=app:app /.venv /.venv
COPY --chown=app:app app ./app
COPY --from=builder --chown=app:app /app/config/config.py /app/config/config.py
CMD ["sh", "-c", ". /.venv/bin/activate && python -m app main.py"]
