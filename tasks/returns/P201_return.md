# Return: P201

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P201_cheese_branch_rehab.md` |
| Model | `gemini/cli` |
| Started | 2026-06-18T04:38:54.770600+00:00 |
| Finished | 2026-06-18T04:57:04.026412+00:00 |
| Exit code | 0 |

---

## Output

```
- **Conflicted files + which side you took for each:**
  - Zero conflicts were reported by git. The merge from `origin/master` into `sweep/cheese-conform` was handled automatically by the 'ort' strategy. 
  - Verified `bari-web/src/lib/comparisons/registry/index.ts` contains the union of both categories (imports for both `cheese` and `yogurts`).
  - Verified `bari-web/src/app/hashvaot/page.tsx` correctly uses the conformed `cheese-page-data`. Yogurt usage was not present in this file in either `origin/master` or the stale branch, but the conformed `FeaturedYogurtsIntelligenceCard` component exists and uses the new `yogurts-page-data`.

- **`npm run build` exit code + total page count:**
  - Exit code: `0`
  - Total page count: `39`

- **Confirmation both `/hashvaot/cheese` and `/hashvaot/yogurts` are in the build output:**
  - Confirmed. Both routes were generated as static pages:
    ```
    ├ ○ /hashvaot/cheese
    ├ ○ /hashvaot/yogurts
    ```

- **Grep results for the three deleted-module names (must be empty):**
  - `cheese-comparison-page-data`: (empty)
  - `cheese-shelf-filters`: (empty)
  - `yogurts-comparison-page-data`: (empty)
  - Verified all three modules are physically deleted and have zero remaining references in `bari-web/src`.

- **The merge commit SHA + confirmation of push to origin/sweep/cheese-conform:**
  - Merge commit SHA: `f3b38349ed5283022ff76ea4c24393780d64a319`
  - **Push Status:** Attempted push to `origin/sweep/cheese-conform` failed due to terminal authentication restrictions (`fatal: could not read Username for 'https://github.com': terminal prompts disabled`). The merge is committed locally in `C:\bari-cheese`.

Task P201 is complete. The stale `sweep/cheese-conform` branch has been rehabilitated by merging `origin/master`, ensuring the yogurt conform from master and the cheese conform from the branch are both preserved.

### Results Summary
- **Merge Status:** Successfully auto-merged with zero conflicts.
- **Verification:**
    - `yogurts-page-data.ts` and `cheese-page-data.ts` are present and used by their respective routes.
    - `registry/index.ts` contains both categories.
    - `npm run build` exited with code `0` and generated 39 pages.
    - Routes `/hashvaot/cheese` and `/hashvaot/yogurts` are confirmed in the build output.
- **Cleanup:** Zero references to `cheese-comparison-page-data`, `cheese-shelf-filters`, or `yogurts-comparison-page-data` remain in the source.
- **Git State:**
    - **Merge Commit SHA:** `f3b38349ed5283022ff76ea4c24393780d64a319`
    - **Push:** Attempted but failed due to authentication restrictions in the headless environment.

