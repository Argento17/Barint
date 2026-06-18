# Return: P174

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P174_counterfactual_method.md` |
| Model | `gemini/cli` |
| Started | 2026-06-18T04:51:47.139179+00:00 |
| Finished | 2026-06-18T05:07:15.451940+00:00 |
| Exit code | 0 |

---

## Output

```
I have successfully completed task P174.

### Accomplishments
1.  **Implemented Counterfactual Method**: Created a standalone Python module `03_operations/bsip2/proto_v0/src/method_counterfactual.py` that identifies the minimal changes to label-observable inputs (sugar, sodium, ingredient count, seed oil, additives) required to improve a product's grade.
2.  **Advanced Logic**: The script supports both **single-lever** and **two-lever** counterfactuals, simulating the scoring engine's dimensions, caps, and penalties based on sensitivities derived from the BSIP2 traces and current grade policies.
3.  **Comprehensive Reporting**: Generated `sample.json` and `sample.md` reports by processing 53 live product traces. The results show that 13 products have achievable grade improvements via one or two levers.
4.  **Zero Engine Impact**: Verified that no existing engine modules, constants, or configurations were modified, maintaining the "read-only" constraint over the scoring path.

### Key Metrics
*   **Products Processed**: 53
*   **Achievable Improvements**: 13 (3 single-lever, 10 two-lever)
*   **Achievable False**: 40

### Deliverables
*   Script: `03_operations/bsip2/proto_v0/src/method_counterfactual.py`
*   Reports: `03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json` and `sample.md`
*   Return Contract: `tasks/returns/P174_return.md`

I propose this task as **RETURNED**.


