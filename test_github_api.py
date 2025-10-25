# test_github_api.py
import unittest
from unittest.mock import MagicMock, patch

import github_api
from github_api import GitHubAPIError, list_user_repos_with_commit_counts


# ---- tiny response stub the mocks will return ----
class _Resp:
    def __init__(self, status_code=200, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json = [] if json_data is None else json_data
        self.text = text if text else str(self._json)
        self.headers = headers or {}

    def json(self):
        return self._json


def _mk_session(routes):
    """
    Build a MagicMock session whose .get(url, **kwargs) returns _Resp
    from the 'routes' dict (keyed by the full URL string).
    Unknown URLs return 404.
    """
    session = MagicMock()

    def _get(url, **kwargs):  # accept **kwargs (timeout, etc.)
        return routes.get(url, _Resp(status_code=404, json_data={"err": "not found"}))

    session.get.side_effect = _get
    return session


class GithubApiTests(unittest.TestCase):
    # ---------- helpers ----------
    def _repos_url(self, user):
        return f"https://api.github.com/users/{user}/repos?per_page=100"

    def _commits_url(self, user, repo):
        return f"https://api.github.com/repos/{user}/{repo}/commits?per_page=100"

    # ---------- tests ----------
    def test_happy_two_repos(self):
        """Valid user with two repos; counts returned and alphabetically sorted."""
        user = "alice"
        routes = {
            self._repos_url(user): _Resp(200, [{"name": "Beta"}, {"name": "Alpha"}]),
            self._commits_url(user, "Beta"): _Resp(200, [{}, {}, {}]),  # 3
            self._commits_url(user, "Alpha"): _Resp(200, [{}, {}]),    # 2
        }
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            out = list_user_repos_with_commit_counts(user)
        self.assertEqual(out, [("Alpha", 2), ("Beta", 3)])

    def test_200_from_repos_but_empty_list(self):
        """200 OK from repos endpoint but no repos — should return empty list."""
        user = "bob"
        routes = {self._repos_url(user): _Resp(200, [])}
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            out = list_user_repos_with_commit_counts(user)
        self.assertEqual(out, [])

    def test_non_200_from_repos_raises(self):
        """If the repos endpoint errors, raise GitHubAPIError."""
        user = "charlie"
        routes = {self._repos_url(user): _Resp(500, {"err": "boom"})}
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            with self.assertRaises(GitHubAPIError):
                list_user_repos_with_commit_counts(user)

    def test_non_200_from_commits_raises(self):
        """Error while fetching commits for one repo raises GitHubAPIError."""
        user = "dana"
        routes = {
            self._repos_url(user): _Resp(200, [{"name": "Only"}]),
            self._commits_url(user, "Only"): _Resp(500, {"err": "boom"}),
        }
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            with self.assertRaises(GitHubAPIError):
                list_user_repos_with_commit_counts(user)

    def test_commits_409_empty_repo_counts_as_zero(self):
        """409 'Git Repository is empty' should be treated as zero commits."""
        user = "erin"
        routes = {
            self._repos_url(user): _Resp(200, [{"name": "NewRepo"}]),
            self._commits_url(user, "NewRepo"): _Resp(
                409, {"message": "Git Repository is empty.", "status": "409"}
            ),
        }
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            out = list_user_repos_with_commit_counts(user)
        self.assertEqual(out, [("NewRepo", 0)])

    def test_skips_repo_without_name(self):
        """If a repo entry lacks a 'name', it should be skipped gracefully."""
        user = "frank"
        routes = {
            self._repos_url(user): _Resp(200, [{"id": 1}, {"name": "Good"}]),
            self._commits_url(user, "Good"): _Resp(200, [{}, {}]),
        }
        fake_session = _mk_session(routes)
        with patch.object(github_api, "_new_session", return_value=fake_session):
            out = list_user_repos_with_commit_counts(user)
        self.assertEqual(out, [("Good", 2)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
