# OrientaStudentBot - Chatbot per l'Orientamento degli Studenti

## Introduzione

OrientaStudentBot è un chatbot sviluppato con il framework Rasa, progettato per assistere gli studenti durante gli open day dell'Università Politecnica delle Marche. Il chatbot fornisce informazioni su workshop, visite ai laboratori, OFA e orientamento all'interno degli edifici universitari. Integrato con Telegram, **OrientaStudentBot** offre un'interfaccia semplice e intuitiva, accessibile direttamente da smartphone.

## Architettura del Progetto

### Rasa e Componenti Principali

Il progetto si basa su Rasa, una piattaforma potente per la comprensione del linguaggio naturale (NLU) e la gestione del dialogo (Core). Le componenti principali includono:
- **NLU**: Responsabile della comprensione degli intenti degli utenti e dell'estrazione delle entità.
- **Core**: Gestisce il flusso della conversazione, determinando le azioni da eseguire in risposta agli input degli utenti.
- **File di Configurazione**: `domain.yml`, `nlu.yml`, `stories.yml`, `rules.yml`, `credentials.yml`, `endpoints.yml`, che definiscono il comportamento complessivo del chatbot.

### Dataset

Un dataset fittizio è stato creato per simulare le interazioni reali degli studenti. Il dataset è composto da tre file CSV:
- **`aule.csv`**: Contiene informazioni sulle aule dell'università.
- **`lab_tours.csv`**: Include i dettagli sui tour dei laboratori.
- **`workshops.csv`**: Fornisce informazioni sui workshop offerti.

### Funzionalità del Chatbot

OrientaStudentBot offre diverse funzionalità:
- **Visualizzare informazioni su un workshop**: Questa funzionalità consente agli utenti di ottenere informazioni dettagliate su un workshop specifico. Il chatbot risponde alle richieste degli utenti fornendo dati come la data, l'orario, la location e il corso di studi associato.
- **Visualizzare i workshop per corso di studio**: In questa funzionalità, il chatbot permette agli utenti di filtrare i workshop disponibili in base al loro corso di studi. Il chatbot chiede all'utente di selezionare il corso di studi di interesse tramite un elenco di opzioni interattive (bottoni). Una volta selezionato il corso di studi, l'utente riceve una lista dei workshop disponibili per il corso di studi scelto, permettendo una ricerca mirata e personalizzata.
- **Visualizzare i tour dei laboratori**: Questa funzionalità consente agli utenti di esplorare i tour dei laboratori offerti dall'università.
- **Visualizzare informazioni sui tour dei laboratori**: Questa opzione consente agli utenti di ottenere informazioni dettagliate su un singolo tour dei laboratori. L'utente può specificare il nome del tour desiderato, e il chatbot risponderà con tutti i dettagli pertinenti.
- **Visualizzare informazioni sulle aule**: Il chatbot offre la possibilità di ottenere informazioni dettagliate sulle aule dell'università, inclusi il nome dell'aula, l'edificio in cui si trova, la quota, le indicazioni specifiche e un link alla planimetria.
- **Visualizzare informazioni sulle quote**: Questa funzionalità permette agli utenti di ottenere un link alla planimetria di una specifica quota (livello) all'interno di un edificio.
- **Visualizzare informazioni sugli OFA**: OrientaStudentBot è in grado di fornire informazioni sugli Obblighi Formativi Aggiuntivi (OFA), che sono spesso fonte di dubbi tra gli studenti. Il chatbot risponde alle domande degli utenti riguardanti cosa sono gli OFA, le date dei test di ingresso e le conseguenze di non superare questi test.
- **Prenotare un workshop**: OrientaStudentBot offre una funzionalità di prenotazione per i workshop. L'utente dovrà compilare un form con le diverse informazioni necessarie al bot e, se i dati inseriti sono corretti, verrà inviata un'email di conferma prenotazione.

### Integrazione con Telegram

Il chatbot è stato integrato con Telegram per migliorare l'accessibilità. Utilizzando ngrok, il server locale del chatbot è stato esposto tramite un endpoint pubblico. La configurazione necessaria per il deploy su Telegram è stata implementata nel file `credentials.yml`.

### Testing

Il chatbot è stato sottoposto a test approfonditi per simulare diverse interazioni, comprese quelle con input errati, al fine di garantire un'esperienza utente robusta e affidabile.
