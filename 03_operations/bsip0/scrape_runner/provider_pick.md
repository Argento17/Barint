# Provider Pick — Israeli VM for Scrape Runner

Scored 2026-06-12 for a single always-on small Linux VM (2 GB RAM, Israeli IP).

---

## Options

### Kamatera (Tel Aviv DC)

| Spec | Detail |
|---|---|
| Plan | 1 vCPU Type A (shared), 2 GB RAM, 20 GB NVMe, 5 TB traffic |
| Price | **$6/mo** (hourly also available) |
| Israeli IP | Yes — Tel Aviv datacenter, no geo-premium |
| Payment | Credit card (all major), PayPal; no minimum contract |
| Setup | Web console, no CLI required; 30-day / $100 free trial |
| Notes | Israeli-founded company; same price globally; 99.95% SLA |

Sources: kamatera.com/pricing ($6/mo SKU #p142548 confirmed), whtop.com/plans/kamatera.com/142548, vpsbenchmarks.com (Tel Aviv trial Nov 2025).

### AWS il-central-1 (Tel Aviv)

| Spec | Detail |
|---|---|
| Plan | t4g.small (2 vCPU ARM, 2 GB RAM) — cheapest with 2 GB |
| Price | **~$14.09/mo** on-demand; ~$8.91/mo 1-year reserved |
| Israeli IP | Yes — il-central-1 (Tel Aviv) |
| Payment | Credit card; AWS account required; reserved requires 1-yr commit |
| Notes | ARM (Graviton2) — Playwright/Chromium runs fine on ARM64, but all our existing scrapers are x86-tested. t3.small (x86) = $17.52/mo. Credit card + phone verification on signup. |

Source: aws-pricing.com/il-central-1.html, cloudprice.net/aws/ec2/instances/t4g.small.

### GCP me-west1 (Tel Aviv)

| Spec | Detail |
|---|---|
| Plan | e2-small (2 shared vCPU, 2 GB RAM) |
| Price | **~$13.45/mo** on-demand; ~$8.48/mo 1-year CUD |
| Israeli IP | Yes — me-west1 (Tel Aviv) |
| Payment | Credit card; GCP account required; CUD requires 1-yr commit |
| Notes | Shared vCPU. 1-year committed-use discount requires pre-purchase of $X/mo for 12 months. Free tier ($300 credit) available for new accounts. |

Source: gcloud-compute.com/me-west1.html, cloudprice.net/gcp/compute/instances/e2-small.

### Azure Israel Central (Modiin)

| Spec | Detail |
|---|---|
| Plan | B1ms (1 vCPU, 2 GB RAM) — smallest with 2 GB |
| Price | **~$15–18/mo** (israelcentral pricing not published on public pages; B1ms in eastus = ~$15/mo, Israel Central typically +0–30%) |
| Israeli IP | Yes — israelcentral (Modiin area) |
| Payment | Credit card; Azure account required |
| Notes | Newer region (opened 2023); fewer instance families available (only 51% of SKUs). B-series is burstable (CPU credits). Uncertain pricing without signing in. |

Source: cloudprice.net/region/israelcentral, Azure pricing pages.

---

## Comparison Table

| Provider | Monthly on-demand | 1-yr commit | CPU arch | Payment friction | Israeli IP guaranteed |
|---|---|---|---|---|---|
| **Kamatera** | **$6** | N/A (monthly) | x86 | Low — card/PayPal, no account hoop | Yes (Tel Aviv) |
| AWS il-central-1 | ~$14.09 (ARM) / $17.52 (x86) | ~$8.91 (ARM) | ARM or x86 | Medium — AWS account, phone verify | Yes (Tel Aviv) |
| GCP me-west1 | ~$13.45 | ~$8.48 (1-yr CUD) | x86 (shared) | Medium — GCP account, billing | Yes (Tel Aviv) |
| Azure Israel Central | ~$15–18 | ~$10–12 | x86 (burstable) | Medium — Azure account, billing | Yes (Modiin) |

---

## Recommendation

**Kamatera — $6/mo.**

Rationale:
1. **Lowest cost by 2x+.** $6 vs $13–18 for the hyperscalers. At $72/year this is negligible for the owner.
2. **Zero payment friction.** Credit card or PayPal, no account verification gauntlet, no phone verification, no 1-year commitment. Owner can sign up and have a VM running in ~10 minutes.
3. **x86 native.** Matches our existing toolchain. No ARM compatibility surprises.
4. **Israeli company, Israeli DC.** Legal simplicity and local support.
5. **Shared CPU is fine** — Playwright one-page-at-a-time barely touches 1 vCPU.

Hyperscalers only win if we need autoscaling, VPC peering, or enterprise IAM — we don't. For a single always-on 2GB box that runs a weekly cron job, Kamatera is the optimal choice.

**If Kamatera is rejected** (e.g., owner prefers a known brand): pick **AWS t4g.small reserved** (~$8.91/mo with 1-yr commit) — the best price among hyperscalers, but requires committing for a year.
