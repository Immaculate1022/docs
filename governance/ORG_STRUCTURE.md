# PegaConstellation organization structure

**Status:** Proposed target state

The organization should be understandable to a first-time visitor without requiring them to infer which repository is canonical. The public front door should be the organization profile plus the hub and docs repositories; the four core projects should be clearly separated from research, labs, community, and archival material.

## Target repository groups

| Group | Repositories | Public role |
|---|---|---|
| Front door | `pegaconstellation-hub`, `docs` | Project map, status pulses, executive materials, ecosystem map, and Pages landing page. |
| Core systems | `IOF-Resonance-Core`, `AHR-Endpoint`, `aetherius-nexus`, `moebius-llama` | Main implementation and research surfaces, each with an explicit maturity statement. |
| Geometry and language | `tesseract-medium`, `iof-design-grammar` | Shared mathematical substrate and conceptual vocabulary. |
| Research and specifications | `research`, `sovereign-reality-engine`, `IOF-Resonant-Hardware`, `Sustained-quantum-tunneling-protocol-` | Notes, specifications, experiments, and hardware/protocol concepts. |
| Labs | `penteract-kaleidoscope`, `tessy-tesseract-kids-lab`, `tessy-4d-shape-explorer` | Visual and educational exploration; avoid presenting these as core system evidence. |
| Governance | `community` | Operating charter, contribution expectations, and safety boundaries. |
| Archive / decision pending | `infinite-optical-fabric-resonance-core` | Hold until its relationship to `IOF-Resonance-Core` is decided. |

## Naming and header standard

Every public repository README should begin with a consistent header in the form **PegaConstellation > IOF > [Repository name]**. The next paragraph should state the repository’s role and maturity in one or two sentences. A visitor should be able to tell whether a repository is a runnable prototype, an experiment, a specification, an educational lab, or an archive before reading implementation details.

Repository names should remain stable during the migration. Renaming should happen only when it removes a genuine ambiguity, such as the relationship between `IOF-Resonance-Core` and `infinite-optical-fabric-resonance-core`. Avoid renaming several repositories during the ownership transfer; ownership migration and taxonomy cleanup are separate changes.

## Organization profile layout

The organization profile README should use this order:

1. A one-sentence description of PegaConstellation as a research and engineering constellation.
2. A “Start here” link to the hub and docs front door.
3. Four core-system cards or links: IOF-Resonance-Core, AHR-Endpoint, Aetherius Nexus, and Möbius-Llama.
4. A geometry/language section linking tesseract-medium and IOF Design Grammar.
5. A research and labs section with clear experimental labels.
6. A short safety and evidence note explaining that conceptual diagrams, prototypes, and passing local checks do not equal measured production results.
7. Contribution and attribution links.

## Default repository settings

Use `main` as the default branch unless a repository has a concrete reason to differ. Keep issues enabled for core systems and governance; use discussions only when there is a clear moderation plan. Add a short security policy to AHR-Endpoint before inviting vulnerability reports. Do not enable Actions workflows merely because a repository has a template; workflows must match the actual project type and should be manual or disabled when their prerequisites are absent.

## Canonical links after migration

| Surface | Canonical organization URL pattern |
|---|---|
| Organization | `https://github.com/PegaConstellation` |
| Hub | `https://github.com/PegaConstellation/pegaconstellation-hub` |
| Docs / Pages | `https://github.com/PegaConstellation/docs` and, after activation, `https://pegaconstellation.github.io/docs/` |
| Core projects | `https://github.com/PegaConstellation/[repository]` |

The organization name and Pages URL are targets, not current facts. Confirm availability and exact casing in GitHub before publishing links that depend on them.
