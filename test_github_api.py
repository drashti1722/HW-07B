import unittest
from unittest.mock import patch
import github_api

class _Resp:
    """Mock response object."""
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

class _FakeSession:
    """Mock session object."""
    def __init__(self, responses):
        self.responses = responses

    def get(self, url, timeout=None):  # Added `timeout` argument
        if url in self.responses:
            return self.responses[url]
        raise ValueError(f"Unexpected URL: {url}")

    def close(self):  # Add a `close` method to mock the real session's behavior
        pass

def _mk_session(routes):
    """Create a fake session with predefined routes."""
    responses = {url: _Resp(status, data) for url, (status, data) in routes.items()}
    return _FakeSession(responses)

class TestGitHubAPI(unittest.TestCase):
    def _repos_url(self, user):
        return f"https://api.github.com/users/{user}/repos?per_page=100"

    def _commits_url(self, user, repo):
        return f"https://api.github.com/repos/{user}/{repo}/commits?per_page=100"

    # ---------- tests ----------
    def test_happy_two_repos(self):
        """Valid user with two repos; counts returned and alphabetically sorted."""
        user = "alice"
        routes = {
            self._repos_url(user): (200, [
                {"name": "Beta"},
                {"name": "Alpha"},
            ]),
            self._commits_url(user, "Beta"): (200, [{}, {}, {}]),  # 3 commits
            self._commits_url(user, "Alpha"): (200, [{}, {}]),    # 2 commits
        }
        fake_session = _mk_session(routes)

        with patch.object(github_api, "_new_session", return_value=fake_session):
            out = github_api.list_user_repos_with_commit_counts(user)

        self.assertEqual(out, [("Alpha", 2), ("Beta", 3)])

if __name__ == "__main__":
    unittest.main(verbosity=2)