"""Bari external-data integration clients.

Thin, read-only clients over authoritative external sources, granted to agents as
capabilities (see TASK-170). Each client is import-safe and exposes a small typed
surface. Run any client module directly (`python -m integrations.clients.<name>`)
for a live smoke test.

Sources:
  open_food_facts  — DISABLED (TASK-238 OFF ban, project-wide, forever). Raises OffDisabledError
                     on every call. NOT a data source. Retained only as the enforced ban guard;
                     see open_food_facts.py. Never use OFF for any field, any category.
  il_prices        — Israeli price-transparency feeds (Data)
  literature       — PubMed E-utilities + Europe PMC (Research)
  tzameret         — Israeli MoH food-composition DB (Nutrition)
  pagespeed        — Google PageSpeed Insights (Frontend)
  github_artifacts — merged-commit / CI / deploy state via `gh` (CC)
"""
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)
