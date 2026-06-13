#!/usr/bin/env bash
set -euo pipefail

# Launcher script for ulauncher-claude plugin.
# Opens Claude Code in the directory passed as the first argument.
#
# The terminal is set from the extension's "Terminal" preference via the
# TERMINAL environment variable, and defaults to the system default terminal.

TERMINAL="${TERMINAL:-x-terminal-emulator}"
CLAUDE="$HOME/.local/bin/claude"

dir="${1:-$PWD}"

if [ ! -d "$dir" ]; then
    notify-send "claude-repo" "Directory not found: $dir" 2>/dev/null || true
    echo "Directory not found: $dir" >&2
    exit 1
fi

# Terminals differ in how they take a working directory and a command to run.
# Where tabs are supported, open a new tab in the active window.
case "$(basename "$TERMINAL")" in
    ptyxis | x-terminal-emulator | gnome-terminal)
        exec "$TERMINAL" --tab --working-directory="$dir" -- "$CLAUDE" ;;
    konsole)
        exec "$TERMINAL" --new-tab --workdir "$dir" -e "$CLAUDE" ;;
    kitty)
        exec "$TERMINAL" --directory "$dir" "$CLAUDE" ;;
    wezterm)
        exec "$TERMINAL" start --cwd "$dir" -- "$CLAUDE" ;;
    *)
        # alacritty, xterm, … have no working-directory flag, so run from the directory itself.
        cd "$dir"
        exec "$TERMINAL" -e "$CLAUDE" ;;
esac
