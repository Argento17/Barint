# Dependency & Security Report — 2026-07-04

> READ-ONLY report (TASK-505 maintenance lane). Nothing was modified.
> Triage actions are PROPOSALS — apply via normal PR flow with build + e2e green.

## Summary
- Security vulnerabilities: **11** (npm audit rc=1; totals: critical=0, high=2, moderate=6, low=3, info=0; pip-audit NOT INSTALLED (pip install pip-audit to enable Python CVE scanning))
- Outdated majors (breaking-risk): **8**
- Outdated minors/patches (batch candidates): **82**
- Tool status: npm outdated rc=1; 3 major, 15 minor/patch; pip list --outdated rc=0; 5 major, 67 minor/patch

## 1. Security vulnerabilities (by severity)

### npm (bari-web)
| Package | Severity | Vulnerable range | Fixed in | Direct? | Advisory |
|---|---|---|---|---|---|
| hono | high | <=4.12.24 | fix available (npm audit fix) | no | Hono: IP Restriction bypasses static deny rules for non-canonical IPv6 ; Hono: Cookie helper does not sanitize sameSite  |
| tmp | high | <=0.2.5 | @lhci/cli@0.1.0 (SEMVER-MAJOR) | no | tmp allows arbitrary temporary file / directory write via symbolic link `dir` parameter; tmp has Path Traversal via unsa |
| @lhci/cli | moderate | * | @lhci/cli@0.1.0 (SEMVER-MAJOR) | yes | (transitive) |
| js-yaml | moderate | <=3.14.2 \|\| 4.0.0 - 4.1.1 | fix available (npm audit fix) | no | JS-YAML: Quadratic-complexity DoS in merge key handling via repeated aliases; JS-YAML: Quadratic-complexity DoS in merge |
| next | moderate | 9.3.4-canary.0 - 16.3.0-canary.5 | next@9.3.3 (SEMVER-MAJOR) | yes | (transitive) |
| postcss | moderate | <8.5.10 | next@9.3.3 (SEMVER-MAJOR) | no | PostCSS has XSS via Unescaped </style> in its CSS Stringify Output |
| qs | moderate | 6.11.1 - 6.15.1 | fix available (npm audit fix) | no | qs has a remotely triggerable DoS: qs.stringify crashes with TypeError on null/undefined entries in comma-format arrays  |
| uuid | moderate | <11.1.1 | @lhci/cli@0.1.0 (SEMVER-MAJOR) | no | uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided |
| @babel/core | low | <=7.29.0 | fix available (npm audit fix) | no | @babel/core: Arbitrary File Read via sourceMappingURL Comment |
| external-editor | low | >=1.1.1 | @lhci/cli@0.1.0 (SEMVER-MAJOR) | no | (transitive) |
| inquirer | low | 3.0.0 - 8.2.6 \|\| 9.0.0 - 9.3.7 | @lhci/cli@0.1.0 (SEMVER-MAJOR) | no | (transitive) |

### Python (pip-audit)
_pip-audit NOT INSTALLED (pip install pip-audit to enable Python CVE scanning)_

## 2. Outdated majors (breaking-risk — propose-only, never applied unattended)

### npm (bari-web)
| Package | Current | Wanted | Latest |
|---|---|---|---|
| @types/node | 20.19.41 | 20.19.43 | 26.1.0 |
| eslint | 9.39.4 | 9.39.4 | 10.6.0 |
| typescript | 5.9.3 | 5.9.3 | 6.0.3 |

### Python
| Package | Current | Latest |
|---|---|---|
| cryptography | 48.0.0 | 49.0.0 |
| protobuf | 6.33.6 | 7.35.1 |
| reportlab | 4.5.1 | 5.0.0 |
| rpds-py | 0.30.0 | 2026.6.3 |
| setuptools | 81.0.0 | 82.0.1 |

## 3. Outdated minors/patches (low-risk batch candidates)

### npm (bari-web)
| Package | Current | Wanted | Latest |
|---|---|---|---|
| @axe-core/playwright | 4.11.3 | 4.12.1 | 4.12.1 |
| @playwright/test | 1.60.0 | 1.61.1 | 1.61.1 |
| @tailwindcss/postcss | 4.3.0 | 4.3.2 | 4.3.2 |
| @types/react | 19.2.14 | 19.2.17 | 19.2.17 |
| eslint-config-next | 16.2.6 | 16.2.6 | 16.2.10 |
| framer-motion | 12.38.0 | 12.42.2 | 12.42.2 |
| lucide-react | 1.14.0 | 1.23.0 | 1.23.0 |
| next | 16.2.6 | 16.2.6 | 16.2.10 |
| playwright | 1.60.0 | 1.61.1 | 1.61.1 |
| radix-ui | 1.4.3 | 1.6.1 | 1.6.1 |
| react | 19.2.4 | 19.2.4 | 19.2.7 |
| react-dom | 19.2.4 | 19.2.4 | 19.2.7 |
| recharts | 3.8.1 | 3.9.2 | 3.9.2 |
| shadcn | 4.7.0 | 4.13.0 | 4.13.0 |
| tailwindcss | 4.3.0 | 4.3.2 | 4.3.2 |

