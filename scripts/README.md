# Repository-link auditor

[`audit_repo_links.py`](audit_repo_links.py) is a read-only pre-migration auditor for the PegaConstellation GitHub constellation. It scans public repository documentation and selected configuration files, extracts unique HTTP(S) links, checks their current status and final redirect target, classifies personal-account versus future-organization URLs, and records a suggested canonical organization URL for links owned by the current account.

## Run it

From a checkout of this repository:

```bash
python3 scripts/audit_repo_links.py \
  --owner Immaculate1022 \
  --target-org PegaConstellation \
  --output-dir link-audit-report
```

Set `GITHUB_TOKEN` when auditing frequently or when the public API rate limit is insufficient. The token is used only for authenticated read requests. The script never writes to GitHub, changes Pages or Actions, transfers repositories, or creates an organization.

Use `--repos repo-a repo-b` to limit the scan to named repositories. The default scan covers every public repository owned by the current account. Each run writes `link-audit.json` for automation and `link-audit.md` for human review.

## Reading the results

Personal-account links are expected before migration. After a repository transfer, rewrite them to the organization target only after the transfer has succeeded and redirects are verified. GitHub Pages results require an explicit decision because a URL may be documented even when Pages is disabled. Any HTTP 4xx or 5xx result must be reviewed before its transfer wave is considered complete.

The first baseline is preserved at [`../governance/link-audit-baseline.md`](../governance/link-audit-baseline.md). Re-run the auditor after each transfer wave and compare issue counts, final URLs, and canonical targets.
