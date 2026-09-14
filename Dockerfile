FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# We use the Procfile for Railway to start the correct process (web or worker)
# Default CMD in case of local docker run
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
