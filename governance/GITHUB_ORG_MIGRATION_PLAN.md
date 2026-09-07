# PegaConstellation GitHub organization migration plan

**Status:** Proposed; no organization has been created and no repository has been transferred.

**Prepared:** 2026-09-07

## Objective

Move the public PegaConstellation work from the personal `Immaculate1022` account into one organization so that the project map, issues, Pages sites, permissions, and ownership have a stable public home. The migration should preserve repository history, redirects, licenses, issue context, releases, and links.

> The organization is an ownership and navigation improvement, not a claim that every repository is production-ready. Prototype, research, educational, and archival status labels must move with the repositories.

## Proposed transfer order

| Wave | Repositories | Reason | Gate before transfer |
|---|---|---|---|
| 0 — prepare | `docs`, `pegaconstellation-hub`, profile README review | Establish the new public front door and redirect targets first. | Confirm canonical URLs, README links, Pages plan, and license files. |
| 1 — core | `IOF-Resonance-Core`, `AHR-Endpoint`, `aetherius-nexus`, `moebius-llama` | Move the four repositories visitors are most likely to treat as the main product surface. | Confirm README status language, build commands, archived-candidate boundaries, and external links. |
| 2 — substrate and research | `tesseract-medium`, `iof-design-grammar`, `research`, `sovereign-reality-engine`, `IOF-Resonant-Hardware`, `Sustained-quantum-tunneling-protocol-` | Move supporting conceptual, geometry, research, and hardware work once the core map is stable. | Review licenses and decide canonical names for duplicate or similarly named surfaces. |
| 3 — labs and community | `penteract-kaleidoscope`, `tessy-tesseract-kids-lab`, `tessy-4d-shape-explorer`, `community` | Move educational labs and governance material after the core navigation is tested. | Verify child-friendly language, links, and community charter references. |
| hold | `infinite-optical-fabric-resonance-core` | Possible duplicate or alternate surface for `IOF-Resonance-Core`. | Decide whether to archive, redirect, consolidate, or retain before transfer. |

## Pre-transfer checklist

Create the organization with the intended name and owner account. Enable two-factor authentication and choose the smallest useful member/permission model. Before moving repositories, add a consistent attribution and license file wherever the author intends the same terms to apply; do not silently replace MIT, Apache-2.0, or repository-specific terms.

Search every README, workflow, Pages configuration, badge, package manifest, and documentation link for the old `Immaculate1022/<repo>` URL. Keep the personal profile README as a short pointer to the organization rather than deleting the profile repository. Record the canonical new URLs in a migration manifest.

## Transfer procedure

1. Create the organization through GitHub’s organization flow; verify the final login/name before proceeding.
2. Add only the required owner and maintainers, with two-factor authentication enabled.
3. Transfer the wave-0 documentation repositories and verify redirects, links, Pages, Actions, and branch protection.
4. Transfer the wave-1 core repositories one at a time. After each transfer, clone the new URL, run the documented checks, and inspect the repository’s Actions and Pages settings.
5. Transfer the supporting waves only after the front door and core links are stable.
6. Update the profile README, hub, docs index, package metadata, badges, and external references to point to the organization.
7. Leave the personal account repositories in place only as GitHub redirects or profile infrastructure; do not create duplicate forks.

## Verification gates

| Gate | Pass condition |
|---|---|
| Ownership | Repository appears under the organization and the old URL redirects. |
| Code integrity | Default branch, commit history, tags, releases, issues, and pull requests remain present. |
| Documentation | README, hub, docs index, and ecosystem map resolve through organization URLs. |
| Build | AHR `cargo fmt -- --check`, `cargo check`, and `cargo test` remain green; Möbius install/import is verified separately. |
| Safety | AHR dry-run audit remains green; archived candidate modules are not activated automatically. |
| Hosting | Pages is intentionally enabled or intentionally left disabled; no failing workflow is left push-triggered. |
| License | License files and attribution terms are explicit and consistent with the author’s intent. |

## Rollback posture

Do not delete the personal repositories immediately after transfer. Use GitHub redirects and retain a local clone of each repository. If a transfer causes broken links, missing Actions permissions, or Pages problems, stop the next wave and repair the affected repository before continuing. Reversal should be treated as an account-level GitHub operation, not a destructive Git reset.

## Account-level references

- [GitHub: Transferring a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository)
- [GitHub: Creating an organization](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch)
- [GitHub: Managing repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)
