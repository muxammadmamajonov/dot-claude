# Support

This is a **template repository** — a `.claude/` operating system you copy into your own projects.
"Support" here means help using and contributing to the template itself. Issues in an application you
*built with* this OS are yours to triage in your own project (the OS gives you the tools —
`.claude/commands/fix-bugs.md`, `.claude/templates/bug-report.md` — to do that).

## Before you ask

Check these first — most questions are already answered:

1. **[START_HERE.md](START_HERE.md)** — a 60-second quick start.
2. **[README.md](README.md)** — full overview, install steps, and the copy-paste prompt for any AI.
3. **[PROJECT_OS.md](PROJECT_OS.md)** — the design philosophy and the full 9-stage flow in depth.
4. **[.claude/CLAUDE.md](.claude/CLAUDE.md)** — the constitution; if the system did something you didn't
   expect, the answer is almost always here.
5. **[examples/](examples/)** — worked project briefs across project types.
6. Run `/self-test` (`.claude/scripts/integrity-check.py` + `validate.py` + `generate_adapters.py --check`) —
   if something feels broken after you customized `.claude/`, this usually finds it.

## Where to get help

- **How do I use / customize this system?** Open a [GitHub Discussion](../../discussions) (or an issue
  tagged `question` if Discussions isn't enabled on this repo) — the maintainers and community answer here.
- **I think I found a bug in the template** (a broken link, a shallow file, a command that contradicts
  the constitution, an adapter out of sync) — open a GitHub issue. Include the output of `/self-test` and
  which file(s) are affected.
- **I want to propose a change** — small additions (a new preset, skill, checklist, agent refinement)
  are a normal PR; anything that changes behavior for every project this template is copied into (a new
  stage, a new agent family, a schema change) is an **RFC** first — see `CONTRIBUTING.md` §11 and
  `.claude/templates/rfc.md`.
- **I found a security issue** (a default that could expose secrets, a hook that could be bypassed to run
  something destructive, a permission-policy gap) — **do not** open a public issue. Follow `SECURITY.md`.
- **Someone violated the Code of Conduct** — follow the reporting instructions in `CODE_OF_CONDUCT.md`,
  not a public issue.

## Response expectations

This is a community-maintained template, not a paid product with an SLA. Maintainers triage issues and
discussions on a best-effort basis. Security reports (`SECURITY.md`) get priority handling; conduct
reports (`CODE_OF_CONDUCT.md`) are handled privately and promptly. Everything else — feature requests,
usage questions, RFCs — is addressed in rough order of received, weighted by how many projects it affects.

## What "support" does not include

- Debugging your own application's code, infrastructure, or business logic. Use the OS's own gates for
  that (`/fix-bugs`, `/audit-security`, `/audit-production`) — that's what they're for.
- Guaranteeing compliance certification outcomes. `.claude/docs/COMPLIANCE.md` is a control-mapping aid,
  not a substitute for your own auditor.
- Running the system on your behalf, hosting it, or providing a managed version. There isn't one — you
  copy `.claude/` into your own repo and it runs entirely inside your own AI coding agent.
