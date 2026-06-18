from pathlib import Path
path = Path(r"C:/Bari/03_operations/spine/dual_extract.py")
text = path.read_text(encoding="utf-8")
old = """            lines.append(
                f"- **{row['barcode']}** ({row['name']}):  "
                f"A={row['extractor_a']} vs B={row['extractor_b']}"
            )"""
new = """            lines.append(
                f"- **{row['barcode']}** ({row['name']}): `{row['field']}` "
                f"A={row['extractor_a']} vs B={row['extractor_b']}"
            )"""
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("fixed")
