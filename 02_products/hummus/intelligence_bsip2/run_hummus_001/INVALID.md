# run_hummus_001 — INVALID FOR DISPLAY

**Status:** INVALID — do not use for user-facing display or frontend packaging  
**Invalidated by:** TASK-045  
**Date:** 2026-05-31  
**Reason:** Category routing defect — 44/69 products misrouted to `dessert` instead of `sauce_spread`; 7 products misrouted to `whole_food_fat`; 13 products misrouted to `default`. The `calorie_density` dimension (weight 15%) was computed from the wrong lookup table for 64 of 69 products.  
**Authoritative replacement:** `run_hummus_002` — path: `C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\`  
**Freeze report:** `C:\Bari\03_operations\bsip2\run_hummus_002\baseline_freeze_report.md`  
**Routing fix reference:** `C:\Bari\03_operations\bsip2\routing_fix_hummus_v1.md` (TASK-044)

Traces in this directory must not be read by the frontend pipeline or any scoring consumer.
