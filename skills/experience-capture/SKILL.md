---
name: experience-capture
description: Turn a verified, reusable problem-solving experience into a project-level Skill after user approval. Use after resolving a non-trivial, non-obvious problem that may recur.
---

# Experience Capture

Use this workflow after solving a difficult problem.

## 1. Decide whether it is reusable

Continue only if the solution is verified, non-obvious, repeatable, and useful in the current project. Do not capture typos, routine errors, one-time fixes, unverified guesses, temporary machine state, or sensitive information.

## 2. Propose the Skill

Inspect `.agents/skills/` for an existing Skill covering the same problem. If one exists, propose updating it instead of creating a duplicate.

Otherwise, prepare a concise proposal with:

- the proposed lowercase hyphenated Skill name;
- the problem and verified root cause;
- the repeatable solution and verification;
- why it is reusable;
- the target path: `.agents/skills/<solution-slug>/SKILL.md`.

Ask the user for approval before creating or modifying any Skill. Do not write the Skill before approval.

## 3. Create and validate

After approval, read and follow:

```text
C:\Users\Witty-Felix\.codex\skills\.system\skill-creator\SKILL.md
```

Use those instructions to create or update the project-level Skill. Keep it narrow, actionable, verified, and free of secrets or unnecessary machine-specific paths. Validate the result, then report the changed path. Do not commit automatically.