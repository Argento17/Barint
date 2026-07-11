---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

<!-- source: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines -->
<!-- installed: 2026-05-31 -->
<!-- version: 1.0.0 -->
<!-- security note: this skill makes an external WebFetch call to retrieve guidelines at runtime — see Bari security notes below -->

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Bari Security Notes

This skill fetches external content from `github.com/vercel-labs/web-interface-guidelines` at runtime.
- Approved for use on Bari frontend files only
- Do not run against files outside the Bari project directory
- If the external URL becomes unavailable, skip this skill and use `bari-frontend-ui` instead
