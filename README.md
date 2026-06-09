# Pitch Master

Open-source fundraising copilot for founders and investors.

## What is Pitch Master?

Pitch Master is a local web app that helps founders and investors with two modes:

- **Build Mode**: Answer a guided questionnaire, get a spendable pitch (one-liner, deck outline, investor narrative, email intro)
- **Audit Mode**: Upload a PDF pitch deck, get a PEF-100 score and actionable improvement suggestions

## Installation

```bash
git clone https://github.com/your-org/pitch-master.git
cd pitch-master
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Setup

Edit `.env` with your API key:

```env
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

Supported providers: `openai`, `anthropic`, `google`, `groq`, `openrouter`

## Run

```bash
streamlit run app.py
```

## Build Mode

1. Fill in the questionnaire (Company, Problem, Solution, Why Now, Market, Business Model, Traction, Team, Ask)
2. Click "Generate Pitch"
3. Get: executive summary, deck outline, investor narrative, email intro, PEF self-audit
4. Download as Markdown, TXT, or DOCX

## Audit Mode

1. Upload a PDF pitch deck
2. View extracted text preview
3. See automatic PEF-100 score (Attention, Understanding, Belief, Trust, FOMO, Cognitive Friction)
4. Get LLM-powered qualitative audit with specific improvement suggestions

## PEF-100 Score

The PEF-100 (Persuasion Effectiveness Framework) scores pitch decks on five layers:

- **Attention**: Does the deck capture focus?
- **Understanding**: Can the reader process it efficiently?
- **Belief**: Are the claims credible?
- **Trust**: Is the team trustworthy?
- **FOMO**: Is there urgency to act?

Plus penalties for Cognitive Friction and Perceived Risk.

> **Disclaimer**: This is a heuristic v0.1 score, not investment advice. Pitch Master does not decide whether a company is investable. It helps founders and investors structure thinking around pitch clarity and persuasion.

## Tech Stack

- Python 3.11+
- Streamlit
- OpenAI / Anthropic / Google / Groq / OpenRouter SDKs
- pypdf (PDF extraction)
- python-docx (DOCX export)
- reportlab (PDF export)

## License

MIT License. See [LICENSE](LICENSE).

## Roadmap

- [ ] PEF-100 human validation (3-rater IRR study)
- [ ] Outcome validation (Crunchbase fundraising data)
- [ ] Multi-language support
- [ ] Team collaboration features
- [ ] API endpoint for programmatic access
- [ ] Real-time pitch coaching mode

## Disclaimer

Pitch Master is not financial advice. Pitch Master does not decide whether a company is investable. It helps founders and investors structure thinking around pitch clarity and persuasion.
