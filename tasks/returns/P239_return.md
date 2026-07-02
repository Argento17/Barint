# Return: P239

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P239_c2_sie_sa_traceability_audit.md` |
| Model | `opencode/deepseek-v4-flash-free` |
| Started | 2026-06-19T09:34:11.897904+00:00 |
| Finished | 2026-06-19T09:34:51.399832+00:00 |
| Exit code | 0 |

---

## Output

```
**S/A items (20):**

| barcode | grade | score | acquisition_method | name_he |
|---|---|---|---|---|
| 7290012760266 | S | 91.2 | search_panel | סופהרב ויטמין D3-1000 טיפות בד"ץ |
| 7290019444312 | A | 82.8 | brand_panel | אלטמן חומצה פולית פלוס 400 מקג 90 טבליות |
| 7290118814061 | S | 91.2 | search_panel | סופהרב ברזל 9 חודשים 60 כמוסות |
| 7290013142146 | S | 91.2 | brand_panel | אלטמן ויטמין D-1000 טיפות 15 מל |
| 7290012760891 | A | 81.0 | search_panel | סופהרב סידן 600 בדץ 60 טבליות |
| 7290017243450 | S | 91.2 | search_panel | סופהרב ויטמין B12+חומצה פולית 100 טבליות |
| 7290012056741 | S | 91.2 | search_panel | טינק ברזל נוח 90 כמוסות |
| 7290017490601 | S | 91.2 | search_panel | נוטריקר D3+K2 ויטמין 1000 יחבל 60 כמוסות |
| 7290018439623 | S | 91.2 | search_panel | נוטריקר ויטמין די-1000 יח 90 כמוסות רכות |
| 7290012760761 | S | 91.2 | search_panel | סופהרב ויטמין D-1000 כמוסות 90 |
| 7290019444374 | S | 91.2 | brand_panel | אלטמן גאמיס ויטמין D 1000 כמוסות 60 יח |
| 7290017218366 | S | 91.2 | brand_panel | אלטמן ויטמין D-1000 כמוסות רכות 100 יחיד |
| 7290006437273 | A | 82.8 | brand_panel | אלטמן חומצה פולית 400 מקג 200 טבליות |
| 7290010035984 | S | 91.2 | search_panel | פלוריש ויטמין D-1000 טיפות למבוגרים |
| 7290015765572 | S | 91.2 | brand_panel | אלטמן ויטמין B12 מתיל קובלאמין 60 טבליות |
| 7290008111041 | A | 82.8 | search_panel | הדס חומצה פולית 400 מקג 200 טבליות |
| 712179581913 | S | 91.2 | search_panel | קטגורי 5- ליפוזמין B12 ספקטרום 60 כמוסות |
| 783495578741 | S | 91.2 | search_panel | קטגורי 5- ליפוזמין.Fe ברזל 60 כמוסות |
| 7290001471845 | A | 86.2 | brand_panel | אלטמן ויטמין B12 פלוס 120 טבליות |
| 7290015318433 | S | 91.2 | search_panel | טינק ויטמין D1000 טיפות 20 מל |

**name_derived in S+A: 0** (empty list — no top-grade item has `name_derived` acquisition)

