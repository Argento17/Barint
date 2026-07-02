path = "C:/Bari/bari-web/src/components/comparisons/magnesium-comparison-page.tsx"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# Remove the unknown props from the ComparisonPage call
lines_to_remove = [
    "      collapseMobileNote\n",
    "      collapseMobilePrologue\n",
    "      noAutoExpand\n",
    "      headerSlot={<MagnesiumSafetyBox />}\n",
    "      clampVerdictLines={3}\n",
    "      compactDividers\n",
    "      forcePartialDisclosure\n",
]
for line in lines_to_remove:
    txt = txt.replace(line, "")

# Also remove the MagnesiumSafetyBox import since it's no longer used
txt = txt.replace('import { MagnesiumSafetyBox } from "@/components/shared/magnesium-safety-box";\n', "")

with open(path, "w", encoding="utf-8") as f:
    f.write(txt)
print("fixed")
# Verify
with open(path, encoding="utf-8") as f:
    print(f.read())
