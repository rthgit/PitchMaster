<p align="center">
  <h1 align="center">🎯 Pitch Master</h1>
  <p align="center">Open-source fundraising copilot for founders and investors</p>
  <p align="center">
    <a href="#quick-start">Quick Start</a> •
    <a href="#features">Features</a> •
    <a href="#user-manual">Manual</a> •
    <a href="#api-providers">Providers</a> •
    <a href="#license">License</a>
  </p>
</p>

---

Pitch Master is a local web app that helps founders build clear, credible pitch decks and investors audit them with the PEF-100 scoring framework.

> **Disclaimer:** This is a heuristic v0.1 score, not investment advice. Pitch Master does not decide whether a company is investable.

---

## Quick Start

### Windows (recommended)

```bash
# Clone the repo
git clone https://github.com/rthgit/PitchMaster.git
cd PitchMaster

# Double-click start.bat — it does everything automatically
start.bat
```

### Manual Installation

```bash
# Clone
git clone https://github.com/rthgit/PitchMaster.git
cd PitchMaster

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env with your API key

# Run
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## Configuration

Edit `.env` with your API key:

```env
# Choose one provider
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
TEMPERATURE=0.3

# Set the key for your provider
OPENAI_API_KEY=sk-...
```

### Supported Providers

| Provider | Models | Key Variable |
|----------|--------|--------------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-3.5-turbo | `OPENAI_API_KEY` |
| Anthropic | claude-3-opus, claude-3-sonnet | `ANTHROPIC_API_KEY` |
| Google | gemini-1.5-pro, gemini-1.5-flash | `GOOGLE_API_KEY` |
| Groq | llama3-8b, mixtral-8x7b | `GROQ_API_KEY` |
| OpenRouter | Any model | `OPENROUTER_API_KEY` |

---

## Features

### 🏗️ Build Mode
Answer a guided questionnaire, get a complete pitch:
- Executive Summary
- Pitch Deck Outline (slide by slide)
- Investor Narrative
- Email Intro (ready to copy)
- PEF Self-Audit

### 🔍 Audit Mode
Upload a PDF pitch deck, get:
- Automatic PEF-100 score (0-100)
- Layer breakdown (Attention, Understanding, Belief, Trust, FOMO)
- Penalty analysis (Cognitive Friction, Perceived Risk)
- Red flag detection
- LLM-powered qualitative audit with improvement suggestions

### 📊 Compare
Side-by-side PEF-100 comparison of multiple decks with bar charts.

### 📁 History
Save, load, delete, and export past pitches. Stats overview.

### 📈 Analytics
PEF-100 score distribution, average layer scores, activity timeline.

### 📑 Templates
4 pre-built pitch templates:
- **Seed SaaS** — B2B SaaS at seed stage
- **Series A B2C** — Consumer product with traction
- **Pre-Seed Deep Tech** — Technical moat, research-heavy
- **Growth Marketplace** — Marketplace with network effects

### 🌍 Multi-Language
Full UI in English, Italian, Portuguese, Spanish. Switch from sidebar.

---

## PEF-100 Score

The PEF-100 (Persuasion Effectiveness Framework) scores pitch decks on five layers:

| Layer | Score | Question |
|-------|-------|----------|
| **Attention** | 0-25 | Does the deck capture focus? |
| **Understanding** | 0-25 | Can the reader process it efficiently? |
| **Belief** | 0-25 | Are the claims credible? |
| **Trust** | 0-25 | Is the team trustworthy? |
| **FOMO** | 0-25 | Is there urgency to act? |

**Penalties** (0-10 each):
- **Cognitive Friction** — How much mental effort the deck requires
- **Perceived Risk** — Red flags and risk indicators

**Final Score:** 0-100 (higher = more persuasive)

---

## User Manual

See [MANUALE_UTENTE.md](MANUALE_UTENTE.md) for the complete user guide.

### Quick Reference

| Action | How |
|--------|-----|
| Start app | `start.bat` or `streamlit run app.py` |
| Stop app | `stop.bat` or Ctrl+C |
| Change language | Sidebar → Language dropdown |
| Switch mode | Sidebar → Mode radio buttons |
| Generate pitch | Build Mode → Fill form → Generate Pitch |
| Audit deck | Audit Mode → Upload PDF → Run Deep Audit |
| Compare decks | Compare → Select decks from history |
| View history | History → Browse saved pitches |
| See analytics | Analytics → View charts and stats |

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11+
- **LLM:** Multi-provider (OpenAI, Anthropic, Google, Groq, OpenRouter)
- **PDF:** pypdf (extraction), reportlab (export)
- **DOCX:** python-docx
- **Data:** pandas (analytics)

---

## Project Structure

```
PitchMaster/
├── app.py                      # Streamlit app
├── start.bat                   # Windows launcher
├── stop.bat                    # Windows stopper
├── restart.bat                 # Windows restarter
├── requirements.txt            # Dependencies
├── .env.example                # API key template
├── pitch_master/
│   ├── __init__.py
│   ├── config.py               # Environment config
│   ├── llm_router.py           # Multi-provider LLM router
│   ├── providers.py            # Provider implementations
│   ├── prompts.py              # System prompts (4 languages)
│   ├── pef_engine.py           # PEF-100 scoring engine
│   ├── pdf_utils.py            # PDF text extraction
│   ├── export_utils.py         # MD, TXT, DOCX, PDF export
│   ├── languages.py            # UI translations (EN, IT, PT, ES)
│   ├── history.py              # Pitch history storage
│   └── templates.py            # Pitch templates
├── outputs/                    # Generated files
│   └── history/                # Saved pitches
├── README.md                   # This file
├── MANUALE_UTENTE.md           # User manual
└── LICENSE                     # MIT License
```

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## Roadmap

- [x] Multi-language support (EN, IT, PT, ES)
- [x] Pitch history and management
- [x] PEF-100 deck comparison
- [x] Pre-built pitch templates
- [x] Analytics dashboard
- [ ] PEF-100 human validation (3-rater IRR study)
- [ ] Outcome validation (Crunchbase data)
- [ ] Team collaboration features
- [ ] API endpoint for programmatic access
- [ ] Real-time pitch coaching mode
- [ ] Telegram/Discord bot integration

---

<p align="center">
  Made with ❤️ for founders and investors
</p>
