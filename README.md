# 🤖 AI Daily Updates

A Streamlit app that finds the most important AI news from the past 24 hours and turns it into short, readable cards: what happened, why it matters, and a link to the original source.

Web search is done with **Tavily**, and the analysis is done with **Groq (GPT-OSS-120B)**.

## Features

- One-click search for the latest AI news (models, products, tools, agents, research)
- Picks the 5–8 most important updates and removes duplicates
- Each update includes a summary, a "Why it matters" note, the company, and a category
- Featured top story, responsive card grid, and category filter
- Results are kept in session state, so filtering doesn't trigger a new search
- Source links are included so you can verify every item

## How it works

```
Get AI updates (button)
        │
        ▼
Tavily search  ──►  6 queries, news topic, last 24 hours
        │
        ▼
Deduplicate URLs, keep top 12 results, trim content
        │
        ▼
Groq GPT-OSS-120B  ──►  selects and summarizes updates as JSON
        │
        ▼
Streamlit UI  ──►  stats, category filter, featured story + card grid
```

## Project structure

```
.
├── app.py          # Streamlit UI
├── agent.py        # Tavily search + Groq analysis (get_ai_updates)
├── .env            # Your API keys (not committed)
├── .gitignore
└── README.md
```

## Getting started

### 1. Prerequisites

- Python 3.9 or newer
- A [Tavily](https://tavily.com) API key
- A [Groq](https://console.groq.com) API key

### 2. Clone and install

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install streamlit tavily-python groq python-dotenv
```

Optionally, save your dependencies with `pip freeze > requirements.txt` so others can install with `pip install -r requirements.txt`.

### 3. Add your API keys

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_key_here
GROQ_API_KEY=your_groq_key_here
```

Never commit this file. It is already listed in `.gitignore`.

### 4. Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501) and click **Get AI updates**.

## Configuration

You can tune these values in `agent.py`:

| Setting | Where | What it does |
|---|---|---|
| `queries` | `search_ai_updates()` | Topics searched on Tavily |
| `max_results` | `search_ai_updates()` | Results per query |
| `results[:12]` | `generate_ai_updates()` | How many articles are sent to the model |
| `content[:500]` | `generate_ai_updates()` | Characters of each article sent to the model |
| `max_completion_tokens` | Groq call | Output limit (keep it high, see troubleshooting) |
| `reasoning_effort` | Groq call | How much the model "thinks" before answering |

## Troubleshooting

**`json_validate_failed` / "max completion tokens reached before generating a valid document"**

GPT-OSS uses part of its token budget for reasoning, so a low limit can cut the JSON off. In the Groq call in `agent.py`, use:

```python
max_completion_tokens=8000,
reasoning_effort="low",
```

If it still fails, ask for 5 updates instead of 5–8 in the prompt.

**"No significant AI updates were found"**

Tavily returned nothing for the last 24 hours. Try again later, or add more queries.

**Authentication errors**

Check that `.env` is in the same folder you run `streamlit run app.py` from and that both keys are valid.

## Tech stack

- [Streamlit](https://streamlit.io): UI
- [Tavily](https://tavily.com): news search
- [Groq](https://groq.com) with `openai/gpt-oss-120b`: analysis and summarization
- [python-dotenv](https://pypi.org/project/python-dotenv/): environment variables

## Notes

- Summaries are generated only from the search results provided, but AI output can still contain mistakes. Use the source link to confirm important details.
- Each run makes 6 Tavily searches and 1 Groq call, so keep your API usage limits in mind.