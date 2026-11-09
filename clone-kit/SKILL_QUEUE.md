# SKILL_QUEUE · Monthly Skill Review

See [`UPSTREAM_SYNC.md`](../docs/UPSTREAM_SYNC.md) for the process and [`TRANSPARENCY_LOG.md`](../docs/TRANSPARENCY_LOG.md) for licensing decisions. A skill is mirrored only when redistribution permission is clear.

## Process

1. Collect requests from the `skill-request` Discussion template.
2. Review the license, overlap with existing skills, usefulness, and maintenance cost.
3. Mark each request `accept`, `defer`, or `reject`, with a reason.
4. For accepted skills, follow `UPSTREAM_SYNC.md`, update `skills/`, refresh the manifest, and run repository checks.
5. Publish a batch summary and preserve the history below.

## Community requests

| # | Skill or capability | Source | Status | Rationale |
|---|---|---|---|---|
| — | None yet | — | — | Queue created 2026-11-06 |

## Waiting for permission

These 16 local skills are recorded in `MANIFEST.json` with `mirrored: false` because the upstream source did not declare a redistribution license:

`analytics-data-analysis`, `chart-craft-plus`, `data-analysis-pro`, `data-extractor`, `data-scientist`, `data-visualization`, `document-processor`, `excel`, `excel-data-analysis-and-report-generation`, `excel-weekly-dashboard`, `finance-charts`, `market-research-litiao`, `prompt-extractor`, `py-math-viz`, `report-generation`, and `skill-file-converter`.

Platform-internal skills and the three `alibabacloud-*` vendor duplicates are permanently excluded; see the transparency log.

## Third-party MIT collection

Twelve skills from Orchestra AI-Research-SKILLs 1.4.0 have been mirrored. The remaining skills will be reviewed only when requested. The upstream license evidence has an MIT/ISC metadata inconsistency documented in the transparency log.

## Batch history

### 2026-11-06 · Orchestra subset

Mirrored 12 skills: `peft-fine-tuning`, `huggingface-accelerate`, `optimizing-attention-flash`, `evaluating-llms-harness`, `weights-and-biases`, `tensorboard`, `sentence-transformers`, `clip`, `segment-anything-model`, `transformer-lens-interpretability`, `ml-paper-writing`, and `brainstorming-research-ideas`.

### 2026-11-06 · Initial queue

- Community requests: 0.
- Waiting for permission: 16.
- Existing public mirror at that time: 89 skills.
