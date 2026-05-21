"""
github_client.py
Client GitHub minimal pour ALFRED.

Variables d'environnement (.env) :
    GITHUB_TOKEN=ghp_...
    GITHUB_OWNER=cognitive-products-lab
    GITHUB_REPO=alfred_assistant
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

_API = "https://api.github.com"


class GitHubClient:

    def __init__(
        self,
        token: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ):
        self.token = token or os.getenv("GITHUB_TOKEN", "")
        self.owner = owner or os.getenv("GITHUB_OWNER", "")
        self.repo = repo or os.getenv("GITHUB_REPO", "")

        if not self.token:
            raise ValueError("GITHUB_TOKEN manquant dans .env")
        if not self.owner or not self.repo:
            raise ValueError("GITHUB_OWNER et GITHUB_REPO requis dans .env")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[dict] = None,
    ) -> Any:
        url = f"{_API}{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"GitHub API {method} {path} → {e.code}: {e.read().decode()}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        try:
            self._request("GET", "/user")
            return True
        except Exception:
            return False

    def list_issues(self, state: str = "open") -> list[dict]:
        path = f"/repos/{self.owner}/{self.repo}/issues?state={state}&per_page=50"
        return self._request("GET", path)

    def create_issue(self, title: str, body: str = "", labels: Optional[list[str]] = None) -> dict:
        payload: dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return self._request("POST", f"/repos/{self.owner}/{self.repo}/issues", payload)

    def add_issue_comment(self, issue_number: int, comment: str) -> dict:
        return self._request(
            "POST",
            f"/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments",
            {"body": comment},
        )

    def list_pull_requests(self, state: str = "open") -> list[dict]:
        path = f"/repos/{self.owner}/{self.repo}/pulls?state={state}&per_page=50"
        return self._request("GET", path)

    def get_repo_info(self) -> dict:
        return self._request("GET", f"/repos/{self.owner}/{self.repo}")
