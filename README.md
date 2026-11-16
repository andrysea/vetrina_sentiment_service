# Vetrinia Sentiment Analysis Service

## 1. Descrizione del progetto

Servizio REST sviluppato con **Python e FastAPI** per l'analisi del sentiment di recensioni per la sola lingua inglese.

Il servizio utilizza un modello di Machine Learning preaddestrato, basato su scikit-learn, per classificare le recensioni come:

- `positive`
- `negative`
- `neutral`

Il progetto ha l'obiettivo di rendere il modello disponibile attraverso API REST, verificarne il funzionamento mediante test automatici e predisporne il deployment e il monitoraggio.

**Tecnologie impiegate:** Python 3.13, FastAPI, scikit-learn, Pytest, Docker, Prometheus, Grafana e Jenkins.

## 2. Architettura

Il sistema è composto da tre servizi principali:

- **FastAPI:** espone il modello di Sentiment Analysis attraverso gli endpoint REST.
- **Prometheus:** raccoglie periodicamente le metriche di funzionamento del servizio.
- **Grafana:** si collega a Prometheus per visualizzare e analizzare le metriche.

I servizi vengono eseguiti in container Docker e gestiti tramite Docker Compose.

## 3. Prerequisiti

Per eseguire il progetto sono necessari:

- Docker Desktop installato e avviato.
- Docker Compose (incluso in Docker Desktop).
- Il repository del progetto contenente il modello `models/sentiment_analysis_model.pkl`.

Per eseguire i test direttamente sul computer sono necessari anche Python 3.13 e pip.

## 4. Prima installazione e avvio

### 4.1 Accedere al progetto

Aprire il terminale e posizionarsi nella directory principale del repository:

cd /percorso/del/progetto/vetrina_sentiment_service

### 4.2 Configurare le variabili d'ambiente

Creare il file `.env` nella directory principale.

Se è presente `.env.example`, copiarlo:

cp .env.example .env

Impostare nel file `.env` una password sicura per Grafana:

GRAFANA_ADMIN_PASSWORD=INSERIRE_PASSWORD_PERSONALE


### 4.3 Verificare Docker Compose

Assicurarsi che Docker Desktop sia avviato.

Eseguire:

- docker compose config --quiet


Il comando verifica la configurazione Compose. Se termina senza errori, si può procedere.

### 4.4 Costruire e avviare i servizi

- docker compose up -d --build

Il comando costruisce l'immagine del servizio FastAPI, scarica le immagini necessarie e avvia i container in background.

### 4.5 Verificare i container

- docker compose ps

I servizi `api`, `prometheus` e `grafana` devono risultare in esecuzione.

## 5. Avvii successivi

Dopo aver spento e riacceso il computer, aprire Docker Desktop e posizionarsi nella cartella del progetto.

Per avviare l'intero sistema:

- docker compose up -d

Per verificarne lo stato:

- docker compose ps


## 6. Utilizzo del servizio

### 6.1 FastAPI

Documentazione interattiva:

http://localhost:8000/docs

**POST /predict**

Esempio di richiesta:

{
  "review": "This product is amazing!"
}


Esempio di risposta:

{
  "sentiment": "positive",
  "confidence": 0.8249
}


Il valore di confidence rappresenta la probabilità stimata dal modello per la classe prevista.

Le richieste non valide restituiscono HTTP 422. Gli errori interni di predizione vengono gestiti con HTTP 500.

### 6.2 Prometheus

Interfaccia:

http://localhost:9090

Verificare lo stato della raccolta con la query PromQL:

- up{job="vetrinia-api"}

Il valore `1` indica che Prometheus sta raccogliendo correttamente le metriche.

### 6.3 Grafana

Interfaccia:

http://localhost:3000

Credenziali di accesso:

- Utente: `admin`
- Password: quella configurata nel file `.env`.

Il Data Source Prometheus viene configurato automaticamente attraverso i file di provisioning del repository.

## 7. Monitoraggio

L'endpoint **GET /metrics** espone le metriche utilizzate da Prometheus:

- `sentiment_prediction_errors_total`: numero di errori interni di predizione.
- `sentiment_request_duration_seconds`: distribuzione dei tempi di risposta HTTP.
- `process_cpu_seconds_total`: tempo CPU cumulativo del processo.
- `process_resident_memory_bytes`: memoria residente utilizzata dal processo.

Le dashboard Grafana permetteranno di visualizzare questi indicatori e individuare eventuali anomalie.

## 8. Esecuzione dei test automatici

Per eseguire i test direttamente sul computer, creare e attivare un ambiente virtuale Python:

- python3 -m venv .venv
- source .venv/bin/activate

Installare le dipendenze:

- python -m pip install -r requirements.txt

Eseguire la suite:

- python -m pytest tests/ -v


Il progetto include test unitari e di integrazione per la validazione, le predizioni, gli errori HTTP e le metriche.

**Ultima verifica locale completata: 20 test superati.**

## 9. Comandi Docker utili

Visualizzare lo stato dei container:

- docker compose ps

Visualizzare i log di tutti i servizi:

- docker compose logs

Seguire in tempo reale i log FastAPI:

- docker compose logs -f api

Visualizzare i log di Prometheus:

- docker compose logs prometheus

Visualizzare i log di Grafana:

- docker compose logs grafana

Ricostruire l'immagine e aggiornare i servizi dopo modifiche al codice:

- docker compose up -d --build

Arrestare e rimuovere i container gestiti da Compose:

- docker compose down

I volumi persistenti di Prometheus e Grafana vengono conservati dal normale comando `down`.


### 10. Dashboard Grafana

La dashboard **Vetrinia — Sentiment Analysis Monitoring** viene caricata automaticamente tramite provisioning e contiene quattro pannelli:

- Errori di predizione.
- Tempo di risposta P95.
- Utilizzo CPU del processo FastAPI.
- Memoria RAM del processo FastAPI.

La configurazione si trova nei seguenti file:

- `monitoring/grafana/dashboards/vetrina-dashboard.json`
- `monitoring/grafana/provisioning/dashboards/dashboard.yml`
- `monitoring/grafana/provisioning/datasources/prometheus.yml`

Per avviare l'infrastruttura:

- docker compose up -d


Aprire `http://localhost:3000` e accedere con le credenziali configurate nel file `.env`.

La dashboard è gestita tramite file: eventuali modifiche permanenti devono essere apportate alla configurazione versionata nel repository.

## Continuous Integration & Continuous Deployment

La pipeline Jenkins rileva automaticamente le modifiche
pubblicate su GitHub mediante Poll SCM ogni due minuti.

---
**Vetrinia S.p.A. — Sentiment Analysis Service**

Progetto DevOps e gestione del ciclo di vita del software.
