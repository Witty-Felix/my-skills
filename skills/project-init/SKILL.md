---
name: project-init
description: Initialize any project with CodeGraph and connect the global experience-capture workflow to the project AGENTS.md. Use at the start of work in a project.
---

# Project Init

Perform these two steps at the project root.

## 1. Initialize CodeGraph

If `.codegraph` does not exist, run:

```powershell
codegraph init
```

If `.codegraph` already exists, skip this step. Do not manually start `codegraph serve --mcp`.

## 2. Connect experience capture

Ensure the project `AGENTS.md` contains this rule:

```md
## Experience Capture

After resolving a non-trivial, reusable problem, invoke the global `experience-capture` Skill. The Skill must obtain user approval before creating a new project-level Skill.
```

Create `AGENTS.md` if it does not exist. Do not duplicate this rule or modify unrelated content.