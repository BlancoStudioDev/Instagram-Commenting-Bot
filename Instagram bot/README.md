# Instagram Reels Comment Bot - Documentazione

## Indice
1. [Introduzione](#introduzione)
2. [Requisiti di sistema](#requisiti-di-sistema)
3. [Installazione](#installazione)
4. [Utilizzo](#utilizzo)
   - [Interfaccia a riga di comando (CLI)](#interfaccia-a-riga-di-comando-cli)
   - [Interfaccia grafica (GUI)](#interfaccia-grafica-gui)
5. [Funzionalità](#funzionalità)
6. [Limitazioni e precauzioni](#limitazioni-e-precauzioni)
7. [Risoluzione dei problemi](#risoluzione-dei-problemi)
8. [FAQ](#faq)

## Introduzione

Instagram Reels Comment Bot è uno strumento automatizzato che consente di commentare i Reels di Instagram in modo automatico. Il bot può scorrere tra i Reels e inserire un commento predefinito per un numero specificato di Reels.

Questo bot è stato sviluppato utilizzando Python e Selenium per l'automazione del browser. È disponibile sia con un'interfaccia a riga di comando (CLI) che con un'interfaccia grafica (GUI), a seconda delle preferenze dell'utente e delle capacità del sistema.

## Requisiti di sistema

Per utilizzare Instagram Reels Comment Bot, è necessario disporre dei seguenti requisiti:

- Python 3.6 o versione successiva
- Google Chrome installato
- Connessione a Internet
- Account Instagram valido

Dipendenze Python:
- selenium
- webdriver-manager
- tkinter (solo per l'interfaccia grafica)

## Installazione

Segui questi passaggi per installare e configurare il bot:

1. **Clona o scarica il repository**

   ```bash
   git clone https://github.com/tuonome/instagram-reels-comment-bot.git
   cd instagram-reels-comment-bot
   ```

   In alternativa, puoi scaricare e decomprimere il file ZIP del progetto.

2. **Installa le dipendenze Python**

   ```bash
   pip install selenium webdriver-manager
   ```

   Se desideri utilizzare l'interfaccia grafica, installa anche tkinter:

   ```bash
   # Su Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Su Fedora
   sudo dnf install python3-tkinter
   
   # Su macOS (usando Homebrew)
   brew install python-tk
   
   # Su Windows, tkinter è generalmente incluso con l'installazione di Python
   ```

3. **Verifica l'installazione di Google Chrome**

   Assicurati che Google Chrome sia installato sul tuo sistema. Il bot utilizza Chrome per l'automazione.

4. **Rendi eseguibili gli script (solo per Linux/macOS)**

   ```bash
   chmod +x cli.py
   chmod +x gui.py
   ```

## Utilizzo

Il bot può essere utilizzato in due modi: tramite interfaccia a riga di comando (CLI) o tramite interfaccia grafica (GUI).

### Interfaccia a riga di comando (CLI)

L'interfaccia a riga di comando è il modo più semplice e universale per utilizzare il bot. Funziona su tutti i sistemi operativi e non richiede librerie grafiche aggiuntive.

Per visualizzare l'help e le opzioni disponibili:

```bash
python cli.py --help
```

Esempio di utilizzo base:

```bash
python cli.py
```

Questo comando avvierà il bot in modalità interattiva, chiedendo all'utente di inserire le credenziali di Instagram, il commento da pubblicare e il numero di Reels da commentare.

Esempio di utilizzo con parametri:

```bash
python cli.py --username tuousername --comment "Grande video! 👍" --num-reels 10 --headless
```

Questo comando avvierà il bot con i parametri specificati:
- Username: tuousername
- Commento: "Grande video! 👍"
- Numero di Reels da commentare: 10
- Modalità headless: attiva (il browser non sarà visibile)

La password verrà sempre richiesta in modo sicuro durante l'esecuzione, per evitare di memorizzarla in chiaro nella cronologia dei comandi.

### Interfaccia grafica (GUI)

L'interfaccia grafica offre un modo più intuitivo per utilizzare il bot, ma richiede l'installazione di tkinter.

Per avviare l'interfaccia grafica:

```bash
python gui.py
```

L'interfaccia grafica presenta i seguenti campi:
- **Username**: il tuo nome utente Instagram
- **Password**: la tua password Instagram (non verrà memorizzata)
- **Commento**: il testo che desideri pubblicare come commento
- **Numero di Reels**: il numero di Reels da commentare
- **Modalità headless**: se selezionata, il browser non sarà visibile durante l'esecuzione

Dopo aver compilato i campi, clicca su "Avvia Bot" per iniziare il processo di commento automatico.

## Funzionalità

Il bot offre le seguenti funzionalità:

1. **Login automatico su Instagram**
   - Gestione automatica dei popup di cookie e notifiche

2. **Navigazione alla sezione Reels**
   - Individuazione e accesso automatico alla sezione Reels

3. **Scorrimento tra i Reels**
   - Navigazione automatica tra i Reels utilizzando i tasti freccia

4. **Inserimento e invio di commenti**
   - Individuazione del pulsante di commento
   - Inserimento del testo del commento
   - Invio del commento

5. **Simulazione di comportamento umano**
   - Ritardi casuali tra le azioni
   - Digitazione simulata carattere per carattere

6. **Modalità headless**
   - Possibilità di eseguire il bot senza visualizzare il browser

## Limitazioni e precauzioni

Prima di utilizzare il bot, tieni presente le seguenti limitazioni e precauzioni:

1. **Limitazioni di Instagram**
   - Instagram ha restrizioni contro i bot e l'automazione
   - L'uso eccessivo di automazione può portare a blocchi temporanei o permanenti dell'account
   - Instagram impone limiti orari per azioni come commenti, like e follow

2. **Rischi per l'account**
   - L'utilizzo di bot è contrario ai termini di servizio di Instagram
   - L'account potrebbe essere soggetto a restrizioni o sospensione
   - Utilizza il bot a tuo rischio e pericolo

3. **Consigli per un uso sicuro**
   - Limita il numero di commenti a 10-15 per sessione
   - Attendi almeno 1-2 ore tra le sessioni
   - Varia il testo dei commenti per evitare di sembrare spam
   - Evita di utilizzare il bot 24/7

## Risoluzione dei problemi

Se riscontri problemi durante l'utilizzo del bot, prova le seguenti soluzioni:

1. **Il bot non riesce a effettuare il login**
   - Verifica che le credenziali siano corrette
   - Controlla se il tuo account richiede l'autenticazione a due fattori (non supportata)
   - Prova ad accedere manualmente a Instagram e verifica se ci sono captcha o verifiche di sicurezza

2. **Il bot non trova il pulsante di commento**
   - Instagram potrebbe aver modificato la struttura della pagina
   - Prova ad aggiornare il bot all'ultima versione
   - Segnala il problema aprendo una issue su GitHub

3. **Il browser si chiude inaspettatamente**
   - Verifica che Chrome sia installato correttamente
   - Aggiorna Chrome all'ultima versione
   - Controlla se ci sono errori nei log

4. **L'interfaccia grafica non si avvia**
   - Verifica che tkinter sia installato correttamente
   - Utilizza l'interfaccia a riga di comando come alternativa

## FAQ

**D: È legale utilizzare questo bot?**
R: L'automazione di Instagram è contraria ai termini di servizio della piattaforma. L'utilizzo di questo bot potrebbe comportare restrizioni o sospensione dell'account. Utilizzalo a tuo rischio e pericolo.

**D: Posso utilizzare il bot per più account Instagram?**
R: Sì, puoi utilizzare il bot per diversi account, ma è consigliabile non eseguirlo contemporaneamente per più account dallo stesso indirizzo IP.

**D: Il bot può commentare Reels specifici o di utenti specifici?**
R: Attualmente, il bot commenta i Reels che appaiono nel feed principale della sezione Reels. Non è possibile selezionare Reels specifici o di utenti specifici.

**D: Posso personalizzare il bot per altre azioni su Instagram?**
R: Il codice è open source e può essere modificato per supportare altre azioni. Tuttavia, ricorda che l'automazione eccessiva aumenta il rischio di rilevamento e blocco dell'account.

**D: Come posso contribuire al progetto?**
R: Puoi contribuire aprendo issue, suggerendo miglioramenti o inviando pull request su GitHub.