### Python
| Package | Current | Latest |
|---|---|---|
| aiohappyeyeballs | 2.6.2 | 2.7.1 |
| aiohttp | 3.14.0 | 3.14.1 |
| altair | 6.1.0 | 6.2.2 |
| anyio | 4.13.0 | 4.14.1 |
| ast-grep-cli | 0.42.3 | 0.44.0 |
| beautifulsoup4 | 4.14.3 | 4.15.0 |
| cachetools | 7.1.3 | 7.1.4 |
| certifi | 2026.4.22 | 2026.6.17 |
| click | 8.4.0 | 8.4.2 |
| crawlee | 1.7.2 | 1.8.0 |
| fastapi | 0.136.3 | 0.139.0 |
| filelock | 3.29.1 | 3.29.5 |
| fsspec | 2026.4.0 | 2026.6.0 |
| google-api-core | 2.30.3 | 2.31.0 |
| google-auth | 2.52.0 | 2.55.1 |
| google-cloud-vision | 3.14.0 | 3.15.0 |
| greenlet | 3.5.0 | 3.5.3 |
| grpcio | 1.80.0 | 1.81.1 |
| grpcio-status | 1.80.0 | 1.81.1 |
| headroom-ai | 0.23.0 | 0.30.0 |
| hf-xet | 1.5.0 | 1.5.1 |
| hpack | 4.1.0 | 4.2.0 |
| httptools | 0.7.1 | 0.8.0 |
| huggingface_hub | 1.18.0 | 1.22.0 |
| idna | 3.15 | 3.18 |
| impit | 0.12.0 | 0.13.1 |
| jiter | 0.15.0 | 0.16.0 |
| litellm | 1.82.3 | 1.83.7 |
| llvmlite | 0.47.0 | 0.48.0 |
| lxml | 6.1.0 | 6.1.1 |
| matplotlib | 3.10.9 | 3.11.0 |
| mcp | 1.27.2 | 1.28.1 |
| mpmath | 1.3.0 | 1.4.1 |
| narwhals | 2.21.2 | 2.23.0 |
| numba | 0.65.1 | 0.66.0 |
| numpy | 2.4.4 | 2.5.0 |
| onnxruntime | 1.26.0 | 1.27.0 |
| openai | 2.41.0 | 2.44.0 |
| opentelemetry-api | 1.42.1 | 1.43.0 |
| pillow | 12.2.0 | 12.3.0 |
| pip | 26.1.1 | 26.1.2 |
| playwright | 1.59.0 | 1.61.0 |
| plotly | 6.7.0 | 6.8.0 |
| Protego | 0.6.0 | 0.6.2 |
| pydantic_core | 2.46.4 | 2.47.0 |
| pydantic-settings | 2.14.1 | 2.14.2 |
| pydeck | 0.9.2 | 0.9.3 |
| pyOpenSSL | 26.2.0 | 26.3.0 |
| pypdf | 6.13.0 | 6.14.2 |
| pytest | 9.0.3 | 9.1.1 |
| python-multipart | 0.0.29 | 0.0.32 |
| regex | 2026.5.9 | 2026.6.28 |
| requests | 2.34.1 | 2.34.2 |
| safetensors | 0.7.0 | 0.8.0 |
| soupsieve | 2.8.3 | 2.8.4 |
| sse-starlette | 3.4.4 | 3.4.5 |
| starlette | 1.0.0 | 1.3.1 |
| streamlit | 1.57.0 | 1.58.0 |
| tokenizers | 0.22.2 | 0.23.1 |
| torch | 2.12.0 | 2.12.1 |
| tqdm | 4.68.1 | 4.68.3 |
| transformers | 5.10.2 | 5.13.0 |
| tree-sitter | 0.25.2 | 0.26.0 |
| tree-sitter-language-pack | 1.8.1 | 1.12.2 |
| typer | 0.25.1 | 0.26.8 |
| typing_extensions | 4.15.0 | 4.16.0 |
| uvicorn | 0.47.0 | 0.50.0 |

## 4. Triage recommendations (propose-only)

| Package | Ecosystem | Action | Reason |
|---|---|---|---|
| hono | npm | patch now | high vulnerability; fix: fix available (npm audit fix) |
| tmp | npm | propose major | high vulnerability; fix: @lhci/cli@0.1.0 (SEMVER-MAJOR) |
| @lhci/cli | npm | batch | moderate vulnerability; fix: @lhci/cli@0.1.0 (SEMVER-MAJOR) |
| js-yaml | npm | batch | moderate vulnerability; fix: fix available (npm audit fix) |
| next | npm | batch | moderate vulnerability; fix: next@9.3.3 (SEMVER-MAJOR) |
| postcss | npm | batch | moderate vulnerability; fix: next@9.3.3 (SEMVER-MAJOR) |
| qs | npm | batch | moderate vulnerability; fix: fix available (npm audit fix) |
| uuid | npm | batch | moderate vulnerability; fix: @lhci/cli@0.1.0 (SEMVER-MAJOR) |
| @babel/core | npm | ignore-with-reason | low/info severity; batch with next routine update (fix available (npm audit fix)) |
| external-editor | npm | ignore-with-reason | low/info severity; batch with next routine update (@lhci/cli@0.1.0 (SEMVER-MAJOR)) |
| inquirer | npm | ignore-with-reason | low/info severity; batch with next routine update (@lhci/cli@0.1.0 (SEMVER-MAJOR)) |
| @types/node | npm | propose major | 20.19.41 -> 26.1.0 breaking-risk; needs migration notes |
| eslint | npm | propose major | 9.39.4 -> 10.6.0 breaking-risk; needs migration notes |
| typescript | npm | propose major | 5.9.3 -> 6.0.3 breaking-risk; needs migration notes |
| @axe-core/playwright, @playwright/test, @tailwindcss/postcss, @types/react, eslint-config-next, framer-motion, lucide-react, playwright, radix-ui, react, react-dom, recharts, shadcn, tailwindcss | npm | batch | 14 minor/patch bumps; low-risk batch behind build+e2e green |


---
_Generated by `03_operations/maintenance/deps_report.py`. Rules: security patches within same major -> normal PR flow (build + e2e green); majors -> propose with migration notes; next/react/playwright majors -> Frontend Agent; never auto-merge; never touch the deploy repo directly._