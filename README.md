# CI check
# Assignment-SSW-567
 HW03b_Mocking
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/drashti1722/Assignment-SSW-567/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/drashti1722/Assignment-SSW-567/tree/main)

This project queries the GitHub API to retrieve a list of repositories for a given user and the number of commits in each repository.  

It includes:
- A core function (`get_user_repos_and_commits`) implemented in **`src/github_api.py`**  
- A simple demo program (**`demo.py`**) for interactive use  
- Unit tests in **`tests/test_github_api.py`**

---

## Requirements
- Python 3.8+
- `requests`
- `pytest`

Install dependencies:
```bash
pip install -r requirements.txt

GitHub Repo Commit Counter

Repositories and commit counts for 'drashti1722':

Repo: Assignment-SSW-567 Number of commits: 5
Repo: HelloWorld Number of commits: 1
Repo: shop-website Number of commits: 1
Repo: shoping Number of commits: 1
=======


