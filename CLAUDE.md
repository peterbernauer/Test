# CLAUDE.md

This file provides guidance to AI assistants (Claude and others) working in this repository.

## Repository Overview

This is a new, empty repository. As the project grows, update this file to reflect the actual codebase structure, conventions, and workflows.

**Repository**: peterbernauer/Test
**Remote**: Configured at `http://local_proxy@127.0.0.1:60135/git/peterbernauer/Test`

---

## Git Workflow

### Branch Naming

- Feature branches: `feature/<short-description>`
- Bug fixes: `fix/<short-description>`
- Claude-generated branches: `claude/<session-id>` (managed automatically)

### Commit Conventions

Use clear, imperative commit messages:

```
Add user authentication module
Fix null pointer in payment handler
Refactor database connection pooling
```

Avoid vague messages like "fix stuff" or "WIP".

### Pushing Changes

Always push with tracking:

```bash
git push -u origin <branch-name>
```

If the push fails due to network errors, retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s).

---

## Development Guidelines for AI Assistants

### Before Making Changes

1. **Read before editing** — always read a file before modifying it.
2. **Understand the context** — explore surrounding files to understand patterns and conventions.
3. **Prefer editing over creating** — modify existing files rather than creating new ones unless strictly necessary.

### Code Quality

- Keep solutions minimal and focused — only make changes directly requested or clearly necessary.
- Do not add docstrings, comments, or type annotations to code you didn't change.
- Do not refactor or "clean up" surrounding code when fixing a bug or adding a feature.
- Avoid premature abstractions — three similar lines of code is better than an unnecessary helper.
- Do not add error handling for scenarios that cannot happen in practice.
- Trust framework guarantees; only validate at system boundaries (user input, external APIs).

### Security

- Never introduce SQL injection, XSS, command injection, or other OWASP Top 10 vulnerabilities.
- Do not commit secrets, credentials, or `.env` files.
- Do not skip commit hooks (`--no-verify`) unless explicitly instructed.

### File Management

- Do not create documentation files (`.md`, `README`) unless explicitly requested.
- Do not create backup files or leave commented-out dead code.
- Remove unused imports and variables.

---

## Testing

> Update this section once a test framework is established.

When a test suite exists:

- Run tests before and after changes to confirm nothing regresses.
- Do not mark a task complete if tests are failing.
- Add tests only when explicitly requested or when the change clearly requires them.

---

## Project Structure

> This section will be populated as the project develops.

Once source files are added, document the layout here:

```
<project-root>/
├── src/          # Source code
├── tests/        # Test files
└── CLAUDE.md     # This file
```

---

## Updating This File

When the project evolves, keep this file current:

- Add a **Project Structure** section once directories are established.
- Document the **build/run commands** once a tech stack is chosen.
- Add **language/framework-specific conventions** as they emerge.
- Record any **non-obvious decisions** so future contributors (human or AI) understand the reasoning.
