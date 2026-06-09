<p align="center">
  <h1 align="center">📖 Manuale Utente — Pitch Master</h1>
  <p align="center">Guida completa all'utilizzo di Pitch Master</p>
</p>

---

## Indice

1. [Introduzione](#introduzione)
2. [Installazione](#installazione)
3. [Configurazione](#configurazione)
4. [Avvio dell'Applicazione](#avvio-dellapplicazione)
5. [Panoramica dell'Interfaccia](#panoramica-dellinterfaccia)
6. [Modalita Costruisci](#modalita-costruisci)
7. [Modalita Audita](#modalita-audita)
8. [Confronto PEF](#confronto-pef)
9. [Cronologia](#cronologia)
10. [Analytics](#analytics)
11. [Template](#template)
12. [Lingue Supportate](#lingue-supportate)
13. [Esportazione](#esportazione)
14. [PEF-100 Spiegazione](#pef-100-spiegazione)
15. [FAQ](#faq)
16. [Risoluzione Problemi](#risoluzione-problemi)

---

## Introduzione

Pitch Master e un'applicazione web open source che aiuta founder e investitori a:

- **Founder:** Costruire pitch deck chiari, credibili e investibili
- **Investitori:** Audita pitch deck con il framework di scoring PEF-100

### Cosa fa Pitch Master?

| Funzionalita | Descrizione |
|--------------|-------------|
| **Build Mode** | Genera pitch completi da questionari guidati |
| **Audit Mode** | Analizza PDF di pitch deck con punteggi PEF-100 |
| **Confronto** | Confronta PEF-100 di piu deck affiancati |
| **Cronologia** | Salva e gestisci pitch passati |
| **Analytics** | Dashboard con grafici e trend PEF-100 |
| **Template** | 4 template predefiniti per diversi stadi |

> **Nota:** Pitch Master non decide se una startup e investibile. Aiuta a strutturare il pensiero su chiarezza e persuasione del pitch.

---

## Installazione

### Requisiti

- Python 3.11 o superiore
- Windows 10/11, Linux, o macOS
- Connessione internet (per LLM API)

### Windows (consigliato)

```bash
# 1. Clona il repository
git clone https://github.com/rthgit/PitchMaster.git
cd PitchMaster

# 2. Fai doppio clic su start.bat
#    - Crea automaticamente il virtual environment
#    - Installa le dipendenze
#    - Avvia l'applicazione
```

### Installazione Manuale

```bash
# 1. Clona il repository
git clone https://github.com/rthgit/PitchMaster.git
cd PitchMaster

# 2. Crea il virtual environment
python -m venv .venv

# 3. Attiva il virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Installa le dipendenze
pip install -r requirements.txt

# 5. Configura la chiave API
cp .env.example .env
# Modifica .env con la tua chiave API

# 6. Avvia l'applicazione
streamlit run app.py
```

L'app si apre su **http://localhost:8501**

---

## Configurazione

### File .env

Copia `.env.example` in `.env` e modificalo con la tua chiave API:

```env
# Scegli un provider
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
TEMPERATURE=0.3

# Imposta la chiave per il provider scelto
OPENAI_API_KEY=sk-...
```

### Provider Supportati

| Provider | Modelli Consigliati | Chiave API |
|----------|---------------------|------------|
| **OpenAI** | gpt-4o-mini, gpt-4o | `OPENAI_API_KEY` |
| **Anthropic** | claude-3-sonnet, claude-3-opus | `ANTHROPIC_API_KEY` |
| **Google** | gemini-1.5-flash, gemini-1.5-pro | `GOOGLE_API_KEY` |
| **Groq** | llama3-8b, mixtral-8x7b | `GROQ_API_KEY` |
| **OpenRouter** | Qualsiasi modello | `OPENROUTER_API_KEY` |

### Consigli sui Modelli

- **Per iniziare:** `gpt-4o-mini` (economico e veloce)
- **Per qualita:** `gpt-4o` o `claude-3-sonnet`
- **Per velocita:** `groq` con `llama3-8b`
- **Per budget:** `google` con `gemini-1.5-flash`

---

## Avvio dell'Applicazione

### Metodo 1: start.bat (consigliato)

```bash
# Fai doppio clic su start.bat
# L'app si apre su http://localhost:8501
```

### Metodo 2: Manuale

```bash
# Attiva il virtual environment
.venv\Scripts\activate

# Avvia Streamlit
streamlit run app.py
```

### Metodo 3: Da IDE

1. Apri la cartella PitchMaster in VS Code / PyCharm
2. Apri il terminale integrato
3. Esegui: `streamlit run app.py`

### Comandi BAT

| Comando | Azione |
|---------|--------|
| `start.bat` | Avvia l'applicazione |
| `stop.bat` | Ferma l'applicazione |
| `restart.bat` | Riavvia l'applicazione |

### Pulsanti UI

Nella sidebar trovi:

| Pulsante | Azione |
|----------|--------|
| 🚀 **Start Pitch Master** | Attiva l'app |
| ⏹ **Stop** | Disattiva l'app |
| 🔄 **Restart** | Riavvia l'app |

---

## Panoramica dell'Interfaccia

### Layout

```
┌─────────────────────────────────────────────────────┐
│  🎯 Pitch Master                          v0.1.0   │
├──────────────┬──────────────────────────────────────┤
│  Lingua:     │                                      │
│  [EN]     ▼  │         CONTENUTO PRINCIPALE         │
│              │                                      │
│  Modalita:   │                                      │
│  ○ Costruisci│                                      │
│  ○ Audita    │                                      │
│  ○ Confronto │                                      │
│  ○ Cronologia│                                      │
│  ○ Analytics │                                      │
│              │                                      │
│  Provider:   │                                      │
│  openai      │                                      │
│  Modello:    │                                      │
│  gpt-4o-mini │                                      │
│              │                                      │
│  ──────────  │                                      │
│  Disclaimer  │                                      │
└──────────────┴──────────────────────────────────────┘
```

### Sidebar

La sidebar contiene:

1. **Selettore Lingua** — Cambia la lingua dell'interfaccia
2. **Pulsanti Start/Stop** — Controlla l'applicazione
3. **Navigazione** — Seleziona la modalita
4. **Info Provider** — Mostra provider e modello attivi
5. **Disclaimer** — Avviso legale

### Area Principale

L'area principale cambia in base alla modalita selezionata.

---

## Modalita Costruisci

### Cos'e

Genera un pitch completo rispondendo a un questionario guidato.

### Come usarla

1. **Seleziona un template** (opzionale)
   - Seed SaaS
   - Series A B2C
   - Pre-Seed Deep Tech
   - Growth Marketplace
   - Oppure "Custom" per iniziare da zero

2. **Compila il questionario**

   | Campo | Descrizione | Obbligatorio |
   |-------|-------------|:------------:|
   | Nome Azienda | Il nome della tua startup | ✅ |
   | One-liner | Cosa fate in una frase | ✅ |
   | Problema | Il problema che risolvete | ✅ |
   | Soluzione | La vostra soluzione | ✅ |
   | Perche Ora | Timing, trend, regolamentazione | ❌ |
   | Mercato | TAM/SAM, tasso di crescita | ❌ |
   | Business Model | Prezzi, unit economics | ❌ |
   | Traction | Ricavi, utenti, pilot, crescita | ❌ |
   | Team | Founders, background, vantaggio | ❌ |
   | Richiesta | Quanto, per cosa | ❌ |

3. **Clicca "Genera Pitch"**

4. **Risultato include:**
   - Executive Summary (3-4 frasi)
   - Pitch Deck Outline (slide by slide)
   - Investor Narrative (300-400 parole)
   - Email Intro (50-80 parole)
   - PEF Self-Audit (auto-valutazione)

5. **Esporta** in MD, TXT, DOCX, o PDF

### Esempio di Output

```markdown
# Executive Summary
La Piattaforma AI per la Logistica riduce i costi del 30% per le PMI italiane.
Con 50 clienti paganti e $100K MRR, stiamo crescendo del 15% MoM.
Il team ha 20 anni di esperienza nel settore logistico.
Stiamo raccogliendo $2M per scalare a livello nazionale.

# Pitch Deck Outline
## Slide 1: Title
- Company: [Nome]
- One-liner: [Descrizione]
- Logo + Tagline

## Slide 2: Problem
- Il problema specifico
- Dati che quantificano il problema
- Chi soffre del problema
...
```

---

## Modalita Audita

### Cos'e

Analizza un PDF di pitch deck e fornisce:
- Punteggio PEF-100 automatico
- Analisi per livello
- Suggerimenti di miglioramento
- Audit qualitativo powered by LLM

### Come usarla

1. **Carica un PDF**
   - Trascina il file nell'area di upload
   - Oppure clicca "Carica PDF" e seleziona il file

2. **Visualizza i risultati automatici**
   - Numero di pagine e parole
   - Punteggio PEF-100 (0-100)
   - Scomposizione per livello (0-25 ciascuno)
   - Penalita (0-10 ciascuna)
   - Red flags individuati

3. **Esegui l'Audit Approfondito** (opzionale)
   - Clicca "Esegui Audit Approfondito"
   - LLM analizza il deck in dettaglio
   - Ricevi punteggi 0-5 per ogni dimensione
   - Suggerimenti concreti di miglioramento

4. **Esporta** l'audit in MD, TXT, DOCX, o PDF

### PEF-100 Score

| Punteggio | Significato |
|-----------|-------------|
| 80-100 | Eccellente — pitch molto persuasivo |
| 60-79 | Buono — pitch efficace con aree di miglioramento |
| 40-59 | Medio — pitch funzionale ma migliorabile |
| 20-39 | Debole — pitch necessita di revisioni significative |
| 0-19 | Critico — pitch richiede riscrittura completa |

### Layer PEF-100

| Layer | Domanda | Max |
|-------|---------|-----|
| **Attention** | Il deck cattura l'attenzione? | 25 |
| **Understanding** | Il messaggio e chiaro? | 25 |
| **Belief** | Le affermazioni sono credibili? | 25 |
| **Trust** | Il team e degno di fiducia? | 25 |
| **FOMO** | C'e urgenza di agire? | 25 |

### Red Flags

Il sistema rileva automaticamente:
- Affermazioni di rendimenti garantiti
- "Nessuna concorrenza"
- "Primo movers" senza evidenze
- Buzzword AI senza specifics
- Moltiplicatori irrealistici (10x, 100x)
- "Nessun rischio"

---

## Confronto PEF

### Cos'e

Confronta i punteggi PEF-100 di piu deck affiancati.

### Come usarlo

1. **Esegui prima alcuni audit** in Modalita Audita
   - Ogni audit viene salvato nella cronologia

2. **Vai alla sezione Confronto**
   - Seleziona i deck da confrontare (max 5)

3. **Visualizza:**
   - Tabella comparativa con punteggi
   - Grafici a barre per livello
   - Confronto diretto PEF-100

### Esempio

```
Deck A (72/100)     Deck B (58/100)     Deck C (45/100)
├─ Attention: 22    ├─ Attention: 18    ├─ Attention: 12
├─ Understanding:20 ├─ Understanding:15 ├─ Understanding:18
├─ Belief: 15       ├─ Belief: 12       ├─ Belief: 8
├─ Trust: 10        ├─ Trust: 8         ├─ Trust: 4
└─ FOMO: 5          └─ FOMO: 5          └─ FOMO: 3
```

---

## Cronologia

### Cos'e

Salva, carica, ed elimina pitch e audit passati.

### Come usarla

1. **Salvataggio automatico**
   - Ogni pitch generato viene salvato
   - Ogni audit eseguito viene salvato con punteggio PEF-100

2. **Visualizza la cronologia**
   - Vai alla sezione "Cronologia"
   - Vedi tutte le voci salvate
   - Filtra per modalita (Build/Audit)

3. **Gestisci le voci**
   - Espandi una voce per vedere i dettagli
   - Esporta in MD, TXT, DOCX, PDF
   - Elimina voci non necessarie

4. **Statistiche**
   - Totale pitch salvati
   - Media PEF-100
   - Numero audit vs build

---

## Analytics

### Cos'e

Dashboard con grafici e statistiche sui tuoi pitch.

### Cosa mostra

| Grafico | Descrizione |
|---------|-------------|
| **Distribuzione PEF-100** |istogramma dei punteggi |
| **Media Layer** | Punteggio medio per livello |
| **Attivita** | Timeline dei pitch creati |

### Come usarlo

1. **Esegui piu audit** per avere dati
2. **Vai alla sezione Analytics**
3. **Visualizza i grafici**
4. **Analizza i trend**

---

## Template

### Disponibili

| Template | Descrizione | Ideale per |
|----------|-------------|------------|
| **Seed SaaS** | B2B SaaS a seed stage | Startup SaaS pre-revenue |
| **Series A B2C** | Prodotto consumer con traction | Series A, consumer |
| **Pre-Seed Deep Tech** | Tech moat, ricerca | Deep tech, pre-prodotto |
| **Growth Marketplace** | Marketplace con network effects | Marketplace, growth |

### Come usarli

1. In Modalita Costruisci, seleziona un template
2. I campi vengono pre-compilati con esempi
3. Modifica con i tuoi dati reali
4. Genera il pitch

### Esempio Template Seed SaaS

```
Nome Azienda: [Nome]
One-liner: We help [customer] solve [problem] with [solution]
Problema: Businesses waste [X hours/$Y] on [manual process]
Soluzione: Our [platform/tool] automates [process] using [technology]
...
```

---

## Lingue Supportate

### Disponibili

| Lingua | Flag | Codice |
|--------|------|--------|
| English | 🇬🇧 | EN |
| Italiano | 🇮🇹 | IT |
| Portugues | 🇧🇷 | PT |
| Espanol | 🇪🇸 | ES |

### Come Cambiare

1. Nella sidebar, trova il selettore lingua
2. Seleziona la lingua desiderata
3. L'interfaccia si aggiorna immediatamente

### Cosa viene tradotto

- Tutte le etichette dell'interfaccia
- Bottoni, header, errori
- System prompts (l'LLM risponde nella lingua selezionata)
- Nomi dei livelli PEF-100
- Disclaimer

---

## Esportazione

### Formati Supportati

| Formato | Estensione | Uso |
|---------|------------|-----|
| **Markdown** | .md | Documentazione, GitHub |
| **TXT** | .txt | Testo semplice, email |
| **DOCX** | .docx | Word, documenti formali |
| **PDF** | .pdf | Stampa, presentazioni |

### Come Esportare

1. Dopo aver generato un pitch o audit
2. Clicca il pulsante del formato desiderato
3. Il file viene salvato nella cartella `outputs/`

### Dove vengono salvati

```
outputs/
├── pitch_NomeAzienda_20260609_143022.md
├── audit_deck_20260609_143522.pdf
└── ...
```

---

## PEF-100 Spiegazione

### Cos'e il PEF-100

Il PEF-100 (Persuasion Effectiveness Framework) e un sistema di scoring che valuta l'efficacia persuasiva dei pitch deck.

### Le 5 Dimensioni

#### 1. Attention (0-25)
- **Novelta:** Il deck presenta qualcosa di nuovo?
- **Rilevanza:** Il problema e rilevante per il lettore?
- **Energia:** Il deck trasmette entusiasmo?
- **Timing:** Il timing e convincente?

#### 2. Understanding (0-25)
- **Chiarita:** Il messaggio e facile da capire?
- **Compressione:** Il contenuto e conciso?
- **Struttura:** Il deck e ben organizzato?
- **Cognizione Visiva:** Il layout e efficace?

#### 3. Belief (0-25)
- **Prove:** Ci sono dati a supporto?
- **Traction:** Ci sono segnali di trazione?
- **Meccanismo:** Il "come funziona" e chiaro?
- **Logica di Mercato:** Il mercato ha senso?

#### 4. Trust (0-25)
- **Competenza:** Il team ha esperienza rilevante?
- **Autenticita:** Il messaggio e onesto?
- **Founder Fit:** Il founder e il giusto per questo problema?
- **Credibilita Leadership:** La leadership ha credibilita?

#### 5. FOMO (0-25)
- **Potenziale:** Il mercato e grande?
- **Momentum:** La crescita e in atto?
- **Scarsita:** C'e scarsita o urgenza?
- **Asimmetria:** Il rapporto rischio/rendimento e favorevole?

### Penalita

| Penalita | Max | Cosa misura |
|----------|-----|-------------|
| **Fatica Cognitiva** | 10 | Quanto sforzo mentale richiede il deck |
| **Rischio Percepito** | 10 | Red flags e indicatori di rischio |

### Calcolo Finale

```
PEF-100 = (Somma Livelli / 125) × 80 + ((20 - Penalita) / 20) × 20
```

Range: 0-100

---

## FAQ

### Devo pagare per usare Pitch Master?

No. Pitch Master e open source e gratuito. Paghi solo le chiamate API al provider LLM scelto.

### Qual provider scegliere?

- **Per iniziare:** OpenAI con gpt-4o-mini (economico)
- **Per qualita:** Anthropic con claude-3-sonnet
- **Per velocita:** Groq con llama3-8b
- **Per budget:** Google con gemini-1.5-flash

### I miei dati vengono salvati?

I pitch vengono salvati localmente nella cartella `outputs/history/`. Nessun dato viene inviato a server esterni (tranne le chiamate API al provider LLM).

### Posso usare Pitch Master offline?

No. Serve una connessione internet per le chiamate API al LLM. Il PEF-100 automatico funziona anche offline.

### Come cambio la lingua?

Nella sidebar, usa il selettore lingua in alto.

### Posso personalizzare i template?

Si. Seleziona "Custom" e compila i campi da zero. I template sono solo esempi.

### Come esporto in PDF?

Dopo aver generato un pitch o audit, clicca il pulsante "PDF" nelle opzioni di esportazione.

---

## Risoluzione Problemi

### "ImportError: cannot import name..."

**Soluzione:** Cancella la cartella `__pycache__` e riavvia.

```bash
# Windows
rmdir /s /q pitch_master\__pycache__

# Linux/Mac
rm -rf pitch_master/__pycache__
```

### "Missing API key..."

**Soluzione:** Controlla il file `.env` e assicurati che la chiave sia impostata correttamente.

### "Streamlit non parte"

**Soluzione:** Assicurati di avere il virtual environment attivo e le dipendenze installate.

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
### "PDF Error: Failed to extract text..."

**Soluzione:** Il PDF potrebbe essere protetto o scannerizzato. Prova con un altro PDF.

### "LLM call failed..."

**Soluzione:** Controlla:
1. La chiave API e valida
2. Hai credito/saldo sul provider
3. Il modello esiste
4. La connessione internet funziona

### L'app e lenta

**Soluzione:**
- Usa un modello piu veloce (groq, gemini-flash)
- Riduci la temperatura
- Usa un PDF piu corto

---

## Supporto

- **GitHub:** https://github.com/rthgit/PitchMaster
- **Issues:** https://github.com/rthgit/PitchMaster/issues

---

<p align="center">
  <sub>Fatto con ❤️ per founder e investitori</sub>
</p>
