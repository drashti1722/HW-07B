import unittest
import github_api


# ---------- simple fake HTTP machinery (no external libs needed) ----------

class _FakeResponse:
    def __init__(self, status: int, json_obj):
        self.status_code = status
        self._json = json_obj

    @property
    def text(self):
        # Something short to show in raised errors
        try:
            import json
            return json.dumps(self._json)
        except Exception:
            return str(self._json)

    def json(self):
        return self._json


class _FakeSession:
    """
    routes: dict[str, _FakeResponse]
        keys are full URLs to be requested; values are the fake Response to return
    """
    def __init__(self, routes):
        self._routes = dict(routes)

    def get(self, url):
        if url not in self._routes:
            raise AssertionError(f"unexpected URL requested: {url}")
        return self._routes[url]


# ------------------------------ unit tests ---------------------------------

class GithubApiTests(unittest.TestCase):

    def test_happy_two_repos(self):
        """Valid user with two repos, each with commits — counts returned and sorted."""
        user = "alice"
        routes = {
            f"https://api.github.com/users/{user}/repos": _FakeResponse(
                200, [{"name": "Beta"}, {"name": "Alpha"}]  # out of order on purpose
            ),
            f"https://api.github.com/repos/{user}/Alpha/commits": _FakeResponse(
                200, [{"c": 1}] * 10
            ),
            f"https://api.github.com/repos/{user}/Beta/commits": _FakeResponse(
                200, [{"c": 1}] * 11
            ),
        }
        fake_session = _FakeSession(routes)

        out = github_api.list_user_repos_with_commit_counts(user, session=fake_session)
        self.assertEqual(out, [("Alpha", 10), ("Beta", 11)])

    def test_200_from_repos_but_empty_list(self):
        """200 OK from repos endpoint but no repos — should return empty list."""
        user = "norepos"
        routes = {
            f"https://api.github.com/users/{user}/repos": _FakeResponse(200, []),
        }
        fake_session = _FakeSession(routes)

        out = github_api.list_user_repos_with_commit_counts(user, session=fake_session)
        self.assertEqual(out, [])

    def test_non_200_from_repos_raises(self):
        """If the repos endpoint errors, we propagate GitHubAPIError."""
        user = "oops"
        routes = {
            f"https://api.github.com/users/{user}/repos": _FakeResponse(500, {"err": "boom"})
        }
        fake_session = _FakeSession(routes)

        with self.assertRaises(github_api.GitHubAPIError):
            github_api.list_user_repos_with_commit_counts(user, session=fake_session)

    def test_non_200_from_commits_raises(self):
        """Error while fetching commits for one repo raises GitHubAPIError."""
        user = "bob"
        routes = {
            f"https://api.github.com/users/{user}/repos": _FakeResponse(
                200, [{"name": "Only"}]
            ),
            f"https://api.github.com/repos/{user}/Only/commits": _FakeResponse(
                404, {"message": "not found"}
            ),
        }
        fake_session = _FakeSession(routes)

        with self.assertRaises(github_api.GitHubAPIError) as cm:
            github_api.list_user_repos_with_commit_counts(user, session=fake_session)
        # optional: assert message contains status
        self.assertIn("404", str(cm.exception))

    def test_skips_repo_without_name(self):
        """If a repo entry lacks a 'name', we skip it gracefully."""
        user = "odd"
        routes = {
            f"https://api.github.com/users/{user}/repos": _FakeResponse(
                200, [{"id": 1}, {"name": "Good"}]
            ),
            f"https://api.github.com/repos/{user}/Good/commits": _FakeResponse(
                200, [{"c": 1}, {"c": 2}]
            ),
        }
        fake_session = _FakeSession(routes)

        out = github_api.list_user_repos_with_commit_counts(user, session=fake_session)
        self.assertEqual(out, [("Good", 2)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
