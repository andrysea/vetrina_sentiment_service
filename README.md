
# Vetrinia Sentiment Analysis Service

## 1. Descrizione del progetto

Servizio REST sviluppato con **Python e FastAPI** per l'analisi del sentiment di recensioni per la sola lingua inglese. Il servizio utilizza un modello di Machine Learning preaddestrato, basato su scikit-learn.

Lo schema di risposta supporta le seguenti classi:

- `positive`
- `negative`
- `neutral`

I test effettuati sul modello reale verificano le classificazioni `positive` e `negative`.
Il progetto ha l'obiettivo di rendere il modello disponibile attraverso API REST, verificarne il funzionamento mediante test automatici e automatizzarne il deployment e il monitoraggio.

**Tecnologie impiegate:** Python 3.13, FastAPI, scikit-learn, Pytest, Docker, Docker Compose, Prometheus, Grafana, Jenkins e GitHub.

## 2. Architettura

Il sistema è composto da tre servizi principali:

- **FastAPI:** espone il modello di Sentiment Analysis attraverso gli endpoint REST.
- **Prometheus:** raccoglie periodicamente le metriche di funzionamento del servizio.
- **Grafana:** si collega a Prometheus per visualizzare e analizzare le metriche.

I servizi vengono eseguiti in container Docker e gestiti tramite Docker Compose.

L'infrastruttura comprende inoltre:

- **GitHub:** gestisce il versionamento del codice sorgente.
- **Jenkins:** automatizza i test, la build e il deployment del servizio.
- **Gmail SMTP:** permette l'invio delle notifiche relative all'esito della pipeline CI/CD.

## 3. Prerequisiti

Per eseguire il progetto sono necessari:

- Docker Desktop installato e avviato.
- Docker Compose (incluso in Docker Desktop).
- Git.
- Il repository del progetto contenente il modello `models/sentiment_analysis_model.pkl`.

Per eseguire i test direttamente sul computer sono necessari anche Python 3.13 e pip.
Per utilizzare la pipeline CI/CD sono inoltre necessari:

- Jenkins.
- Un ambiente Java compatibile con Jenkins.
- Accesso al repository GitHub.
- Plugin Pipeline, Git e Email Extension.
- Un account SMTP per l'invio delle notifiche.

## 4. Prima installazione e avvio

### 4.1 Accedere al progetto

Clonare il repository:

```bash
git clone https://github.com/andrysea/vetrina_sentiment_service.git
```

Posizionarsi nella directory principale del repository:

```bash
cd vetrina_sentiment_service
```

### 4.2 Configurare le variabili d'ambiente

Creare il file `.env` nella directory principale copiando il file di esempio:

```bash
cp .env.example .env
```

Impostare nel file `.env` una password sicura per Grafana:

```env
GRAFANA_ADMIN_PASSWORD=INSERIRE_PASSWORD_PERSONALE
```

Il file `.env` è escluso dal versionamento Git per evitare la pubblicazione di informazioni riservate.

### 4.3 Verificare Docker Compose

Assicurarsi che Docker Desktop sia avviato.

Eseguire:

```bash
docker compose config --quiet
```

Il comando verifica la configurazione Compose. Se termina senza errori, si può procedere.

### 4.4 Costruire e avviare i servizi

```bash
docker compose up -d --build
```

Il comando costruisce l'immagine del servizio FastAPI, scarica le immagini necessarie e avvia i container in background.

### 4.5 Verificare i container

```bash
docker compose ps
```

I servizi `api`, `prometheus` e `grafana` devono risultare in esecuzione.

## 5. Avvii successivi

Dopo aver spento e riacceso il computer, aprire Docker Desktop e posizionarsi nella cartella del progetto.
Se i container sono già presenti ma risultano arrestati:

```bash
docker compose start
```

Per verificarne lo stato:

```bash
docker compose ps
```

Se si utilizza la pipeline CI/CD, assicurarsi che anche Jenkins sia in esecuzione.
L'utilizzo di `docker compose start` consente di riavviare i container esistenti senza ricrearli con l'immagine predefinita.
Se i container sono stati rimossi, è possibile avviare nuovamente il sistema specificando l'immagine desiderata.

