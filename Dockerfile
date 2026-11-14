
# 1. Immagine base Python
FROM python:3.13-slim

# 2. Impostazioni Python, il primo evita la generazione dei file .pyc e il secondo rende disponibili subito i log di python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directory di lavoro
WORKDIR /app

# 4. Copia delle dipendenze
COPY requirements.txt .

# 5. Installazione delle dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia del codice e del modello ML
COPY app/ ./app/
COPY models/ ./models/

# 7. Creazione di un utente non privilegiato
RUN useradd --create-home --uid 10001 appuser
USER appuser

# 7.1 Copia dei file assegnandoli all'utente appuser
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser models/ ./models/

# 7.2 Esecuzione del servizio come appuser
USER appuser

# 8. Porta utilizzata dal servizio
EXPOSE 8000

# 9. Avvio di FastAPI tramite Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
