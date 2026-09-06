---
name: lilynova
description: Use when working with the LilyNova ecosystem. Create/inspect/run projects, manage files, start servers, scaffold templates, manage Timebreaker/PureLily/Cookie Run/Hermes workspaces, explain errors, run safe builds. Never delete/overwrite without confirmation.
---

# LilyNova Skill

Modular skill for the LilyNova creative + developer ecosystem. Lives at `~/Projects/lilynova/`.

## When to use

Use this skill when the user wants to:
- Create, inspect, or run a LilyNova project
- Scaffold a new project (TypeScript + React + Tailwind, or any template in `templates/`)
- Start/stop a dev server
- Manage files inside a project (read, write, list)
- Show project status / workspace metadata
- Work on a Timebreaker, PureLily, Cookie Run, or Hermes sub-project
- Run safe build/test commands
- Explain build/runtime errors
- Maintain clean project structure

## Where things live

```
~/Projects/lilynova/
├── index.html              # Dashboard
├── src/app.js              # Frontend logic (modular)
├── skills/lilynova/SKILL.md
├── templates/              # Project templates
│   ├── ts-react-tailwind/
│   ├── purelily-static/
│   └── timebreaker/
├── docs/                   # Architecture, API, integration notes
└── package.json            # Ecosystem metadata
```

The existing Hermes Agent dashboard at `~/hermes-webui` and `~/.hermes/hermes-agent` is **preserved** — LilyNova is a new project, not a replacement.

## Operations

1. **Create a project** — `LN_TEMPLATE=<name> LN_NAME=<project> bash ~/Projects/lilynova/scripts/new.sh`
2. **Inspect a project** — list files, package.json, read structure
3. **Run dev task** — `npm run dev` / `npm run build` / `npm test`
4. **Start a server** — background, with a unique port
5. **Stop a server** — kill the PID
6. **Scaffold from template** — copy `templates/<name>/` to `~/Projects/<new-project>/`
7. **Explain error** — read the stacktrace, suggest a fix
8. **Show status** — list projects, recent activity, system info

## Safety rules (MUST follow)

1. **NEVER delete a project or file without explicit confirmation** — show the path first, ask `Confirm? y/n`.
2. **NEVER overwrite an existing project** — check if target dir exists, ask before clobbering.
3. **Destructive commands** (`rm`, `rm -rf`, `mv` over a dir, `git reset --hard`) — print the exact command and ask before running.
4. **No secrets in source** — never write API keys, tokens, or passwords into files; use `~/.lilynova/.env` and `.gitignore` it.
5. **No secrets in logs** — mask anything that looks like a key (`sk-...`, `ghp_...`, `xoxb-...`).
6. **Long-running servers** — background them, never block; return the PID and port.
7. **Confirm before scaffolding into a non-empty directory** — list existing files first.

## Project metadata

All projects use a `lilynova.json` at the root:

```json
{
  "name": "project-name",
  "template": "ts-react-tailwind",
  "created": "2026-09-02",
  "tags": ["creative", "web"],
  "favorite": false
}
```

Store projects at `~/Projects/lilynova-projects/<name>/` by default; allow override via `LN_ROOT`.

## Common tasks

### Scaffold a new project
```bash
LN_NAME=myapp LN_TEMPLATE=ts-react-tailwind bash ~/Projects/lilynova/scripts/new.sh
```
Result: `~/Projects/lilynova-projects/myapp/` with `lilynova.json` and template files.

### List projects
```bash
ls ~/Projects/lilynova-projects/ 2>/dev/null || echo "no projects yet"
```

### Run a project's dev script
```bash
cd ~/Projects/lilynova-projects/<name> && npm run dev
```

### Start dashboard
The dashboard is `~/Projects/lilynova/index.html` — open with any browser; no server required for static view.

## Templates available

- `ts-react-tailwind` — TypeScript + React + Tailwind + Vite
- `purelily-static` — Static HTML/CSS/JS with PureLily theme tokens
- `timebreaker` — Timebreaker language starter (placeholder; expand as language matures)
- `crk-fan` — Cookie Run fan project (no proprietary assets; original art/text only)

## Integration with Hermes

The dashboard links to the existing Hermes Agent skill. Do not duplicate or replace Hermes — LilyNova is a *complement*. If user asks for "Hermes", default to the `hermes-agent` skill; only route to `lilynova` when the request is about LilyNova projects specifically.

## Verification checklist

Before declaring a task done:
1. The project files actually exist (`ls` the path).
2. The dev server (if started) responds (`curl` the port).
3. No secrets leaked into the committed files.
4. The `lilynova.json` is valid JSON and present.
