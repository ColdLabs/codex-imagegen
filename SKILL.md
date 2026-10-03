---
name: codex-imagegen
description: Generate or edit images with the `codex-imagegen` CLI (OpenAI gpt-image-2 through the user's own ChatGPT/Codex login, no API key). Use whenever the user asks to generate, draw, create, make, render, or illustrate an image, picture, icon, logo, mockup, illustration, wallpaper or sprite; to edit, modify, or add something to an existing image; to restyle an image or copy the style of another image (style transfer); or to batch-produce several images. Trigger: `/codex-imagegen`.
---

# codex-imagegen

Wraps `codex-imagegen`, pinned to audited commit `bf126f9` of [jdmnk/codex-imagegen-cli](https://github.com/jdmnk/codex-imagegen-cli). It is pure Python (3.10+) and runs on macOS, Linux and Windows. It uses the Codex CLI's ChatGPT login (`$CODEX_HOME/auth.json`, default `~/.codex/auth.json`) and talks only to `chatgpt.com/backend-api/codex` and `auth.openai.com`.

Every image uses the user's ChatGPT plan quota, so don't generate more than asked. An image takes about 20 seconds at low quality, 25 at auto, longer at high, and about 45 seconds with a style reference.

## Setup (check once per session)

Check the tool and the login before the first image:

```bash
codex-imagegen --version && codex-imagegen generate --prompt test --out check.png --dry-run
```

Success prints the version, then the request as JSON with the token redacted, and exits 0. A dry run writes no file, so `check.png` is never created. It reads the auth file but does not refresh the token, so an expired login only shows on the first real generate. To confirm the audited pin: `grep rev= ~/.local/share/uv/tools/codex-imagegen-cli/uv-receipt.toml` (on Windows the receipt is under `%APPDATA%\uv\tools`).

Whenever step 2 or 3 below is needed, the user is setting this up for the first time. Tell them once: this is an unofficial tool that uses the private Codex backend with their ChatGPT login, every image spends their plan quota, and OpenAI may restrict it at any time. See README.md.

If either step fails, fix it in this order and tell the user what you did:

1. **No `uv`:** the user installs it from https://docs.astral.sh/uv/getting-started/installation/ (macOS, Linux and Windows), then reopens the shell.
2. **No `codex-imagegen`:** `uv tool install git+https://github.com/jdmnk/codex-imagegen-cli@bf126f9`
3. **No Codex login** (`Codex auth file not found`): the user needs the Codex CLI (`npm i -g @openai/codex`) and must run `codex login` in their own terminal and choose "Sign in with ChatGPT". In Claude Code they can type `! codex login`. If their Codex home is elsewhere, pass `--codex-home DIR` or `--auth-file FILE`.

## Defaults

- **Output folder:** the session scratchpad directory when the harness provides one (Claude Code lists it in the system prompt), otherwise the current working directory. A path from the user, or an asset that clearly belongs in the project being worked on, wins over both. The scratchpad is temporary, so when the user wants to keep an image, copy it to where they ask or to their Downloads folder. Always report the full path. Name the file after the subject: `fox-in-snow.png`.
- **Paths:** write them with forward slashes and `~` for the home folder. The CLI expands `~` itself on every OS, but the shell may not, so use absolute paths in other shell commands on Windows.
- **Quality:** leave it at `auto`. Use `--quality low` for drafts, tests or "quick" requests, and `--quality high` only when the user asks for high quality or final assets.
- **Format:** PNG. A `.webp` extension on `--out` writes WebP.
- **Never overwrite:** the CLI refuses with `Output already exists`. Check the folder first and pick a free name (`-2`, `-3`). Only pass `--force` when the user asks to replace the file.

## Commands

```bash
# Generate
codex-imagegen generate --prompt "..." --out OUTDIR/NAME.png

# Edit: 1–5 input images, the prompt says what to change
codex-imagegen edit --image in.png --prompt "add a green scarf" --out OUTDIR/NAME.png

# Style transfer: --image is the content, --style-image is the look (prompt optional)
codex-imagegen edit --image photo.png --style-image painting.jpg --out OUTDIR/NAME.png

# Several variations of one prompt: writes NAME-1.png, NAME-2.png ...
codex-imagegen generate --prompt "..." --n 3 --out OUTDIR/NAME.png

# Batch: one job per line, a JSON string or an object
codex-imagegen batch --input jobs.jsonl --out-dir OUTDIR/BATCH
```

Batch `jobs.jsonl` format (an `out` is relative to `--out-dir` and must stay inside it):
```
"a cup of coffee, isometric icon"
{"prompt": "a lighthouse, pixel art", "out": "lighthouse.png"}
{"prompt": "make it night time", "images": ["/abs/path/day.png"], "out": "night.png"}
```

Useful flags:
- `--size WIDTHxHEIGHT`, e.g. `1024x1024` for square, `1536x1024` for landscape or `1024x1536` for portrait. Both sides must be multiples of 16, each edge at most 3840, the aspect ratio between 1:3 and 3:1, and 655,360–8,294,400 pixels in total. The default `auto` lets the backend pick the orientation from the prompt, so pass `--size` whenever the user wants a specific shape, such as a square icon.
- `--background opaque|auto`. Transparent backgrounds aren't supported.
- `--dry-run` prints the request without sending it. Use it to check a command without spending quota.
- `--prompt-file FILE` reads a long prompt from a file.

Allow at least 6 minutes per command (in Claude Code: a 360000 ms Bash timeout). Batch jobs and `--n` greater than 1 take about 30 seconds per image, so scale the timeout to match, or run them in the background.

## Writing the prompt

Expand short requests into a clear prompt: the subject, the medium or style (flat vector, watercolor, photo, pixel art, isometric 3D), the composition or framing, the lighting or mood, and any text that must appear (in quotes). Keep what the user said and don't add objects or characters they didn't mention. Example: "a fox in snow, flat vector" becomes "A small orange fox sitting in snow, flat vector illustration, simple shapes, limited palette of orange, white and pale blue, centered, plain background". For edits, describe only the change and add "keep everything else the same".

## After generating

1. Look at the file with Read to confirm it matches the request. If it clearly misses (wrong subject, garbled required text), say so and offer one retry with a better prompt. Don't retry on your own more than once.
2. Tell the user the full path, the pixel dimensions (the CLI prints them on its `saved` line), and what it shows in one line.
3. For several images, make a contact sheet so the user can compare them at a glance. The script lives next to this file; `SKILL_DIR` is this file's folder:
   ```bash
   uv run --with pillow SKILL_DIR/scripts/contact_sheet.py OUTDIR/contact.jpg a.png b.png c.png
   ```

## Errors

| Message | Fix |
|---|---|
| `Codex auth file not found` / `refresh token not found` / `token refresh failed` | Setup step 3: the user runs `codex login` and chooses ChatGPT. |
| `Output already exists` | Pick a new filename. |
| `HTTP 429` / rate-limited | The CLI already retries (up to about 5 minutes). If it still fails, quota is used up, so stop and tell the user. |
| `Requested WxH, backend returned ...` | This is a warning only. The image is saved at the size the backend chose. |
| `command not found: codex-imagegen` | Setup step 2. On Windows also check that `%USERPROFILE%\.local\bin` is on PATH (`uv tool update-shell`). |

## Installing this skill on another machine

Copy or clone this folder (SKILL.md plus `scripts/`) into the agent's skills directory, for example `~/.claude/skills/codex-imagegen` for Claude Code or `~/.agents/skills/codex-imagegen` for Codex, or symlink one to the other. Then run the Setup section once.

## Updating

Don't upgrade to a newer commit without auditing it first: read `codex_imagegen_cli/cli.py` for new hosts, subprocess calls, or new uses of the token. Then reinstall pinned to the new commit.
