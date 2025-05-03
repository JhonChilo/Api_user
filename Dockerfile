FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Ejecutar el script de espera antes de iniciar Uvicorn
CMD ["sh", "-c", "python core/wait_for_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]