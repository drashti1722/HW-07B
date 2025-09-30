# github_api.py
from __future__ import annotations

from typing import List, Tuple, Optional
import os
import time
import requests


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass


def _new_session() -> requests.Session:
    """
    Create a requests session with sensible headers and optional token.
    Kept separate so tests can patch it.
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": "ssw-567-hw-github-client",
        "Accept": "application/vnd.github+json",
    })
    token = os.getenv("GITHUB_TOKEN")  # optional, increases rate limit
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


def _raise_if_error(resp: requests.Response, *, allow_409_empty: bool = False) -> None:
    """
    Raise GitHubAPIError unless response is OK.
    If allow_409_empty=True, treat 409 'Git Repository is empty' as OK (zero commits).
    """
    if resp.status_code == 200:
        return
    if allow_409_empty and resp.status_code == 409:
        return

    # nice message for rate limit cases
    reset = resp.headers.get("X-RateLimit-Reset")
    remaining = resp.headers.get("X-RateLimit-Remaining")
    extra = ""
    if resp.status_code == 403 and remaining == "0" and reset:
        try:
            reset_ts = int(reset)
            mins = max(0, int((reset_ts - time.time()) // 60))
            extra = f" (rate limit hit; try again in ~{mins} min)"
        except Exception:
            extra = " (rate limit hit)"
    try:
        body = resp.json()
    except Exception:
        body = resp.text

    raise GitHubAPIError(f"GitHub API error {resp.status_code}{extra}: {body}")


def list_user_repos_with_commit_counts(
    user: str,
    session: Optional[requests.Session] = None
) -> List[Tuple[str, int]]:
    """
    Return a list of (repo_name, commit_count) for the given GitHub user.
    - On commits endpoint, 409 ('Git Repository is empty') is treated as zero.
    - Any other non-200 raises GitHubAPIError.
    Results are sorted by repo name (case-insensitive).
    """
    close_session = False
    if session is None:
        session = _new_session()
        close_session = True

    try:
        # list repos
        repos_url = f"https://api.github.com/users/{user}/repos?per_page=100"
        r = session.get(repos_url, timeout=20)
        _raise_if_error(r)
        repos = r.json() or []

        results: List[Tuple[str, int]] = []
        for repo in repos:
            name = repo.get("name")
            if not name:
                continue

            commits_url = f"https://api.github.com/repos/{user}/{name}/commits?per_page=100"
            c = session.get(commits_url, timeout=20)
            _raise_if_error(c, allow_409_empty=True)

            if c.status_code == 409:
                count = 0
            else:
                commits = c.json()
                count = len(commits) if isinstance(commits, list) else 0

            results.append((name, count))

        results.sort(key=lambda t: t[0].lower())
        return results
    finally:
        if close_session and hasattr(session, "close"):
            session.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python github_api.py <github_user>")
        sys.exit(2)

    user = sys.argv[1]
    try:
        rows = list_user_repos_with_commit_counts(user)
        for name, cnt in rows:
            print(f"Repo: {name}  Number of commits: {cnt}")
    except GitHubAPIError as e:
        print(e)
        sys.exit(1)
