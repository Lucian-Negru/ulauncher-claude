import os
import shlex

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

ICON = "images/icon.jpg"
LAUNCHER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude-repo.sh")


class ClaudeRepoExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


def expand(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def parse_dirs(raw: str):
    dirs = []
    for part in (raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        path = expand(part)
        if path not in dirs:
            dirs.append(path)
    return dirs or [expand("~/repos")]


def launch_action(env: str, target: str) -> RunScriptAction:
    return RunScriptAction(
        f"#!/bin/sh\n{env}{shlex.quote(LAUNCHER)} {shlex.quote(target)} &\n", ""
    )


def list_repos(dirs):
    """Return (name, path) for every repo across all directories, sorted by name."""
    repos = []
    seen = set()
    for repos_dir in dirs:
        try:
            entries = os.listdir(repos_dir)
        except OSError:
            continue
        for name in entries:
            path = os.path.join(repos_dir, name)
            if name.startswith(".") or path in seen or not os.path.isdir(path):
                continue
            seen.add(path)
            repos.append((name, path))
    repos.sort(key=lambda r: (r[0].lower(), r[1]))
    return repos


def score(name: str, query: str):
    """Lower is better. Returns None if the repo doesn't match."""
    name_l = name.lower()
    query_l = query.lower()
    if name_l.startswith(query_l):
        return (0, name_l)
    idx = name_l.find(query_l)
    if idx >= 0:
        return (1, idx, name_l)
    # subsequence fallback
    i = 0
    for ch in name_l:
        if i < len(query_l) and ch == query_l[i]:
            i += 1
    if i == len(query_l):
        return (2, name_l)
    return None


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        prefs = extension.preferences
        keyword = event.get_keyword() or prefs.get("claude_kw", "claude")
        query = (event.get_argument() or "").strip()

        repos_dirs = parse_dirs(prefs.get("repos_dir", "~/repos"))
        terminal = (prefs.get("terminal") or "").strip()
        env = f"TERMINAL={shlex.quote(terminal)} " if terminal else ""
        try:
            limit = max(1, int(prefs.get("result_limit", "8")))
        except ValueError:
            limit = 8

        repos = list_repos(repos_dirs)

        if query:
            scored = []
            for name, path in repos:
                s = score(name, query)
                if s is not None:
                    scored.append((s, name, path))
            scored.sort(key=lambda x: x[0])
            matches = [(name, path) for _, name, path in scored[:limit]]
        else:
            matches = repos[:limit]

        items = []

        if not query:
            for repos_dir in repos_dirs:
                if not os.path.isdir(repos_dir):
                    continue
                items.append(
                    ExtensionResultItem(
                        icon=ICON,
                        name=f"Claude in {repos_dir}",
                        description="Launch Claude Code in the repositories root",
                        on_enter=launch_action(env, repos_dir),
                    )
                )

        for name, path in matches:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name=name,
                    description=path,
                    on_enter=launch_action(env, path),
                    on_alt_enter=SetUserQueryAction(f"{keyword} {name}"),
                )
            )

        if not items:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name="No repositories found",
                    description=f"Nothing matches '{query}'" if query else "No repositories configured",
                    on_enter=SetUserQueryAction(f"{keyword} "),
                )
            )

        return RenderResultListAction(items)


if __name__ == "__main__":
    ClaudeRepoExtension().run()
