# CI check
# Assignment-SSW-567
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

- Fashion-Era: 2 commits
- First-Spline-3D: 3 commits
- HRMS: 2 commits
- HW03 Number of commits: 14 commits
- Kosol-Clone-Project-: 33 commits
- Magni-Era: 3 commits
- MedVision: 2 commits
- memo-invoice: 7 commits
- NFT-Dashboard: 10 commits
- Shopping-Cart: 4 commits
- SSW-567: 5 commits

