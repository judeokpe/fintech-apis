# FROM python:3.11-slim AS builder

# ENV PYTHONUNBUFFERED=1
# RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

# WORKDIR /app

# COPY  app/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r /app/requirements.txt


# FROM python:3.11-slim
# WORKDIR /app
# COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/python3.11/site-packages
# COPY app /app

# RUN addgroup --system app && adduser --system --ingroup app app
# USER app
# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app /app

# Security: non-root user
RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
