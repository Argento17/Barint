from pathlib import Path
ROOT = Path(r"c:/Bari/bari-web")
SCRIPT = ROOT / "scripts/write-admin-expand.mjs"
SCRIPT.write_text("// building...\n", encoding="utf-8")
print("init", SCRIPT)