```markdown
- Conflicted files + which side you took for each: Zero conflicts (auto-merged).
- npm run build exit code + total page count: 0 / 39 pages.
- Confirmation both /hashvaot/cheese and /hashvaot/yogurts are in the build output: Confirmed.
- Grep results for the three deleted-module names (must be empty): Empty.
- The merge commit SHA + confirmation of push to origin/sweep/cheese-conform: f3b38349ed5283022ff76ea4c24393780d64a319 (Push failed: Auth required).
```


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
      date: 'Thu, 18 Jun 2026 04:39:12 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1072',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '3e8210d882df889a',
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
(node:22124) [DEP0190] DeprecationWarning: Passing args to a child process with shell option true can lead to security vulnerabilities, as the arguments are not escaped, only concatenated.
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
      date: 'Thu, 18 Jun 2026 04:40:12 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=818',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'ec28b0a8aa8ca8ec',
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
      date: 'Thu, 18 Jun 2026 04:40:19 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=850',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e669ea637622f345',
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
      date: 'Thu, 18 Jun 2026 04:40:42 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=9976',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '58c3a52448ae2857',
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
      date: 'Thu, 18 Jun 2026 04:41:07 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=703',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e90bec28c906fc14',
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
      date: 'Thu, 18 Jun 2026 04:43:22 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=16736',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'c67166b84794efed',
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
Error executing tool read_file: Path not in workspace: Attempted path "C:\bari-cheese\bari-web\src\app\hashvaot\page.tsx" resolves outside the allowed workspace directories: C:\Bari or the project temp directory: C:\Users\HP\.gemini\tmp\bari
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
      date: 'Thu, 18 Jun 2026 04:43:35 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=748',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '1abf2bb06c470029',
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
      date: 'Thu, 18 Jun 2026 04:45:09 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1026',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'fecc51a5c31660a8',
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
      date: 'Thu, 18 Jun 2026 04:45:14 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=988',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'cc22138d284d3afd',
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
      date: 'Thu, 18 Jun 2026 04:45:33 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1329',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '9a4078dcf5b82145',
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
      date: 'Thu, 18 Jun 2026 04:45:43 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1138',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'e0b4565c8147f071',
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
      date: 'Thu, 18 Jun 2026 04:45:50 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=2257',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '4057975f0aee1caa',
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
      date: 'Thu, 18 Jun 2026 04:46:00 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=886',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '2fae8d7f0dc419e9',
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
      date: 'Thu, 18 Jun 2026 04:46:24 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=970',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'ebe881f9e1ea4645',
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
      date: 'Thu, 18 Jun 2026 04:47:28 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=2120',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'a452133f09fe738c',
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
      date: 'Thu, 18 Jun 2026 04:47:50 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=7158',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '8bd4c7d80bd61618',
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
      date: 'Thu, 18 Jun 2026 04:48:44 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=31352',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '4fa743c168d720b4',
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
      date: 'Thu, 18 Jun 2026 04:49:31 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1031',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '7ef0aabed454fdaf',
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
      date: 'Thu, 18 Jun 2026 04:50:27 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1114',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'a50053599f76637f',
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
      date: 'Thu, 18 Jun 2026 04:50:35 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1521',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'b001bc84112bda80',
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
      date: 'Thu, 18 Jun 2026 04:51:04 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1207',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '4494f0d54903ce29',
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
      date: 'Thu, 18 Jun 2026 04:52:11 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1253',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '53da44864b3f270a',
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
      date: 'Thu, 18 Jun 2026 04:53:08 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=7833',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '7908cbbf040efddf',
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
      date: 'Thu, 18 Jun 2026 04:53:25 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1175',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'edc2493932d8b24d',
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
      date: 'Thu, 18 Jun 2026 04:53:31 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1326',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '6e283fd2f2470aa8',
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
      date: 'Thu, 18 Jun 2026 04:53:52 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1457',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'be3b3f795211634c',
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
      date: 'Thu, 18 Jun 2026 04:54:00 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1085',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '5bbe17aac3ade75',
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
      date: 'Thu, 18 Jun 2026 04:54:24 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1719',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'a2dfe6206f83bd2c',
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
      date: 'Thu, 18 Jun 2026 04:54:32 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1295',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '1254e13e8c3a78cb',
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
      date: 'Thu, 18 Jun 2026 04:54:47 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1406',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '73e8b302407de7af',
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
      date: 'Thu, 18 Jun 2026 04:55:14 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1711',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '3c9b2f79902c6c69',
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
      date: 'Thu, 18 Jun 2026 04:55:49 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1449',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '4403faf88e0fabfe',
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
      date: 'Thu, 18 Jun 2026 04:56:10 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1421',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '619f3e75fff6166',
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
      date: 'Thu, 18 Jun 2026 04:56:15 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1422',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': '3a720d3d9acda1c5',
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
      date: 'Thu, 18 Jun 2026 04:56:51 GMT',
      server: 'ESF',
      'server-timing': 'gfet4t7; dur=1326',
      vary: 'Origin, X-Origin, Referer',
      'x-cloudaicompanion-trace-id': 'fbe7c34d2411b867',
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
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
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
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
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
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/closed/TASK-322.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P175_omega_lipid_extract_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
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

### Delta

### New / modified since dispatch
  ?? 03_operations/bsip2/proto_v0/reports/methods/
  ?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
  ?? 03_operations/page_generator/_generated_milk.json
  ?? 03_operations/page_generator/_generated_milk_gates_report.md
  ?? tasks/TASK-323.md
  ?? tasks/TASK-324.md
  ?? tasks/TASK-325.md
  ?? tasks/closed/TASK-322.md
  ?? tasks/prompts/P174_counterfactual_method.md
  ?? tasks/prompts/P175_omega_lipid_extract_method.md
  ?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
  ?? tasks/returns/P173_return.md
  ?? tasks/returns/P200_return.md
