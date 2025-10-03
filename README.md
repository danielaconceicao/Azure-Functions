🤖 Funzioni di Utilità su Azure (Azure Utility Functions)</br>
Ciao! Benvenuto in questo set di Azure Functions creato per eseguire diverse utili operazioni di elaborazione dati e multimediale. 

  ```
      (  )   (   )  (   )
       ) (   )  (    ) (
      (_______(___)___(___)
    /|   AZURE FUNCTIONS  |\
   | | ------------------ | |
   | | ------------------ | |
   | | ------------------ | |
   |_|____________________|_|
    ( ) ( )  ( ) ( ) ( ) ( )
   /________________________\
```

🛠️ Funzionalità Implementate </br>
Questo progetto è un hub per quattro microservizi distinti, ognuno accessibile tramite un endpoint HTTP:

1. **Calcolo del Fattoriale (Vectorial)**  
Questa funzione calcola il fattoriale di un numero intero dato. È un utile strumento matematico accessibile direttamente tramite l'URL.

Endpoint: /api/factorial/{number}

Metodo: **GET** 

Esempio di Richiesta: GET /api/factorial/5

* **Risposta di Successo (200):**

```O fatorial de 5 é 120```

2. **Conteggio dei Token (Token Counter)**</br>
Utilizza la libreria tiktoken per contare il numero di token presenti in una stringa di testo, basandosi sul modello gpt-3.5-turbo. 

Endpoint: /api/count_tokens

Metodo: **POST**

* **Corpo della Richiesta (JSON):**
```JSON

{
  "text": "Questo è un testo di prova per contare i token."
}
```
* **Risposta di Successo (200):**

```JSON
{
  "tokens": 12
}
```
3. **Conversione Immagine (Bianco e Nero)**</br>
Riceve una stringa base64 di un'immagine e la converte in bianco e nero (scala di grigi) utilizzando la libreria Pillow. L'immagine convertita viene restituita come una nuova stringa base64.

Endpoint: /api/convert_image

Metodo: **POST**

* **Corpo della Richiesta (JSON):**

```JSON

{
  "image": "iVBORw0KGgoAAAANSUhE..." // Stringa base64 dell'immagine a colori
}
```
* **Risposta di Successo (200):**

```JSON
{
  "image_bw": "iVBORw0KGgoAAAANSUhE..." // Nuova stringa base64 in bianco e nero
}
```

4. **Trascrizione Audio (Audio Transcription)**</br>
Sfrutta il servizio Azure Cognitive Services Speech per trascrivere un file audio. La funzione accetta dati audio codificati in base64, li salva temporaneamente e utilizza l'SDK per ottenere la trascrizione del parlato in testo.

Endpoint: /api/transcribe

Metodo: **POST**

* **Corpo della Richiesta (JSON):**

```JSON
{
  "audio": "aHR0cHM6Ly93d3cueW91..." // Stringa base64 del file audio (.wav consigliato)
}
```
* **Risposta di Successo (200):**
```JSON
{
  "transcription": "Il testo trascritto dal tuo file audio."
}
```

⚙️ Configurazione del Progetto
Per far funzionare il servizio di trascrizione audio, è necessario configurare le tue credenziali di Azure Cognitive Services.

Esporta in Fogli
Dipendenze
Il progetto richiede le seguenti librerie Python:

```Bash

azure-functions
python-dotenv
tiktoken
Pillow
azure-cognitiveservices-speech
Puoi installarle tutte con:
```
```Bash

pip install -r requirements.txt
```
