# codex-imagegen

An agent skill that generates and edits images through [codex-imagegen-cli](https://github.com/jdmnk/codex-imagegen-cli), using your own ChatGPT/Codex login (model `gpt-image-2`). No API key. Works with Claude Code, Codex and any agent that reads `SKILL.md`.

## Before you use this

- **Unofficial.** The CLI talks to the private backend that the Codex app uses, with your own ChatGPT login. OpenAI does not document or support this and may restrict it at any time. Use at your own risk.
- **Every image uses your ChatGPT plan quota.**
- **Third-party code reads your Codex auth file.** The CLI is pinned to commit [`bf126f9`](https://github.com/jdmnk/codex-imagegen-cli/tree/bf126f9), which was reviewed before pinning. Audit the diff before changing the pin.
- Not affiliated with OpenAI or the CLI author. Apache-2.0.

## Install

Requires Python 3.10+, [uv](https://docs.astral.sh/uv/) and the [Codex CLI](https://github.com/openai/codex) logged in with ChatGPT (`codex login`).

```bash
uv tool install git+https://github.com/jdmnk/codex-imagegen-cli@bf126f9
```

Then put this folder in your agent's skills directory:

| Agent | Path |
|---|---|
| Claude Code | `~/.claude/skills/codex-imagegen` |
| Codex | `~/.agents/skills/codex-imagegen` |

Or symlink one path to the other if you use both agents. Or with the skills CLI: `npx skills add coldlabs/codex-imagegen`.

Runs on macOS, Linux and Windows. The agent runs the Setup check in `SKILL.md` at the start of a session and tells you what is missing.

## Use

Ask the agent to generate, edit or restyle an image, or type `/codex-imagegen`. Images land in the session folder or the current directory unless you give a path. `scripts/contact_sheet.py` builds a side-by-side preview when several images are made.