Esempio:

```bash
VETRINIA_IMAGE=vetrinia-sentiment:ci-14 docker compose up -d --no-build
```

Il tag `ci-14` deve essere sostituito con quello dell'ultima immagine valida disponibile.

## 6. Utilizzo del servizio

### 6.1 FastAPI

Documentazione interattiva:

http://localhost:8000/docs

**POST /predict**

Esempio di richiesta:

```json
{
  "review": "This product is amazing!"
}
```

Esempio di risposta:

```json
{
  "sentiment": "positive",
  "confidence": 0.8249072107192307
}
```

È possibile effettuare una richiesta direttamente dal terminale:

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"review":"This product is amazing!"}'
```

Il valore di confidence rappresenta la probabilità stimata dal modello per la classe prevista.
Le richieste non valide restituiscono HTTP 422. Gli errori interni di predizione vengono gestiti con HTTP 500.

**GET /metrics**

L'endpoint espone le metriche del servizio nel formato utilizzato da Prometheus.

http://localhost:8000/metrics

### 6.2 Prometheus

Interfaccia:

http://localhost:9090

Stato dei target:

http://localhost:9090/targets

Verificare lo stato della raccolta con la query PromQL:

```promql
up{job="vetrinia-api"}
```

Il valore `1` indica che Prometheus sta raccogliendo correttamente le metriche.

### 6.3 Grafana

Interfaccia:

http://localhost:3000

Credenziali di accesso iniziali:

- Utente: `admin`
- Password: quella configurata nel file `.env`.

Il Data Source Prometheus viene configurato automaticamente attraverso i file di provisioning del repository.

## 7. Monitoraggio

L'endpoint **GET /metrics** espone le metriche utilizzate da Prometheus:

- `sentiment_prediction_errors_total`: numero di errori interni di predizione.
- `sentiment_request_duration_seconds`: distribuzione dei tempi di risposta HTTP.
- `process_cpu_seconds_total`: tempo CPU cumulativo del processo.
- `process_resident_memory_bytes`: memoria residente utilizzata dal processo.

Prometheus raccoglie le metriche del servizio ogni 15 secondi.
Le dashboard Grafana permettono di visualizzare questi indicatori e individuare eventuali anomalie.

### 7.1 Simulazione del traffico

Per verificare il monitoraggio è possibile generare richieste verso il servizio FastAPI:

```bash
for i in {1..100}; do
  curl -s -X POST http://localhost:8000/predict \
    -H 'Content-Type: application/json' \
    -d '{"review":"This product is amazing!"}' > /dev/null
  sleep 0.2
done
```

Questo comando permette di verificare l'aggiornamento delle metriche in Grafana simulando 100 richieste di predizione.

## 8. Esecuzione dei test automatici

Per eseguire i test direttamente sul computer, creare e attivare un ambiente virtuale Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Assicurarsi di utilizzare Python 3.13.

Installare le dipendenze:

```bash
python -m pip install -r requirements.txt
```

Eseguire la suite:

```bash
python -m pytest tests/ -v
```

Il progetto include test unitari e di integrazione per la validazione, le predizioni, gli errori HTTP e le metriche.

### 8.1 Test unitari

I test unitari verificano il comportamento dei singoli componenti dell'applicazione, tra cui:

- Validazione delle recensioni.
- Validazione delle risposte.
- Gestione dei valori di confidence.
- Funzionamento del servizio di predizione.

### 8.2 Test di integrazione

I test di integrazione verificano:

- Predizioni effettuate utilizzando il modello reale.
- Funzionamento dell'endpoint `/predict`.
- Gestione delle richieste non valide.
- Gestione degli errori interni.
- Funzionamento dell'endpoint `/metrics`.
- Aggiornamento del contatore degli errori di predizione.

**Ultima verifica completata: 20 test superati, di cui 11 unitari e 9 di integrazione.**

I test vengono inoltre eseguiti automaticamente da Jenkins in un container Python 3.13 dedicato.

## 9. Comandi Docker utili

Visualizzare lo stato dei container:

```bash
docker compose ps
```

Visualizzare i log di tutti i servizi:

```bash
docker compose logs
```

Seguire in tempo reale i log FastAPI:

```bash
docker compose logs -f api
```

Visualizzare i log di Prometheus:

```bash
docker compose logs prometheus
```

Visualizzare i log di Grafana:

```bash
docker compose logs grafana
```

Visualizzare le immagini Docker del progetto:

```bash
docker images vetrinia-sentiment
```

Verificare l'immagine utilizzata dal container FastAPI:

```bash
docker inspect vetrina_sentiment_service-api-1 \
  --format '{{.Config.Image}}'
