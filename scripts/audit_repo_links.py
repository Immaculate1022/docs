#!/usr/bin/env python3
"""Read-only pre-migration auditor for GitHub repository links and canonical URLs.

The auditor uses GitHub's public REST API and raw file endpoints. It never writes
repository content, changes Pages, transfers ownership, or creates an organization.
Set GITHUB_TOKEN to increase API rate limits when auditing a larger constellation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

URL_RE = re.compile(r"https?://[^\s<>\"'`()\[\]{}]+", re.IGNORECASE)
TEXT_PATH_RE = re.compile(
    r"(?:^README(?:\.[^/]+)?$|^STATUS\.md$|^docs/.*\.(?:md|mdx|txt)$|^\.github/workflows/.*\.ya?ml$|^(?:Cargo\.toml|package\.json|pyproject\.toml)$)",
    re.IGNORECASE,
)
TRAILING_PUNCTUATION = ".,;:!?)]}>'\""


@dataclass
class LinkFinding:
    source_repo: str
    source_path: str
    url: str
    kind: str
    status: int | None
    final_url: str | None
    issue: str | None
    canonical_url: str | None


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.headers = {"Accept": "application/vnd.github+json", "User-Agent": "pegaconstellation-link-auditor/1.0"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_json(self, url: str) -> object:
        request = Request(url, headers=self.headers)
        with urlopen(request, timeout=20) as response:
            return json.load(response)

    def get_text(self, url: str) -> str:
        request = Request(url, headers={**self.headers, "Accept": "text/plain"})
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="replace")

    def check_url(self, url: str) -> tuple[int | None, str | None]:
        request = Request(url, headers={"User-Agent": self.headers["User-Agent"]}, method="HEAD")
        try:
            with urlopen(request, timeout=15) as response:
                return response.status, response.geturl()
        except HTTPError as error:
            if error.code in {403, 405}:
                try:
                    request = Request(url, headers={"User-Agent": self.headers["User-Agent"]}, method="GET")
                    with urlopen(request, timeout=15) as response:
                        return response.status, response.geturl()
                except (HTTPError, URLError):
                    return error.code, error.geturl() if hasattr(error, "geturl") else None
            return error.code, error.geturl() if hasattr(error, "geturl") else None
        except URLError:
            return None, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="Immaculate1022", help="Current GitHub owner")
    parser.add_argument("--target-org", default="PegaConstellation", help="Future organization login")
    parser.add_argument("--output-dir", type=Path, default=Path("link-audit-report"))
    parser.add_argument("--repos", nargs="*", help="Optional repository names; default is every public repo")
    parser.add_argument("--sleep", type=float, default=0.05, help="Delay between API requests")
    return parser.parse_args()


def clean_url(raw: str) -> str:
    return raw.rstrip(TRAILING_PUNCTUATION)


def classify_url(url: str, owner: str, target_org: str) -> tuple[str, str | None, str | None]:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [part for part in parsed.path.split("/") if part]
    if host == "github.com" and path_parts:
        if path_parts[0].lower() == owner.lower():
            canonical = "/".join(["https://github.com", target_org, *path_parts[1:]])
            return "personal-account", f"candidate for {target_org} migration", canonical
        if path_parts[0].lower() == target_org.lower():
            return "target-organization", None, None
        return "external-github", None, None
    if host.endswith("github.io"):
        return "github-pages", "verify Pages is intentionally enabled and the path is live", None
    if host == "raw.githubusercontent.com":
        return "raw-github", None, None
    return "external", None, None


def repo_files(client: GitHubClient, owner: str, repo: dict, delay: float) -> Iterable[tuple[str, str]]:
    name = repo["name"]
    branch = repo.get("default_branch") or "main"
    tree_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
    tree = client.get_json(tree_url)
    for item in tree.get("tree", []):
        path = item.get("path", "")
        if item.get("type") != "blob" or not TEXT_PATH_RE.match(path):
            continue
        raw_url = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/{path}"
        try:
            yield path, client.get_text(raw_url)
        except (HTTPError, URLError):
            continue
        time.sleep(delay)


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    client = GitHubClient(os.environ.get("GITHUB_TOKEN"))
    repos = client.get_json(f"https://api.github.com/users/{args.owner}/repos?per_page=100&sort=updated")
    selected = [repo for repo in repos if not args.repos or repo["name"] in args.repos]
    selected = [repo for repo in selected if repo.get("visibility") == "public"]

    findings: list[LinkFinding] = []
    scanned_files = 0
    unique_urls: set[str] = set()
    for repo in selected:
        for path, text in repo_files(client, args.owner, repo, args.sleep):
            scanned_files += 1
            for raw_url in URL_RE.findall(text):
                url = clean_url(raw_url)
                if url in unique_urls:
                    continue
                unique_urls.add(url)
                kind, note, canonical_url = classify_url(url, args.owner, args.target_org)
                status, final_url = client.check_url(url)
                issue = note
                if status is None:
                    issue = issue or "request failed or host unavailable"
                elif status >= 400:
                    issue = f"HTTP {status}" if not issue else f"{issue}; HTTP {status}"
                findings.append(LinkFinding(repo["name"], path, url, kind, status, final_url, issue, canonical_url))
                time.sleep(args.sleep)

    counts: dict[str, int] = {}
    for finding in findings:
        key = finding.issue or "ok"
        counts[key] = counts.get(key, 0) + 1
    report = {
        "auditor": "pegaconstellation-link-auditor/1.0",
        "read_only": True,
        "owner": args.owner,
        "target_org": args.target_org,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "repositories_scanned": len(selected),
        "files_scanned": scanned_files,
        "unique_urls_checked": len(findings),
        "issue_counts": counts,
        "findings": [asdict(finding) for finding in findings],
    }
    json_path = args.output_dir / "link-audit.json"
    md_path = args.output_dir / "link-audit.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# PegaConstellation repository-link audit",
        "",
        f"**Generated:** {report['generated_at']}  ",
        f"**Scope:** `{args.owner}` public repositories → proposed `{args.target_org}` organization  ",
        "**Mode:** read-only; no repository, Pages, Actions, or ownership settings were changed.",
        "",
        "## Summary",
        "",
        f"Scanned **{len(selected)} repositories**, **{scanned_files} text files**, and checked **{len(findings)} unique URLs**.",
        "",
        "| Issue | Count |",
        "|---|---:|",
    ]
    for key, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Findings", "", "| Repository | Source | Kind | Status | URL | Canonical target | Issue |", "|---|---|---|---:|---|---|---|"])
    for finding in findings:
        issue = finding.issue or "—"
        status = str(finding.status) if finding.status is not None else "—"
        canonical = f"`{finding.canonical_url}`" if finding.canonical_url else "—"
        lines.append(f"| `{finding.source_repo}` | `{finding.source_path}` | {finding.kind} | {status} | `{finding.url}` | {canonical} | {issue} |")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Personal-account GitHub links are expected before migration but should be rewritten to the organization URL after each repository transfer. GitHub Pages links require an explicit decision because a repository can contain a landing page without Pages being enabled. HTTP failures require human review before a transfer wave is considered complete.",
        "",
        "The JSON file is the machine-readable baseline for a later post-migration comparison. Re-run the same command after each transfer wave and compare status, final URLs, and issue counts.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"json_report": str(json_path), "markdown_report": str(md_path), "summary": {"repositories": len(selected), "files": scanned_files, "urls": len(findings), "issues": counts}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
