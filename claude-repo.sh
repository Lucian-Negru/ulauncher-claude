#!/usr/bin/env bash
set -euo pipefail

# Launcher script for ulauncher-claude plugin
# This script opens Claude Code in a given repository directory
#
# CUSTOMIZE THIS FILE:
# - Change TERMINAL to your preferred terminal (alacritty, kitty, wezterm, gnome-terminal, etc.)
# - Add any environment variables or setup you need before launching Claude

TERMINAL="alacritty"

if [ $# -lt 1 ] || [ -z "$1" ] || [ "$1" = "%s" ]; then
    dir="$HOME/repos"
else
    dir="$HOME/repos/$1"
fi

if [ ! -d "$dir" ]; then
    notify-send "claude-repo" "Repository not found: $dir" 2>/dev/null || true
    echo "Repository not found: $dir" >&2
    exit 1
fi

exec "$TERMINAL" --working-directory "$dir" -e "$HOME/.local/bin/claude"
