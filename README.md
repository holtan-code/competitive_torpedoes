# Competitive Torpedoes

Brand performance comparison dashboard. Compares SOCi platform metrics against competitor platforms using LVI scoring data.

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/competitive_torpedoes.git
cd competitive_torpedoes
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL and OPENAI_API_KEY
streamlit run app.py
```

## Project Structure

```
competitive_torpedoes/
  app.py              Main Streamlit entry point
  config.py           Settings, env vars, constants
  db.py               Database queries (SQLAlchemy)
  ai_analysis.py      OpenAI chat integration
  charts.py           Plotly chart builders
  components/
    __init__.py
    header.py          Header + platform selector
    overall.py         Overall scores section
    search.py          Search metrics section
    reputation.py      Reputation metrics section
    social.py          Social metrics section
  assets/
    style.css          Custom CSS overrides
```

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key for chart analysis |
