# Platform Compatibility Matrix

> Last reviewed: 2026-11-09. Tool capabilities change frequently. This matrix
> describes how the clone protocol degrades across hosts; it is not a guarantee
> of current vendor features.

Legend: ✅ native or direct support · 🟡 configuration or reduced mode · ⬜ unavailable

| Capability | ChatGPT/Codex plugin | Claude Code | Codex | Ordinary chat model |
|---|---:|---:|---:|---:|
| One-time installation across conversations | ✅ Plugin install | ✅ User-level skills | ✅ User-level skills | ⬜ Host-dependent |
| Discover all `SKILL.md` files | ✅ | ✅ | ✅ | 🟡 Open selected skills manually |
| Load detailed instructions only when relevant | ✅ | ✅ | ✅ | 🟡 Host-dependent |
| Use the routing table | ✅ | ✅ | ✅ | ✅ |
| Citation, claim, and experiment audits | ✅ | ✅ | ✅ | 🟡 Single-model self-audit only |
| Cross-model review loop | 🟡 Configuration required | 🟡 Configuration required | 🟡 Configuration required | ⬜ Skip and disclose |
| Skills requiring external APIs | 🟡 Credentials required | 🟡 Credentials required | 🟡 Credentials required | 🟡 Credentials required |
| Persistent skill availability | ✅ | ✅ | ✅ | ⬜ Repeat context each session |
| Produce reproducible evidence files | ✅ | ✅ | ✅ | ✅ If file export is supported |

## How to interpret the matrix

- **Zero dependency is the baseline.** Even without plugins, the three protocol
  documents and red lines can be loaded as plain text.
- **Install once where possible.** Follow [`INSTALL_ONCE.md`](INSTALL_ONCE.md)
  instead of pasting the Lite Loader into every conversation.
- **🟡 does not mean unusable.** It means an extra setup step or an explicitly
  reduced protocol.
- **⬜ is intentional degradation.** If a cross-model reviewer or external tool
  is unavailable, skip that claim instead of inventing an audit result.
- Re-run the examples in [`demo_assets/`](demo_assets/) on the target host and
  compare them with [`expected_findings.md`](demo_assets/expected_findings.md).

Update the review date whenever host behavior changes. Automated checks can
verify repository structure, but capability claims still require human review
and public correction through Discussions.
