---
name: Skill Development
description: This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive disclosure, or skill development best practices for Claude Code plugins.
version: 0.1.0
---

<!-- source: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md -->
<!-- installed as: skill-creator -->
<!-- installed: 2026-05-31 -->
<!-- bari-agent: All agents (meta-skill) -->

# Skill Development for Claude Code Plugins

This skill provides guidance for creating effective skills for Claude Code plugins.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks.

### What Skills Provide

1. Specialized workflows — Multi-step procedures for specific domains
2. Tool integrations — Instructions for working with specific file formats or APIs
3. Domain expertise — Company-specific knowledge, schemas, business logic
4. Bundled resources — Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (name, description — required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/       — Executable code (Python/Bash/etc.)
    ├── references/    — Documentation loaded into context as needed
    └── assets/        — Files used in output (templates, icons, etc.)
```

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude uses the skill. Be specific about what the skill does and when to use it. Use third-person format: "This skill should be used when..."

### Progressive Disclosure Design Principle

Skills use a three-level loading system:

1. **Metadata (name + description)** — Always in context (~100 words)
2. **SKILL.md body** — When skill triggers (<5k words)
3. **Bundled resources** — As needed by Claude (unlimited)

## Skill Creation Process

### Step 1: Understand the Skill with Concrete Examples

Clarify how the skill will be used before writing anything:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

### Step 2: Plan the Reusable Skill Contents

Analyze each use case to identify what resources are needed:
- Rotating a PDF repeatedly → needs `scripts/rotate_pdf.py`
- Building frontend apps repeatedly → needs `assets/hello-world/` template
- Querying BigQuery repeatedly → needs `references/schema.md`

### Step 3: Create Skill Structure

```bash
mkdir -p skills/skill-name/{references,examples,scripts}
touch skills/skill-name/SKILL.md
```

### Step 4: Edit the Skill

**Writing Style:** Use imperative/infinitive form (verb-first instructions), not second person.

**Correct (imperative):**
```
To create a hook, define the event type.
Configure the MCP server with authentication.
```

**Incorrect (second person):**
```
You should create a hook by defining the event type.
You need to configure the MCP server.
```

**Description (Frontmatter):** Use third-person format with specific trigger phrases:

```yaml
---
name: Skill Name
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", "specific phrase 3".
version: 0.1.0
---
```

**SKILL.md body:** Target 1,500–2,000 words. Move detailed content to `references/`:
- Detailed patterns → `references/patterns.md`
- Advanced techniques → `references/advanced.md`
- Migration guides → `references/migration.md`

### Step 5: Validate and Test

Checklist:
- [ ] SKILL.md has valid YAML frontmatter with `name` and `description`
- [ ] Description uses third person with specific trigger phrases
- [ ] Body uses imperative/infinitive form, not second person
- [ ] SKILL.md is lean (1,500–2,000 words ideal, <5k max)
- [ ] Detailed content moved to `references/`
- [ ] All referenced files exist
- [ ] Scripts are executable and documented
- [ ] Skill triggers on expected user queries

### Step 6: Iterate

After testing the skill on real tasks:
1. Notice struggles or inefficiencies
2. Identify how SKILL.md or bundled resources should be updated
3. Implement changes and test again

**Common improvements:**
- Strengthen trigger phrases in description
- Move long sections from SKILL.md to references/
- Add missing examples or scripts
- Clarify ambiguous instructions

## Skill Contents Guide

### What Goes in SKILL.md (always loaded when skill triggers)
- Core concepts and overview
- Essential procedures and workflows
- Quick reference tables
- Pointers to references/examples/scripts
- Most common use cases

### What Goes in references/ (loaded as needed)
- Detailed patterns and advanced techniques
- Comprehensive API documentation
- Edge cases and troubleshooting
- Extensive examples and walkthroughs

### What Goes in examples/ (working code examples)
- Complete, runnable scripts
- Configuration files
- Template files

### What Goes in scripts/ (utility scripts)
- Validation tools
- Testing helpers
- Automation scripts

## Common Mistakes to Avoid

### Weak Trigger Description

```yaml
# Bad — vague, no specific trigger phrases, not third person
description: Provides guidance for working with hooks.

# Good — third person, specific phrases, concrete scenarios
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events.
```

### Too Much in SKILL.md

```
# Bad
skill-name/
└── SKILL.md  (8,000 words)

# Good
skill-name/
├── SKILL.md  (1,800 words — core essentials)
└── references/
    ├── patterns.md (2,500 words)
    └── advanced.md (3,700 words)
```

### Missing Resource References

Always reference supporting files in SKILL.md so Claude knows they exist:

```markdown
## Additional Resources
- **`references/patterns.md`** — Detailed patterns
- **`references/advanced.md`** — Advanced techniques
```

## Quick Reference: Skill Structures

### Minimal Skill
```
skill-name/
└── SKILL.md
```

### Standard Skill (Recommended)
```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

### Complete Skill
```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   └── example1.sh
└── scripts/
    └── validate.sh
```

## Bari-Specific Notes

- All Bari skills (internal and third-party) live in `C:\Bari\.claude\skills\`
- Internal Bari skills live in `C:\Bari\.claude\skills\bari-*/SKILL.md`
- Third-party skills live in `C:\Bari\.claude\skills\third_party\`
- Any new skill created by this skill must be reviewed by the designated owner before use
- Update `C:\Bari\.claude\skills\third_party\skill_registry.md` after creating any new skill
- Bari skill naming convention: kebab-case, descriptive, prefixed with `bari-` for internal skills
