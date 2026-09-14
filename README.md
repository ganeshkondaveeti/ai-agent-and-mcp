# Groww Weekly Pulse AI Agent

An automated pipeline that fetches Google Play Store reviews for the Groww app, cleans them of PII, clusters them into themes using an LLM, generates a weekly pulse report, and publishes the report via Google Docs and Gmail using an MCP server.

This project is orchestrated using LangChain's ReAct agent and LangGraph. It runs autonomously in the background as a daemon and automatically triggers on a set schedule.

## Architecture

See [architecture.md](docs/architecture.md) for the high-level system design.
See [implementation-plan.md](docs/implementation-plan.md) for a breakdown of the build phases.

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- An MCP Server running the Google Workspace integration (Docs + Gmail). A deployed instance is configured by default.

### 2. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. API Keys
Create a `.env` file in the root directory and add the following keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: `GEMINI_API_KEY` is used for agent orchestration, and `GROQ_API_KEY` is used for token-heavy data clustering).*

## Usage

### Run the Pipeline Once
To execute the pipeline manually right now:
```bash
source .venv/bin/activate
export PYTHONPATH=.
python src/main.py
```

### Run the Background Scheduler
To start the daemon that will trigger the pipeline automatically on a weekly schedule (Mondays at 9:00 AM):
```bash
source .venv/bin/activate
export PYTHONPATH=.
python src/scheduler.py
```

## Configuration Reference
You can tweak parameters in `config/settings.yaml`:
- **app**: Change `play_store_id`, `review_window_weeks`, or `max_reviews`.
- **clustering**: Adjust `max_themes` and how many make it to the final pulse.
- **pulse**: Set `max_words`, `num_quotes`, and `num_action_ideas`.
- **email**: Set the `recipient` or `subject_template`.

## Error Handling & Fallbacks
If the MCP server becomes unreachable or fails to connect, the agent will gracefully switch into **fallback mode**. It will skip publishing to Docs and Email, and will instead save the generated markdown pulse locally to the `output/` directory (e.g., `output/pulse_2026-W37.md`) so the data is not lost.