```json
{"task_id":"P239","status":"RETURNED","agent":"c2-deepseek",
 "sa_total":20,"name_derived_in_sa":0,
 "name_derived_barcodes":[]}
```

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.next.agent.switched: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2e45001MwO5iqOX1e5fNt", "timestamp": "2026-06-19T09:34:18.181Z", "agent": "build"}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "user", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "time": {"created": 1781861658181}, "age
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "text", "text": "META (read first): Zero-inference extraction only. Do NOT judge grades or reason about correctness. Read the file, fil
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b2fff001mBVwnjMhpEhR0A", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "diff": []}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"role": "user", "time": {"created": 1781861658181}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b3b99001coruyveIsvUPte", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "snapshot
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": "Let"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "add"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "unlink"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " read"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " file"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " extract"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "partID": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b3d2b001ZfWcx4Y1kFx7LU", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b3e7100124PnN7VbdZ8unn", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "add"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "unlink"}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"status": "running", "input": {"command": "python -c \"
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"metadata": {"output": "", "description": "Extract S/A 
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"metadata": {"output": "Traceback (most recent call las
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"metadata": {"output": "Traceback (most recent call las
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"metadata": {"output": "Traceback (most recent call las
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_HB7TiYvZVpZqT2vkAWaj8709", "state": {"status": "completed", "input": {"command": "python -c 
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b4ec6001L2J2aUbz69UY0c", "reason": "tool-calls", "snapshot": "ed9a000e07767877e90354420fd75c9fee2eeb5c", "messageID": "msg_edf3b
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b2fff001mBVwnjMhpEhR0A", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b55e5001Ifi0n6l6UVWQRi", "messageID": "msg_edf3b2fff001mBVwnjMhpEhR0A", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b2fff001mBVwnjMhpEhR0A", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b55f4001QSWKZpvzhYsgej", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "diff": []}
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"role": "user", "time": {"created": 1781861658181}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b5e5f001hLBsGf5ScKL2TJ", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "snapshot
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b6020001ee6uIpsiF1uEbq", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " error"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " Unicode"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " encoding"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " characters"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " Windows"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " Let"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " UTF"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " encoding"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": " output"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "partID": "prt_edf3b6020001ee6uIpsiF1uEbq", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b6020001ee6uIpsiF1uEbq", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b61d5001dEUcKBuTY3a194", "messageID": "msg_edf3b55f4001QSWKZpvzhYsgej", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_XlB7WBs0acRdVJr32qcd7736", "state": {"metadata": {"output": "", "description": "Extract S/A 
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_XlB7WBs0acRdVJr32qcd7736", "state": {"metadata": {"output": "", "description": "Extract S/A 
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_XlB7WBs0acRdVJr32qcd7736", "state": {"metadata": {"output": "=== S/A items (20) ===\r\n72900
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"type": "tool", "tool": "bash", "callID": "call_00_XlB7WBs0acRdVJr32qcd7736", "state": {"status": "completed", "input": {"command": "python -X 
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b6ded001v9wiLqAnPse4Qr", "reason": "tool-calls", "snapshot": "ed9a000e07767877e90354420fd75c9fee2eeb5c", "messageID": "msg_edf3b
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b55f4001QSWKZpvzhYsgej", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b55f4001QSWKZpvzhYsgej", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b71db001iaTz8yMuufXcIT", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "diff": []}
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"role": "user", "time": {"created": 1781861658181}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b79c2001CsMGBxaOJRsMPT", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "snapshot
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b7be50017wZ3YT48pE2mpD", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " results"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " clear"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " There"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "+A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " items"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " none"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " them"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " have"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "ac"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "quisition"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "_method"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " =="}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " list"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " empty"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "Let"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " output"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": " results"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7be50017wZ3YT48pE2mpD", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b7be50017wZ3YT48pE2mpD", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b7da9001nTCDkcHvlozlh3", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "/A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " items"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "):"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " b"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "arcode"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " grade"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " acquisition"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_method"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "he"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|---|---"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|---|---"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|---"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "276"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "026"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e4\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "431"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "82"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05e7\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "90"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "881"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "406"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e4\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d1\u05e8\u05d6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "214"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "276"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "089"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "81"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e4\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "600"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d1\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "724"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "345"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e4\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "+"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "205"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "674"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d1\u05e8\u05d6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "90"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "749"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "060"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "+K"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "962"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e7\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "90"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e8\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "276"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "076"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e4\u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "90"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "437"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d0\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "721"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "836"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e8\u05db\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "643"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "727"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "82"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05e7\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "003"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "598"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05dc\u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e8\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "576"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "557"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc\u05d0\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "811"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "104"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "82"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d4\u05d3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05de\u05e6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05e7\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "712"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "179"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "581"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "913"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e7\u05d8\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e8\u05d9"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e1\u05e4\u05e7\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05e8\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "783"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "495"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "578"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "741"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e7\u05d8\u05d2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e8\u05d9"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05d6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": ".F"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "e"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d1\u05e8\u05d6"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05db\u05de\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "147"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "184"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "86"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d0\u05dc\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "120"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "531"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_p"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "anel"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e0\u05e7"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d5"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05df"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05d8"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d9\u05e4"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u05de\u05dc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " |\n\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "+A"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "empty"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " list"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " top"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-grade"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " item"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " acquisition"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": ")\n\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "```"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "json"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "{\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "task"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_id"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "P"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "239"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\",\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "status"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "RET"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "URN"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\",\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "agent"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "-de"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ep"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "seek"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\",\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "sa"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_total"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": ",\""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_in"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_s"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": ",\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "name"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "der"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "ived"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "_b"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "arc"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "odes"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "[]"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "}\n"}
  message.part.delta: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "partID": "prt_edf3b7da9001nTCDkcHvlozlh3", "field": "text", "delta": "```"}
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b7da9001nTCDkcHvlozlh3", "messageID": "msg_edf3b71db001iaTz8yMuufXcIT", "sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "type": "
  message.part.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "part": {"id": "prt_edf3b9661001DLTopzHAxlIUga", "reason": "stop", "snapshot": "ed9a000e07767877e90354420fd75c9fee2eeb5c", "messageID": "msg_edf3b71db00
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b71db001iaTz8yMuufXcIT", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "msg_edf3b71db001iaTz8yMuufXcIT", "parentID": "msg_edf3b2e45001Gz1kLpt7DjtTDU", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4"}
  session.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"id": "ses_120c4d751ffexhSlP6f808k6C4", "slug": "nimble-sailor", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bar
  session.diff: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "diff": []}
  message.updated: {"sessionID": "ses_120c4d751ffexhSlP6f808k6C4", "info": {"role": "user", "time": {"created": 1781861658181}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M tasks/DISPATCH_BOARD.md
?? 03_operations/shadow/goldset/
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? affected_set_spine.json
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING.json
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING_gates_report.md
?? tasks/TASK-349.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? test_acceptance.py
```

### After dispatch

```
M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M tasks/DISPATCH_BOARD.md
?? 03_operations/shadow/goldset/
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? affected_set_spine.json
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING.json
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING_gates_report.md
?? tasks/TASK-349.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? test_acceptance.py
```

### Delta

### Removed / cleaned since dispatch
   M bari-web/src/data/comparisons/cereals_frontend_v2.json
