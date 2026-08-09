FROM python:3.11-slim

# Install system nmap binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment Defaults
ENV SCANNER_ENV=production \
    DATABASE_URL=sqlite:///./data/scanner.db \
    OUTPUT_DIR=./reports

VOLUME ["/app/data", "/app/reports", "/app/logs"]

ENTRYPOINT ["python", "-m", "app.cli.main"]
CMD ["--help"]
