from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "write-admin-expand.mjs"
# Minimal runner - full logic inline
text = r'''import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

function write(rel, content) {
  const abs = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, content, "utf8");
  console.log("wrote", rel);
}

function patch(rel, fn) {
  const abs = path.join(ROOT, rel);
  const before = fs.readFileSync(abs, "utf8");
  const after = fn(before);
  if (after !== before) {
    fs.writeFileSync(abs, after, "utf8");
    console.log("patched", rel);
  }
}

'''
OUT.write_text(text, encoding="utf-8")
print("started", OUT)
