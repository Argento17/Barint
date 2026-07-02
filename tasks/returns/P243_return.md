# Return: P243

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P243_c2_magnesium_delivery_arithmetic_recheck.md` |
| Model | `opencode/deepseek-v4-flash-free` |
| Started | 2026-06-20T07:20:13.498253+00:00 |
| Finished | 2026-06-20T07:21:00.286088+00:00 |
| Exit code | 0 |

---

## Output

```
RETURNED — `tasks/returns/P243_return.md` written with the computed table.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.next.agent.switched: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e5ed001ESJBz4F5A7VpbZ", "timestamp": "2026-06-20T07:20:20.717Z", "agent": "build"}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "user", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "time": {"created": 1781940020717}, "age
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"type": "text", "text": "<!-- META (read first): ZERO-INFERENCE arithmetic. Do ONLY the math below. Do not judge copy,\n     do not infer, do n
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "diff": []}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"role": "user", "time": {"created": 1781940020717}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e6fd55001Okzc9OIlQfOpx3", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "snapshot
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "Let"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " compute"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " each"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " row"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "289"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "71"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "566"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "531"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "842"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "721"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "856"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "020"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "764"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "272"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "72"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "272"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "420"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " decimals"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "),"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "*"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "  "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Wait"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ratio"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "rounded"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " decimals"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " *"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " H"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "mm"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " actually"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Python"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "bank"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "er"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "'s"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " rounding"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Let"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " think"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "..."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " standard"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " rounding"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " rounds"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Okay"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "784"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "712"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "260"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "260"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "542"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "924"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "697"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "109"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "09"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "109"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "531"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "853"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "189"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "996"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "346"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "424"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "448"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "957"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "07"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "881"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "820"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "003"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "398"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "518"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "881"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "606"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "18"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "559"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "904"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "Wait"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "420"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " R"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "ounded"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " decimals"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " *"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Let"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " check"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "..."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " In"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Python"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " round"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "bank"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "er"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "'s"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " rounding"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " In"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " standard"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " math"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "135"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " rounds"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " Either"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " way"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "Let"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " row"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " row"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "71"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "71"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "272"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "72"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "72"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "272"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "355"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "260"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "260"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "109"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "09"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "09"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "109"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "07"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "07"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "18"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " \u2192"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "Now"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " write"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": " tasks"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "returns"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "/P"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "243"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "_return"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e6ff7a0017fA2zeI0Zg1J00", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e71b20001J06wNaAsST7Eso", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " b"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "arcode"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " ratio"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|---|---"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|---"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "289"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "71"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "271"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "566"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "531"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "842"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "721"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "856"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "314"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "020"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "764"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "72"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "272"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "420"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "136"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "784"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "712"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "260"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "542"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "924"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "697"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "09"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "109"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "531"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "853"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "21"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "189"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "996"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "346"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "424"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "944"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "448"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "957"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "07"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "881"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "820"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "89"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "003"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "398"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "518"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "16"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "011"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "881"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "606"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "32"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "106"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "559"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |\n"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "|"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "729"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "843"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "904"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": "24"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "partID": "prt_ee3e71b20001J06wNaAsST7Eso", "field": "text", "delta": " |"}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e72234001Ct8NoWwDs3xzVx", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"type": "tool", "tool": "read", "callID": "call_00_fMmVbN1iDpnX4Y5al57U7416", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\t
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"type": "tool", "tool": "read", "callID": "call_00_fMmVbN1iDpnX4Y5al57U7416", "state": {"status": "completed", "input": {"filePath": "C:\\Bari\
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e71b20001J06wNaAsST7Eso", "messageID": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e72804001Go4KJ1sESWtTyU", "reason": "tool-calls", "snapshot": "506d8f57b7db4bc6ccf65eae50ea41a5e5c68cc8", "messageID": "msg_ee3e6
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e6e7f1001ZAjLa6KXYGPeX2", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e72da5001zvLsWcQbWlUW8m", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "diff": []}
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"role": "user", "time": {"created": 1781940020717}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e739f0001wmUJffEqVKjxTH", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "snapshot
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " directory"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " exists"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " Let"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " write"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": " P"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": "243"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": "_return"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "partID": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e73bb3001feNpfQrFnFV4Wt", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e73d3f0014vrthlWCs20CCj", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"type": "tool", "tool": "write", "callID": "call_00_Y2b3pvq7NAvYz2vFKwel4182", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\
  file.edited: {"file": "C:\\Bari\\tasks\\returns\\P243_return.md"}
  file.watcher.updated: {"file": "C:\\Bari\\tasks\\returns\\P243_return.md", "event": "add"}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"type": "tool", "tool": "write", "callID": "call_00_Y2b3pvq7NAvYz2vFKwel4182", "state": {"status": "completed", "input": {"filePath": "C:\\Bari
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e74a00001nm2coyjzE0jeEa", "reason": "tool-calls", "snapshot": "1a75ef8dc9114850fd5f8fade91c7bfe31393dd5", "messageID": "msg_ee3e7
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e72da5001zvLsWcQbWlUW8m", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75111001ULkIT6R4jwLCyp", "messageID": "msg_ee3e72da5001zvLsWcQbWlUW8m", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e72da5001zvLsWcQbWlUW8m", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e75120001Q3lLp2mCmzGcbc", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "diff": []}
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"role": "user", "time": {"created": 1781940020717}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75acd001sxC5vqEAZS5siF", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "snapshot
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75cd3001ikAsDPECtyFYu7", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": "Task"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": " done"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": " propose"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": " RETURN"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75cd3001ikAsDPECtyFYu7", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75cd3001ikAsDPECtyFYu7", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75df6001QgBwr39oChNEIc", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "RET"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "URN"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " \u2014"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "tasks"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "returns"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "/P"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "243"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "_return"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " written"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " computed"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": " table"}
  message.part.delta: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "partID": "prt_ee3e75df6001QgBwr39oChNEIc", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e75df6001QgBwr39oChNEIc", "messageID": "msg_ee3e75120001Q3lLp2mCmzGcbc", "sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "type": "
  message.part.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "part": {"id": "prt_ee3e76483001ZPKOF8VK1Mqblz", "reason": "stop", "snapshot": "1a75ef8dc9114850fd5f8fade91c7bfe31393dd5", "messageID": "msg_ee3e7512000
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e75120001Q3lLp2mCmzGcbc", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "msg_ee3e75120001Q3lLp2mCmzGcbc", "parentID": "msg_ee3e6e5ed001zPY45z2QJI3Bof", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP"}
  session.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"id": "ses_11c192119ffeSZGRL5c6ua3ZSP", "slug": "crisp-planet", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "diff": []}
  message.updated: {"sessionID": "ses_11c192119ffeSZGRL5c6ua3ZSP", "info": {"role": "user", "time": {"created": 1781940020717}, "agent": "build", "model": {"providerID": "opencode", "modelID": "deepseek-v4-flash-free"},
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
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
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-356.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? _devserver.log
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? affected_set_spine.json
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
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
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? test_acceptance.py
```

### After dispatch

```
M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
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
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-356.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? _devserver.log
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? affected_set_spine.json
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
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
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? test_acceptance.py
```

### Delta

### New / modified since dispatch
  ?? tasks/returns/P243_return.md