--- STDERR ---
Warning: True color (24-bit) support not detected. Using a terminal with true color enabled will result in a better visual experience.
YOLO mode is enabled. All tool calls will be automatically approved.
YOLO mode is enabled. All tool calls will be automatically approved.
Ripgrep is not available. Falling back to GrepTool.
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:52:48 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=786',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e046ae2cf5d01309',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:53:09 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=861',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '37855b93e328e555',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:53:32 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=954',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '25b972b782860277',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
(node:17856) [DEP0190] DeprecationWarning: Passing args to a child process with shell option true can lead to security vulnerabilities, as the arguments are not escaped, only concatenated.
(Use `node --trace-deprecation ...` to show where the warning was created)
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:53:50 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1180',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '1701d8da72f65bb5',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:53:56 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1211',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e7944820e084688a',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:54:09 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=984',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '76f7a7467b11b54a',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:56:07 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1237',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '5836778c86937a6c',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:56:21 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1119',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'c5ed0e5f4ba506df',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:56:28 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1342',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '3e32b8a20def762f',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:56:38 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1124',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '30ec9a4682d594c6',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:57:10 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1503',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '659db03d1a9f5b2e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:57:16 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1614',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '6f13d0ce0bb47b3d',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:57:26 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=997',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'b09497872d703d70',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 4 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:57:48 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1065',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '6f1f899480b7915b',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 5 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:58:25 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=994',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e61d1c02311a36ce',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:59:34 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1340',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '706151fb9d7a7333',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 04:59:40 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=939',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '25826c8fc896f770',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:00:27 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1172',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '9d1619b051a07ab4',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:00:34 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1190',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '6851abbcc2a92cca',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:00:48 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1263',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '472768b769aa1f1',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 4 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:01:08 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1209',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '426f8188b608bc54',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:01:43 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1139',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '45e41f439704ef1d',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:01:48 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1415',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'b44f5be2fcea8483',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:02:26 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1299',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '755c5982c6578410',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:02:32 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1314',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e6b2bc53a365d032',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:02:45 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1433',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '6ace7ee0ac4fb05e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:03:29 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1507',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'bcbf78d18a1681f6',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:03:35 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1230',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '1e6dc50be9c7684e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:04:05 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1486',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e0ce21b2317836c6',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:04:15 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1472',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'b850692954e79444',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:04:20 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=899',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'dc2ee856ae0465f6',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:04:47 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1382',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '9ffe64bd9649bb90',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:04:56 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=780',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '8b9d135f28dc60cc',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:05:01 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=968',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '3e1b5384b44b0254',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 3 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:05:10 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=989',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '9ca8bbca90525f55',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:05:44 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=787',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '5d26104b50ee2ab5',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:05:51 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1391',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '2df21311576ffd02',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:06:11 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1512',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'c7842ff5df66bd6e',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 1 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:06:38 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1482',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e4cb76868165576c',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
Attempt 2 failed with status 429. Retrying with backoff... _GaxiosError: [{
  "error": {
    "code": 429,
    "message": "No capacity available for model gemini-3-flash-preview on the server",
    "errors": [
      {
        "message": "No capacity available for model gemini-3-flash-preview on the server",
        "domain": "global",
        "reason": "rateLimitExceeded"
      }
    ],
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "MODEL_CAPACITY_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "model": "gemini-3-flash-preview"
        }
      }
    ]
  }
}
]
    at Gaxios._request (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:20961:19)
    at process.processTicksAndRejections (node:internal/process/task_queues:104:5)
    at async _OAuth2Client.requestAsync (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:22924:17)
    at async CodeAssistServer.requestStreamingPost (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307166:17)
    at async CodeAssistServer.generateContentStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:306964:23)
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:307841:19
    at async file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:283590:23
    at async retryWithBackoff (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:304851:23)
    at async GeminiChat.makeApiCallAndProcessStream (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328315:28)
    at async GeminiChat.streamWithRetries (file:///C:/Users/HP/AppData/Roaming/npm/node_modules/@google/gemini-cli/bundle/chunk-RCJSF5RP.js:328133:29) {
  config: {
    url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
    method: 'POST',
    params: { alt: 'sse' },
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'CloudCodeVSCode/0.46.0 (aidev_client; os_type=Windows; os_version=10.0.26200; arch=x64; host_path=VSCode/unknown; proxy_client=geminicli) google-api-nodejs-client/9.15.1',
      Authorization: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      'x-goog-api-client': 'gl-node/24.15.0'
    },
    responseType: 'stream',
    body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
    signal: AbortSignal { aborted: false },
    retry: false,
    paramsSerializer: [Function: paramsSerializer],
    validateStatus: [Function: validateStatus],
    errorRedactor: [Function: defaultErrorRedactor]
  },
  response: {
    config: {
      url: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse',
      method: 'POST',
      params: [Object],
      headers: [Object],
      responseType: 'stream',
      body: '<<REDACTED> - See `errorRedactor` option in `gaxios` for configuration>.',
      signal: [AbortSignal],
      retry: false,
      paramsSerializer: [Function: paramsSerializer],
      validateStatus: [Function: validateStatus],
      errorRedactor: [Function: defaultErrorRedactor]
    },
    data: '[{\n' +
      '  "error": {\n' +
      '    "code": 429,\n' +
      '    "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '    "errors": [\n' +
      '      {\n' +
      '        "message": "No capacity available for model gemini-3-flash-preview on the server",\n' +
      '        "domain": "global",\n' +
      '        "reason": "rateLimitExceeded"\n' +
      '      }\n' +
      '    ],\n' +
      '    "status": "RESOURCE_EXHAUSTED",\n' +
      '    "details": [\n' +
      '      {\n' +
      '        "@type": "type.googleapis.com/google.rpc.ErrorInfo",\n' +
      '        "reason": "MODEL_CAPACITY_EXHAUSTED",\n' +
      '        "domain": "cloudcode-pa.googleapis.com",\n' +
      '        "metadata": {\n' +
      '          "model": "gemini-3-flash-preview"\n' +
      '        }\n' +
      '      }\n' +
      '    ]\n' +
      '  }\n' +
      '}\n' +
      ']',
    headers: {
      'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
      'content-length': '630',
      'content-type': 'application/json; charset=UTF-8',
      date: 'Thu, 18 Jun 2026 05:06:45 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1522',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'f29355864320668',
      'x-content-type-options': 'nosniff',
      'x-frame-options': 'SAMEORIGIN',
      'x-xss-protection': '0'
    },
    status: 429,
    statusText: 'Too Many Requests',
    request: {
      responseURL: 'https://cloudcode-pa.googleapis.com/v1internal:streamGenerateContent?alt=sse'
    }
  },
  error: undefined,
  status: 429,
  Symbol(gaxios-gaxios-error): '6.7.1'
}
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M .claude/agents/nutrition-agent.md
 M 01_framework/knowledge/nutrition_reference_kb_v1.md
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/page_generator/rescore_all.py
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-314.md
?? 03_operations/page_generator/_generated_milk.json
?? 03_operations/page_generator/_generated_milk_gates_report.md
?? 03_operations/page_generator/configs/cheese.json
?? 03_operations/page_generator/configs/milk.json
?? 03_operations/page_generator/configs/yogurts.json
?? tasks/TASK-321.md
?? tasks/TASK-321A.md
?? tasks/TASK-321B.md
?? tasks/TASK-321C.md
?? tasks/TASK-321D.md
?? tasks/TASK-321E.md
?? tasks/TASK-321F.md
?? tasks/TASK-321G.md
?? tasks/TASK-321H.md
?? tasks/TASK-321I.md
?? tasks/TASK-322.md
?? tasks/TASK-323.md
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P173_hp_carb_sodium_method.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P200_return.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
?? tasks/scripts/p171_build_exclusions.py
?? tasks/scripts/p171_cheese_scope.py
?? tasks/scripts/p171_cheese_verify.py
?? tasks/scripts/p171_cheese_verify2.py
?? tasks/scripts/p171_cheese_verify3.py
?? tasks/yogurt_copy_audit.txt
?? tasks/yogurt_list.txt
?? terminals/
?? tmp/yogurts_gen_test_final.json
?? yogurts.json
```

### After dispatch

```
M .claude/agents/nutrition-agent.md
 M 01_framework/knowledge/nutrition_reference_kb_v1.md
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/page_generator/rescore_all.py
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-314.md
?? 03_operations/bsip2/proto_v0/reports/methods/
?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
?? 03_operations/page_generator/_generated_milk.json
?? 03_operations/page_generator/_generated_milk_gates_report.md
?? 03_operations/page_generator/configs/cheese.json
?? 03_operations/page_generator/configs/milk.json
?? 03_operations/page_generator/configs/yogurts.json
?? tasks/TASK-321.md
?? tasks/TASK-321A.md
?? tasks/TASK-321B.md
?? tasks/TASK-321C.md
?? tasks/TASK-321D.md
?? tasks/TASK-321E.md
?? tasks/TASK-321F.md
?? tasks/TASK-321G.md
?? tasks/TASK-321H.md
?? tasks/TASK-321I.md
?? tasks/TASK-323.md
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-324.md
?? tasks/closed/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/prompts/_done/P176_additive_burden_index_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P174_return.md
?? tasks/returns/P175_return.md
?? tasks/returns/P176_return.md
?? tasks/returns/P200_return.md
?? tasks/returns/P201_return.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
?? tasks/scripts/p171_build_exclusions.py
?? tasks/scripts/p171_cheese_scope.py
?? tasks/scripts/p171_cheese_verify.py
?? tasks/scripts/p171_cheese_verify2.py
?? tasks/scripts/p171_cheese_verify3.py
?? tasks/yogurt_copy_audit.txt
?? tasks/yogurt_list.txt
?? terminals/
?? tmp/yogurts_gen_test_final.json
?? yogurts.json
```

### Delta

### New / modified since dispatch
  ?? 03_operations/bsip2/proto_v0/reports/methods/
  ?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
  ?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
  ?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
  ?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
  ?? tasks/closed/TASK-322.md
  ?? tasks/closed/TASK-324.md
  ?? tasks/closed/TASK-325.md
  ?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
  ?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
  ?? tasks/prompts/_done/P176_additive_burden_index_method.md
  ?? tasks/returns/P173_return.md
  ?? tasks/returns/P174_return.md
  ?? tasks/returns/P175_return.md
  ?? tasks/returns/P176_return.md
  ?? tasks/returns/P201_return.md
### Removed / cleaned since dispatch
  ?? tasks/TASK-322.md
  ?? tasks/TASK-324.md
  ?? tasks/TASK-325.md
  ?? tasks/prompts/P173_hp_carb_sodium_method.md
