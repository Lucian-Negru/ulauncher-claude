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


class ClaudeRepoExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


def expand(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def list_repos(repos_dir: str):
    try:
        entries = os.listdir(repos_dir)
    except OSError:
        return []
    repos = [
        name
        for name in entries
        if not name.startswith(".")
        and os.path.isdir(os.path.join(repos_dir, name))
    ]
    repos.sort(key=str.lower)
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

        repos_dir = expand(prefs.get("repos_dir", "~/repos"))
        launcher = expand(prefs.get("launcher_script", "~/.local/bin/claude-repo"))
        try:
            limit = max(1, int(prefs.get("result_limit", "8")))
        except ValueError:
            limit = 8

        repos = list_repos(repos_dir)

        if query:
            scored = []
            for name in repos:
                s = score(name, query)
                if s is not None:
                    scored.append((s, name))
            scored.sort(key=lambda x: x[0])
            matches = [name for _, name in scored[:limit]]
        else:
            matches = repos[:limit]

        items = []

        # Always offer "open in ~/repos root" as first item when query is empty
        if not query:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name=f"Claude in {repos_dir}",
                    description="Launch Claude Code in the repositories root",
                    on_enter=RunScriptAction(
                        f"#!/bin/sh\n{shlex.quote(launcher)} &\n", ""
                    ),
                )
            )

        for name in matches:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name=name,
                    description=os.path.join(repos_dir, name),
                    on_enter=RunScriptAction(
                        f"#!/bin/sh\n{shlex.quote(launcher)} {shlex.quote(name)} &\n",
                        "",
                    ),
                    on_alt_enter=SetUserQueryAction(f"{keyword} {name}"),
                )
            )

        if not items:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name="No repositories found",
                    description=f"Nothing in {repos_dir} matches '{query}'",
                    on_enter=SetUserQueryAction(f"{keyword} "),
                )
            )

        return RenderResultListAction(items)


if __name__ == "__main__":
    ClaudeRepoExtension().run()
