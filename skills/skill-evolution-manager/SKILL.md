---
license: MIT
name: "skill-evolution-manager"
description: "When a project, worksheet, client communication or information reading is completed, it needs to be used to determine whether new skills are being embedded, old skills are being updated, skills are being combined or noise is being discarded."
---

# Skills Development Management

## Trigger scene

- Reusable methods emerge from project revisits.
- Users have repeatedly given stable preferences or constraints.
- Read the information and it is found that the process can be migrated.
- There is duplication, conflict or obsolescence of existing skills.
- The implementation of a given skill is ineffective and needs to be optimized.

## Input

- Original experience: Project records, worksheets, dialogue, code reading, document summary.
- Target types of tasks: sales, R & D, research, delivery, wind control, data, hardware.
- A list of skills is available.
- Quality feedback: causes of failure, back-to-work sites, user preferences, acceptance problems.

## Output

- `discard`：Experience is so accidental and unsettled.
- `create`：Create new skills.
- `improve`：Updating of available skills.
- `merge`：Merge and repeat skills.
- `version_note`：Skills version update notes.
- `quality_gate`：The receiving and inspection door for the subsequent use of the skills is forbidden.

## Workstream

1. To judge whether experience is repetitive and avoid turning one-time chat into a noise skill.
2. Retrieval of existing skills to find similar functions and trigger scenarios.
3. If only additional constraints, priority is given to upgrading existing skills.
4. Create new skills if the boundaries of responsibilities differ.
5. When multiple skills are repeated, a merger is proposed.
6. Identify input, output, restricted areas, manual approval points and acceptance criteria.
7. Quality of skills is reviewed by the Korean test and registered to the knowledge base by Wincheon.

## Quality off-limits

- Skills must be subject to clear trigger conditions and cannot be said in general terms.
- Skills must produce archived deliverables.
- Skills do not extend the boundaries of authority.
- The skills update must be maintained in a version of the description.
- Skills related to quotations, contracts, payments, real customer data and production systems must be manually approved.

## References

- `source/xiaohongshu/extracted/AutoSkill-main`
- `source/xiaohongshu/extracted/skills-coach-main`
