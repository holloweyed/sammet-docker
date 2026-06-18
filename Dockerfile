FROM python:3.12-slim AS builder

WORKDIR /build

RUN pip install --upgrade pip setuptools wheel

COPY pyproject.toml .

RUN pip install --prefix=/install .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src/ src/

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8101

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8101"]