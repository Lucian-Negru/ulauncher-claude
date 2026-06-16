# Ulauncher Claude Plugin

A fast, keyboard-driven launcher for opening [Claude Code](https://claude.com/claude-code) in different repositories.

## Features

- **Quick repo switching** — Type `claude` + repo name to launch Claude Code in that directory
- **Fuzzy matching** — Supports prefix, substring, and subsequence matching
- **Configurable** — Customize the keyword, repositories directory, and terminal
- **No dependencies** — Works with any terminal and Claude Code setup

## Installation

### Prerequisites

- [Ulauncher](https://ulauncher.io/) v2.0 or later
- Claude Code CLI installed
- Repositories organized in a single directory (default: `~/repos`)

### Add the extension

1. Open Ulauncher preferences (click the gear icon, or right-click the Ulauncher window)
2. Go to the **Extensions** tab
3. Click **Add extension**
4. Paste the repository URL and confirm:

```
https://github.com/Lucian-Negru/ulauncher-claude
```

Ulauncher downloads the extension and loads it automatically. Open Ulauncher and type `claude` to see your repositories.

To update later, open the same **Extensions** tab and click the update button for the extension.

## Configuration

Open Ulauncher preferences and configure:

- **Claude repo** (keyword) — The trigger keyword, default `claude`
- **Repositories directory** — Where your repos are stored, default `~/repos`. Accepts a comma-separated list to search multiple roots (e.g. `~/work, ~/personal`); each root gets its own launch entry, and the full path is shown so same-named repos stay distinct
- **Terminal** — Terminal emulator used to open Claude Code, default `x-terminal-emulator` (the system default terminal)
- **Results shown** — Maximum number of results to display, default `8`

## Usage

### Basic Usage

1. Press `Ctrl+Space` (or your Ulauncher hotkey)
2. Type `claude` to see all repositories
3. Type `claude <name>` to filter (e.g., `claude myproject`)
4. Press `Enter` to open Claude Code in that repository

### Matching Behavior

The plugin supports three types of matching:

- **Prefix match** (best) — `proj` matches `projectname`
- **Substring match** (good) — `ject` matches `projectname`
- **Subsequence match** (fallback) — `pjn` matches `projectname`

Results are sorted by match quality, so best matches appear first.

### Root Directory

When you just type `claude` with no argument, the top results open Claude in your repositories root directories — one entry per configured root (the **Repositories directory** preference, default `~/repos`).

## Launcher Script

The plugin always uses the `claude-repo.sh` script bundled with the extension — there is no preference to point it elsewhere. It ships executable, so no setup is needed after installing.

The terminal is chosen via the **Terminal** preference (passed to the script as the `TERMINAL` environment variable) and defaults to the system default terminal (`x-terminal-emulator`). The script knows how to invoke common terminals with the correct working-directory and command flags. Where the terminal supports tabs, Claude opens in a **new tab of the active window**:

- `ptyxis` / `x-terminal-emulator` / `gnome-terminal` — new tab (`--tab`)
- `konsole` — new tab (`--new-tab`)
- `kitty` — new window
- `wezterm` — new window
- `alacritty`, `xterm`, `xfce4-terminal`, and other `-e`-style terminals — new window (fallback)

### Customization

The script is invoked with the absolute directory to open as its first argument (the extension builds it from the **Repositories directory** preference), so the repos location is configured there — not in the script. For terminals the script doesn't recognize, or to add environment setup, edit `claude-repo.sh` inside the installed extension directory (`~/.local/share/ulauncher/extensions/<extension-id>/`):
- **Add a terminal**: Add a `case` branch with the terminal's working-directory and command flags
- **Add environment setup**: Insert any environment variables or startup commands before the `exec` line

## Troubleshooting

### "No repositories found"

- Check that the **Repositories directory** preference points to the correct location
- Ensure repositories are direct subdirectories (not nested deeper)
- Verify the directory exists and you have read permissions

### Claude Code doesn't launch

- Run the bundled launcher script manually to test: `./claude-repo.sh <absolute-directory>`
- Verify that Claude Code CLI is installed and available in your PATH

### Plugin doesn't appear in Ulauncher

- Confirm the extension is listed under Ulauncher preferences → **Extensions**; re-add the URL if it isn't
- Check that the extension downloaded correctly:
  ```bash
  ls ~/.local/share/ulauncher/extensions/
  ```
- Restart Ulauncher completely
- Check Ulauncher logs in `~/.local/share/ulauncher/logs/`

## Development

### Project Structure

```
.
├── main.py            # Plugin logic
├── manifest.json      # Plugin metadata
├── versions.json      # API version compatibility
├── claude-repo.sh     # Launcher script (bundled, terminal-aware)
├── images/
│   └── icon.jpg       # Plugin icon
├── LICENSE            # MIT license
└── README.md          # This file
```

### Debugging

Enable debug logging in Ulauncher preferences, then check logs:
```bash
tail -f ~/.local/share/ulauncher/logs/ulauncher.log
```

## Contributing

Found a bug or want to improve the plugin? PRs welcome! Some ideas:

- Support for nested repository directories
- Recent repositories tracking

## License

MIT
