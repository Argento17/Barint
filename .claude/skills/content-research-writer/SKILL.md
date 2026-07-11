---
name: content-research-writer
description: Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on each section. Transforms your writing process from solo effort to collaborative partnership.
---

<!-- source: https://github.com/ComposioHQ/awesome-claude-skills/blob/master/content-research-writer/SKILL.md -->
<!-- installed: 2026-05-31 -->
<!-- bari-agent: Research Analyst, Head of Product, Chief Nutrition Officer -->

# Content Research Writer

This skill acts as your writing partner, helping you research, outline, draft, and refine content while maintaining your unique voice and style.

## When to Use This Skill

- Writing blog posts, articles, or newsletters
- Creating educational content or tutorials
- Drafting thought leadership pieces
- Researching and writing case studies
- Producing technical documentation with sources
- Writing with proper citations and references
- Improving hooks and introductions
- Getting section-by-section feedback while writing

## What This Skill Does

1. **Collaborative Outlining**: Helps you structure ideas into coherent outlines
2. **Research Assistance**: Finds relevant information and adds citations
3. **Hook Improvement**: Strengthens your opening to capture attention
4. **Section Feedback**: Reviews each section as you write
5. **Voice Preservation**: Maintains your writing style and tone
6. **Citation Management**: Adds and formats references properly
7. **Iterative Refinement**: Helps you improve through multiple drafts

## Basic Workflow

1. **Start with an outline**: "Help me create an outline for an article about [topic]"
2. **Research and add citations**: "Research [specific topic] and add citations to my outline"
3. **Improve the hook**: "Here's my introduction. Help me make the hook more compelling."
4. **Get section feedback**: "I just finished the [section]. Review it and give feedback."
5. **Refine and polish**: "Review the full draft for flow, clarity, and consistency."

## Instructions

### 1. Understand the Writing Project

Ask clarifying questions:
- What's the topic and main argument?
- Who's the target audience?
- What's the desired length/format?
- What's your goal? (educate, persuade, entertain, explain)
- Any existing research or sources to include?
- What's your writing style? (formal, conversational, technical)

### 2. Collaborative Outlining

Help structure the content:

```markdown
# Article Outline: [Title]

## Hook
- [Opening line/story/statistic]
- [Why reader should care]

## Introduction
- Context and background
- Problem statement
- What this article covers

## Main Sections

### Section 1: [Title]
- Key point A
- Key point B
- Example/evidence
- [Research needed: specific topic]

### Section 2: [Title]
- Key point C
- Key point D
- Data/citation needed

## Conclusion
- Summary of main points
- Call to action
- Final thought

## Research To-Do
- [ ] Find data on [topic]
- [ ] Get examples of [concept]
- [ ] Source citation for [claim]
```

### 3. Conduct Research

When user requests research on a topic:
- Search for relevant information
- Find credible sources
- Extract key facts, quotes, and data
- Add citations in requested format

Example output:
```markdown
## Research: [Topic]

Key Findings:

1. **Finding A**: [Summary] [1]
2. **Finding B**: [Summary] [2]
3. **Expert Quote**: "[Quote]" - [Attribution] [3]

Citations:
[1] [Author]. ([Year]). "[Title]". [Publication]
[2] [Author]. ([Year]). "[Title]". [Publication]
[3] [Author]. ([Year]). [Source]
```

### 4. Improve Hooks

When user shares an introduction, analyze and strengthen:

**Current Hook Analysis**:
- What works: [positive elements]
- What could be stronger: [areas for improvement]
- Emotional impact: [current vs. potential]

**Suggested Alternatives**:
- Option 1 (Bold statement): [Example] — *Why it works: [explanation]*
- Option 2 (Personal story): [Example] — *Why it works: [explanation]*
- Option 3 (Surprising data): [Example] — *Why it works: [explanation]*

### 5. Provide Section-by-Section Feedback

```markdown
# Feedback: [Section Name]

## What Works Well
- [Strength 1]
- [Strength 2]

## Suggestions for Improvement

### Clarity
- [Specific issue] → [Suggested fix]

### Flow
- [Transition issue] → [Better connection]

### Evidence
- [Claim needing support] → [Add citation or example]

## Specific Line Edits

Original:
> [Exact quote from draft]

Suggested:
> [Improved version]

Why: [Explanation]
```

### 6. Preserve Writer's Voice

- Learn their style by reading existing writing samples
- Suggest, don't replace: offer options, not directives
- Match tone: formal, casual, technical, friendly
- Ask periodically: "Does this sound like you?"

### 7. Citation Management

Handle references based on user preference:

**Inline**: `Studies show 40% productivity improvement (McKinsey, 2024).`

**Numbered**: `Studies show 40% productivity improvement [1].`

Maintain a running references list at the end of the document.

### 8. Final Review and Polish

```markdown
# Full Draft Review

## Overall Assessment
**Strengths**: [List]
**Impact**: [Overall effectiveness assessment]

## Structure & Flow
- [Comments on organization]
- [Transition quality]

## Content Quality
- [Argument strength]
- [Evidence sufficiency]

## Pre-Publish Checklist
- [ ] All claims sourced
- [ ] Citations formatted
- [ ] Examples clear
- [ ] Transitions smooth
- [ ] Call to action present
- [ ] Proofread for typos
```

## Writing Workflows

### Blog Post Workflow
1. Outline together
2. Research key points
3. Write introduction → get feedback
4. Write body sections → feedback each
5. Write conclusion → final review
6. Polish and edit

### Technical Tutorial Workflow
1. Outline steps
2. Write code examples
3. Add explanations
4. Test instructions
5. Add troubleshooting section
6. Final review for accuracy

### Thought Leadership Workflow
1. Brainstorm unique angle
2. Research existing perspectives
3. Develop your thesis
4. Write with strong POV
5. Add supporting evidence
6. Craft compelling conclusion

## File Organization

Recommended structure for writing projects:

```
writing/article-name/
├── outline.md
├── research.md
├── draft-v1.md
├── draft-v2.md
├── final.md
└── sources/
    ├── study1.pdf
    └── article2.md
```

## Best Practices

### For Research
- Verify sources before citing
- Use recent data when possible
- Balance different perspectives
- Link to original sources

### For Voice
- Share examples of your writing
- Specify tone preferences
- Point out good matches: "That sounds like me!"
- Flag mismatches: "Too formal for my style"

## Bari-Specific Notes

- Use for writing category page introductions, comparison criteria descriptions, and product context copy
- Research phase should include checking Bari's label registry for approved attribute language before writing
- All copy destined for the live Bari website must go through the category team review, not directly from this skill's output
- For marketing promotional copy, use the `marketing/copywriting` skill instead
