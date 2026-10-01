# Git Workflow — Baseline Before Phase 3

## Recommended repository state

This commit represents:

**Phase 2 complete / Phase 3 not yet implemented**

Recommended commit message:

`docs: freeze phase 2 architecture baseline before phase 3`

## Commands

```bash
git status
git add .
git commit -m "docs: freeze phase 2 architecture baseline before phase 3"
git tag phase-2-baseline
git status
```

Then Phase 3 work can begin from this clean baseline.

## Important

Do not commit:

- `.env`
- passwords
- API keys
- payment credentials
- database dumps containing sensitive data
- local virtual environments
- `node_modules`
- generated runtime data
