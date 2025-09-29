# github_api.py
from __future__ import annotations

from typing import List, Tuple, Iterable, Optional
import sys

import requests


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass


def _check_response(resp: requests.Response) -> None:
    """Raise GitHubAPIError if the HTTP response is not 200 OK."""
    if resp.status_code != 200:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        # Common helpful hint for rate limits
        if resp.status_code == 403 and "rate limit" in str(detail).lower():
            raise GitHubAPIError(
                "GitHub API error 403 (rate limit). "
                "Wait a few minutes or add authentication."
            )
        raise GitHubAPIError(f"GitHub API error: {resp.status_code} -> {detail}")


def list_user_repos_with_commit_counts(
    user: str,
    session: Optional[requests.Session] = None
) -> List[Tuple[str, int]]:
    """
    Return a list of (repo_name, commit_count) for the given GitHub user.

    - Uses dependency injection (optional session) so tests can mock easily.
    - Raises GitHubAPIError on any non-200 HTTP response.
    """
    sess = session or requests.Session()
    results: List[Tuple[str, int]] = []

    # 1) list repos
    repos_url = f"https://api.github.com/users/{user}/repos"
    r = sess.get(repos_url)
    _check_response(r)
    repos = r.json()
    if not isinstance(repos, list):
        raise GitHubAPIError("Unexpected response shape for repos list")

    for repo in repos:
        name = repo.get("name")
        if not name:
            continue

        # 2) fetch commits for each repo
        commits_url = f"https://api.github.com/repos/{user}/{name}/commits"
        c_resp = sess.get(commits_url)
        _check_response(c_resp)
        commits = c_resp.json()
        count = len(commits) if isinstance(commits, list) else 0
        results.append((name, count))

    # Stable ordering helps test assertions
    results.sort(key=lambda t: t[0].lower())
    return results


if __name__ == "__main__":
    # Simple CLI: python github_api.py <github_user>
    if len(sys.argv) != 2:
        print("Usage: python github_api.py <github_user>")
        sys.exit(2)

    user = sys.argv[1]
    try:
        rows = list_user_repos_with_commit_counts(user)
        for repo, cnt in rows:
            print(f"Repo: {repo}  Number of commits: {cnt}")
    except GitHubAPIError as e:
        print(f"Error: {e}")
        sys.exit(1)
