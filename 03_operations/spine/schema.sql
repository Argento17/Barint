-- Project Spine1 (TASK-252) — pipeline datastore schema v1.
-- SQLite dialect, kept portable (TEXT/INTEGER/REAL only) so a later
-- DuckDB/Postgres move is a port, not a rewrite.
-- spine.db is generated state (gitignored); this file is the law.

CREATE TABLE IF NOT EXISTS runs (
  run_id        TEXT NOT NULL,            -- e.g. run_yogurt_006
  layer         TEXT NOT NULL,            -- bsip1 | bsip2 | frontend
  category      TEXT,                     -- product-system folder, e.g. yogurt_system
  engine        TEXT,                     -- e.g. proto_v0/0.4.1
  generated_at  TEXT,
  meta_json     TEXT,
  PRIMARY KEY (run_id, layer)
);

CREATE TABLE IF NOT EXISTS products (
  product_key   TEXT PRIMARY KEY,         -- canonical id (bsip1_yogurt_X); barcode as fallback
  barcode       TEXT,
  name_he       TEXT,
  brand         TEXT,
  category      TEXT                      -- engine category at last ingest
);

CREATE TABLE IF NOT EXISTS scores (
  run_id           TEXT NOT NULL,
  product_key      TEXT NOT NULL,
  score            REAL,                  -- final_score_estimate
  grade            TEXT,                  -- grade_estimate
  confidence_band  TEXT,
  confidence_score REAL,
  engine_category  TEXT,
  nova_proxy       INTEGER,
  trace_path       TEXT,
  PRIMARY KEY (run_id, product_key)
);

CREATE TABLE IF NOT EXISTS artifacts (
  path        TEXT PRIMARY KEY,
  kind        TEXT NOT NULL,              -- bsip1_record | bsip2_trace | frontend_json | run_summary | stage_output
  sha256      TEXT NOT NULL,
  bytes       INTEGER,
  mtime       TEXT,
  run_id      TEXT,
  recorded_at TEXT
);

CREATE TABLE IF NOT EXISTS lineage (
  child_path  TEXT NOT NULL,
  parent_path TEXT NOT NULL,
  relation    TEXT NOT NULL DEFAULT 'derived_from',
  PRIMARY KEY (child_path, parent_path)
);

-- One row per frontend data file actually consumable by the website.
CREATE TABLE IF NOT EXISTS live_state (
  data_file     TEXT PRIMARY KEY,         -- path under bari-web/src/data/comparisons
  category      TEXT,
  version       TEXT,                     -- _meta.version or parsed from filename
  run_id        TEXT,                     -- _meta.run_id when present
  product_count INTEGER,
  generated_at  TEXT,                     -- _meta.generated
  sha256        TEXT,
  recorded_at   TEXT
);

-- DAG runner bookkeeping: one row per (stage, input-signature) execution.
CREATE TABLE IF NOT EXISTS stage_runs (
  stage_name   TEXT NOT NULL,
  signature    TEXT NOT NULL,             -- sha256 over (name + code_version + input hashes)
  status       TEXT NOT NULL,             -- ok | failed
  started_at   TEXT,
  finished_at  TEXT,
  outputs_json TEXT,                      -- [{"path":..., "sha256":...}, ...]
  error        TEXT,
  PRIMARY KEY (stage_name, signature)
);

CREATE INDEX IF NOT EXISTS idx_scores_product  ON scores(product_key);
CREATE INDEX IF NOT EXISTS idx_artifacts_run   ON artifacts(run_id);
CREATE INDEX IF NOT EXISTS idx_lineage_parent  ON lineage(parent_path);
