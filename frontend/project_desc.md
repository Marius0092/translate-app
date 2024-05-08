# Open Translate

Scrivere un applicazione che sia una sorta di clone di Google Translate / DeepL e che usi modelli 
open source per traduzione, riconoscimento vocale e sintesi vocale. Il progetto può essere eseguito su più fasi
per valutare il progresso.

## V0.1

Realizzare interfaccia grafica del traduttore con una casella di testo per scrivere, una per mostrare l'output,
dei menu per selezionare le lingue (possiamo cominciare con italiano <-> inglese) e un bottone per inviare la 
traduzione. La traduzione effettiva viene gestita dal back-end. Il front-end deve inviare una richiesta json con 
i seguenti campi:

- "text": contenente il testo da tradurre
- "source-lang": contenente il codice lingua di partenza in formato ll-PP dove ll è codice lingua ISO-639 e PP è il codice paese ISO-3166 (vedi https://www.fincher.org/Utilities/CountryLanguageList.shtml).
- "target-lang": contenente il codice lingua destinazione nello stesso formato indicato sopra.

La risposta json conterrà gli stessi campi di cui sopra, più un campo "translation" con il testo tradotto. In 
aggiunta bisognerà controllare la risposta http, il cui codice può essere 200 se la traduzione è stata effettuata
con successo, o 500 se qualcosa è andato storto. Mostrare un messaggio d'errore in caso di codice 500.

## V0.2

In aggiunta alle funzionalità di cui sopra, inviare una richiesta di traduzione ogni volta che l'utente ha finito 
di scrivere una parola (controllare per il carattere spazio o punto), e inoltre inviare una richiesta 1 secondo dopo che l'utente ha terminato di scrivere se il testo non termina con spazio o punto.
