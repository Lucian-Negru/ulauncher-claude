# Ulauncher Claude Plugin

A fast, keyboard-driven launcher for opening [Claude Code](https://claude.com/claude-code) in different repositories.

## Features

- **Quick repo switching** — Type `claude` + repo name to launch Claude Code in that directory
- **Fuzzy matching** — Supports prefix, substring, and subsequence matching
- **Configurable** — Customize the keyword, repositories directory, and launcher script
- **No dependencies** — Works with any terminal and Claude Code setup

## Installation

### Prerequisites

- [Ulauncher](https://ulauncher.io/) v2.0 or later
- Claude Code CLI installed
- Repositories organized in a single directory (default: `~/repos`)

### Quick Setup

1. Clone this repository into Ulauncher's extensions directory:

```bash
git clone https://github.com/YOUR-USERNAME/ulauncher-claude.git \
  ~/.local/share/ulauncher/extensions/com.github.YOUR-USERNAME.claude
```

2. Restart Ulauncher (or press `Ctrl+L` to reload)

3. Open Ulauncher and type `claude` to see available repositories

### Manual Setup

If you prefer to set it up manually:

1. Create the extension directory:
```bash
mkdir -p ~/.local/share/ulauncher/extensions/com.github.YOUR-USERNAME.claude
```

2. Copy the plugin files:
```bash
cp -r . ~/.local/share/ulauncher/extensions/com.github.YOUR-USERNAME.claude/
```

3. Restart Ulauncher

## Configuration

Open Ulauncher preferences and configure:

- **Claude repo** (keyword) — The trigger keyword, default `claude`
- **Repositories directory** — Where your repos are stored, default `~/repos`
- **Launcher script** — Script to open Claude in a directory, default `~/.local/bin/claude-repo`
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

When you just type `claude` with no argument, the first result opens Claude in your repositories root directory (`~/repos`).

## Launcher Script

The plugin uses a launcher script to open Claude. By default, it expects `~/.local/bin/claude-repo`.

Example script:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ] || [ -z "$1" ]; then
    dir="$HOME/repos"
else
    dir="$HOME/repos/$1"
fi

if [ ! -d "$dir" ]; then
    notify-send "claude-repo" "Repository not found: $dir" 2>/dev/null || true
    exit 1
fi

# Customize this to your preferred terminal and setup
exec alacritty --working-directory "$dir" -e "$HOME/.local/bin/claude"
```

You can customize this script to use your preferred terminal (Kitty, WezTerm, GNOME Terminal, etc.) and any additional environment setup you need.

## Troubleshooting

### "No repositories found"

- Check that the **Repositories directory** preference points to the correct location
- Ensure repositories are direct subdirectories (not nested deeper)
- Verify the directory exists and you have read permissions

### Claude Code doesn't launch

- Check that the **Launcher script** exists and is executable
- Run the launcher script manually to test: `~/.local/bin/claude-repo <repo-name>`
- Verify that Claude Code CLI is installed and available in your PATH

### Plugin doesn't appear in Ulauncher

- Check that the extension is installed in the correct location:
  ```bash
  ls ~/.local/share/ulauncher/extensions/com.github.YOUR-USERNAME.claude
  ```
- Restart Ulauncher completely
- Check Ulauncher logs in `~/.local/share/ulauncher/logs/`

## Development

### Project Structure

```
.
├── main.py           # Plugin logic
├── manifest.json     # Plugin metadata
├── versions.json     # API version compatibility
├── images/
│   └── icon.jpg      # Plugin icon
└── README.md         # This file
```

### Testing Changes

1. Edit the plugin files
2. Restart Ulauncher or press `Ctrl+L` to reload
3. Test with `claude` keyword

### Debugging

Enable debug logging in Ulauncher preferences, then check logs:
```bash
tail -f ~/.local/share/ulauncher/logs/ulauncher.log
```

## Contributing

Found a bug or want to improve the plugin? PRs welcome! Some ideas:

- Support for nested repository directories
- Recent repositories tracking
- Custom repository icons
- Shell completion for the launcher script

## License

MIT

## Credits

Created for quick repository navigation with Claude Code.