```

Ricostruire l'immagine e aggiornare i servizi manualmente:

```bash
docker compose up -d --build
```

Quest'ultimo comando è destinato allo sviluppo locale. Quando si utilizza Jenkins, è preferibile lasciare alla pipeline la gestione della build e del deployment.

Arrestare i container senza rimuoverli:

```bash
docker compose stop
```

Arrestare e rimuovere i container gestiti da Compose:

```bash
docker compose down
```

I volumi persistenti di Prometheus e Grafana vengono conservati dal normale comando `down`.

## 10. Dashboard Grafana

La dashboard **Vetrinia — Sentiment Analysis Monitoring** viene caricata automaticamente tramite provisioning e contiene quattro pannelli:

- Errori di predizione.
- Tempo di risposta P95.
- Utilizzo CPU del processo FastAPI.
- Memoria RAM del processo FastAPI.

La configurazione si trova nei seguenti file:

- `monitoring/grafana/dashboards/vetrina-dashboard.json`
- `monitoring/grafana/provisioning/dashboards/dashboard.yml`
- `monitoring/grafana/provisioning/datasources/prometheus.yml`

Aprire http://localhost:3000 e accedere con le credenziali configurate nel file `.env`, se non modificate successivamente.

La dashboard è gestita tramite file: eventuali modifiche permanenti devono essere apportate alla configurazione versionata nel repository.

### 10.1 Interpretazione delle metriche

- **Errori di predizione:** numero di errori interni registrati dall'avvio del processo.
- **Tempo di risposta P95:** tempo entro il quale viene completato circa il 95% delle richieste considerate.
- **Utilizzo CPU:** percentuale di utilizzo della CPU da parte del processo FastAPI, rispetto alla capacità di un core.
- **Utilizzo RAM:** quantità di memoria residente occupata dal processo FastAPI.

## 11. Continuous Integration & Continuous Deployment

La pipeline Jenkins rileva automaticamente le modifiche pubblicate su GitHub mediante Poll SCM ogni due minuti. La configurazione della pipeline è definita nel file `Jenkinsfile`, versionato nella directory principale del repository.

### 11.1 Installazione e avvio di Jenkins

Nell'ambiente macOS utilizzato per lo sviluppo, Jenkins è stato installato tramite Homebrew:

```bash
brew install jenkins-lts
```

Avviare Jenkins:

```bash
brew services start jenkins-lts
```

Interfaccia:

http://localhost:8080

Durante la configurazione iniziale, installare i plugin suggeriti e verificare la disponibilità del plugin Email Extension.

### 11.2 Configurazione della pipeline

Creare un nuovo progetto Jenkins di tipo Pipeline con le seguenti impostazioni:

- **Nome:** `vetrinia-sentiment-ci-cd`
- **Definition:** Pipeline script from SCM
- **SCM:** Git
- **Repository URL:** https://github.com/andrysea/vetrina_sentiment_service.git
- **Branch:** `*/main`
- **Script Path:** `Jenkinsfile`

Avviare manualmente la prima build per inizializzare la pipeline e il trigger automatico.

Il Jenkinsfile contiene la seguente configurazione:

```groovy
triggers {
    pollSCM('H/2 * * * *')
}
```

Jenkins controlla periodicamente il repository e avvia automaticamente la pipeline quando rileva nuove modifiche.

### 11.3 Fasi della pipeline

La pipeline è composta dalle seguenti fasi:

1. **Checkout:** recupera il codice sorgente da GitHub.
2. **Verifica ambiente:** verifica la disponibilità di Git, Python e Docker.
3. **Test automatici:** esegue i test unitari e di integrazione.
4. **Build Docker:** costruisce e verifica l'immagine Docker del servizio.
5. **Deploy Docker:** distribuisce la nuova immagine attraverso Docker Compose.
6. **Post Actions:** invia una notifica e-mail relativa all'esito della pipeline.

Il deployment viene eseguito soltanto se le fasi precedenti sono state completate correttamente.

### 11.4 Versionamento delle immagini Docker

Ogni immagine costruita dalla pipeline viene identificata utilizzando il numero della build Jenkins.

Esempi:

- `vetrinia-sentiment:ci-10`
- `vetrinia-sentiment:ci-13`
- `vetrinia-sentiment:ci-14`

Il file `compose.yaml` utilizza la seguente configurazione:

```yaml
image: ${VETRINIA_IMAGE:-vetrinia-sentiment:1.0}
```

La variabile `VETRINIA_IMAGE` viene impostata dinamicamente da Jenkins durante il deployment.
In assenza della variabile viene utilizzata l'immagine predefinita `vetrinia-sentiment:1.0`.
Questo meccanismo garantisce che la pipeline distribuisca l'immagine associata alla build corrente.

### 11.5 Deployment automatico

Il deployment viene effettuato in un ambiente di staging locale gestito tramite Docker Compose.
Jenkins ricrea esclusivamente il container FastAPI, senza ricreare i container Prometheus e Grafana.

Successivamente vengono eseguiti:

- Un controllo della disponibilità dell'endpoint `/metrics`.
- Uno smoke test sull'endpoint `/predict`.
- Una verifica del risultato della predizione.

Se il servizio non risulta disponibile entro il numero massimo di tentativi oppure lo smoke test fallisce, la pipeline termina con stato `FAILURE`.

Nell'ambiente utilizzato per lo sviluppo, il Jenkinsfile accede al file `.env` attraverso il percorso:

```text
$HOME/Desktop/vetrina_sentiment_service/.env
```

Se il progetto viene installato in una posizione differente, è necessario adattare tale percorso nel Jenkinsfile.

### 11.6 Configurazione delle notifiche e-mail

Le notifiche vengono gestite tramite il plugin Email Extension di Jenkins.

Accedere a:

```text
Gestisci Jenkins > System > Extended E-mail Notification
```

Configurare:

- **SMTP server:** `smtp.gmail.com`
- **SMTP Port:** `587`
- **Use TLS:** abilitato.
- **Use SSL:** disabilitato.
- **Use OAuth 2.0:** disabilitato.
- **Default Recipients:** indirizzo e-mail del destinatario.

Configurare inoltre l'indirizzo e-mail dell'amministratore di sistema utilizzando l'indirizzo del mittente.

Per l'autenticazione SMTP tramite Gmail è stata utilizzata una password per le app generata dall'account Google con verifica in due passaggi.

La credenziale viene salvata in Jenkins utilizzando:

- **Kind:** Username with password
- **Username:** indirizzo Gmail.
- **Password:** password per le app di Google.
- **ID:** `gmail-smtp`

Selezionare le credenziali nella configurazione SMTP.

Nessuna password SMTP viene inserita nel Jenkinsfile o pubblicata nel repository.

### 11.7 Notifiche di successo e fallimento

Al termine della pipeline, Jenkins invia automaticamente una notifica e-mail contenente:

- Nome del progetto.
- Numero della build.
- Stato della pipeline.
- Collegamento ai dettagli dell'esecuzione.

Sono previste due tipologie di notifiche:

- **SUCCESS:** pipeline completata correttamente.
- **FAILURE:** errore durante l'esecuzione della pipeline.

Le notifiche vengono implementate attraverso il blocco `post` del Jenkinsfile e la funzione `emailext()`.

### 11.8 Verifica della pipeline CI/CD

Sono stati verificati due scenari.

**Scenario 1 — Esecuzione corretta**

- Rilevamento automatico delle modifiche.
- Recupero del codice da GitHub.
- Superamento dei 20 test automatici.
- Creazione dell'immagine Docker.
- Deployment del servizio.
- Superamento dello smoke test.
- Ricezione della notifica e-mail di successo.

**Scenario 2 — Fallimento simulato**

È stato aggiunto temporaneamente un test destinato a fallire per verificare il comportamento della pipeline.

Risultato:

- 20 test superati.
- 1 test fallito intenzionalmente.
- Build Docker non eseguita.
- Deployment non eseguito.
- Ricezione della notifica e-mail di fallimento.

Il test temporaneo è stato successivamente rimosso e la pipeline è stata ripristinata correttamente.

## 12. Sicurezza

Il progetto adotta le seguenti misure di sicurezza:

- Esclusione del file `.env` dal repository Git.
- Gestione delle credenziali SMTP mediante Jenkins Credentials.
- Esecuzione del servizio FastAPI nel container con un utente non root.
- Validazione delle richieste tramite Pydantic.
- Gestione degli errori interni senza esporre dettagli tecnici al client.
- Versionamento delle dipendenze Python.
- Accesso locale alle porte dei servizi.
- Caricamento di un modello pickle proveniente da una fonte affidabile.

## 13. Risoluzione dei problemi

### 13.1 FastAPI non disponibile

Verificare lo stato dei container:

```bash
docker compose ps
```

Consultare i log:

```bash
docker compose logs api
```

### 13.2 Prometheus non raccoglie le metriche

Verificare lo stato del target:

http://localhost:9090/targets

Controllare che FastAPI sia disponibile e che l'endpoint `/metrics` risponda correttamente.

Consultare i log:

```bash
docker compose logs prometheus
```

### 13.3 Grafana non visualizza le metriche

Verificare:

- Che Prometheus sia in esecuzione.
- Che il target `vetrinia-api` risulti UP.
- Che il Data Source Prometheus sia configurato correttamente.
- Che l'intervallo temporale selezionato contenga dati.
- Che siano state effettuate richieste verso FastAPI.

### 13.4 Jenkins non avvia automaticamente la pipeline

Verificare:

- Che Jenkins sia in esecuzione.
- Che la prima build sia stata avviata.
- Che il repository GitHub sia raggiungibile.
- Che le modifiche siano state pubblicate sul branch `main`.
- Che il trigger Poll SCM sia configurato.

### 13.5 Mancata ricezione delle notifiche

Verificare:

- La configurazione del server SMTP.
- La correttezza dell'indirizzo e-mail.
- La validità della password per le app.
- La credenziale selezionata in Jenkins.
- L'abilitazione del protocollo TLS.
- Il contenuto del Console Output della build.

### 13.6 Versione Docker non corretta

Verificare l'immagine distribuita:

```bash
docker inspect vetrina_sentiment_service-api-1 \
  --format '{{.Config.Image}}'
```

Controllare che il tag corrisponda alla build Jenkins distribuita.

Evitare di ricreare manualmente il container senza valorizzare `VETRINIA_IMAGE`, poiché verrebbe utilizzata l'immagine predefinita.

## 14. Risultati e conclusioni

Il progetto implementa un sistema integrato per la gestione del ciclo di vita di un servizio di Machine Learning.

Sono state realizzate le seguenti funzionalità:

- Esposizione del modello tramite API REST.
- Containerizzazione del servizio.
- Test unitari e di integrazione.
- Versionamento del codice sorgente.
- Pipeline CI/CD automatizzata.
- Versionamento delle immagini Docker.
- Deployment automatico.
- Notifiche e-mail di successo / fallimento.
- Monitoraggio tramite Prometheus.
- Visualizzazione delle metriche tramite Grafana.

---

**Vetrinia S.p.A. — Sentiment Analysis Service**
Progetto DevOps e gestione del ciclo di vita del software.
