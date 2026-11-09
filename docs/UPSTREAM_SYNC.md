# UPSTREAM_SYNC · Upstream synchronisation and synthesizing process

> `skills/` Mirror From [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（MIT）。
> This document sets out how to track upstream evolution and make changes**Development**Into the warehouse: a mirror, an unmistakable, and a trail from the entire journey.

## Snapshot Baseline

- Checkout date and list:`clone-kit/MANIFEST.json`（With every skill. source / version / installUrl）。
- Mirror scope: Upper upstream 87 A skills directory. SKILL.md Original + Additional to this warehouse"Mirror description"Paragraph (see `skills/NOTICE.md`）。
- Support documentation (%1)scripts/、references/、../shared-references/）**No mirror distribution**，Go back upstream when used.

## Synchronization of processes (on a monthly or larger upstream version)

0. **Take differences (mechanized)**：`python scripts/upstream_diff.py`（Aluminous clones upstream of the warehouse cache, stripping out of this warehouse for additional sections/End of line/The end of the line is empty, and the skills of the Hashi comparison, the output. added / removed / changed；
   When the show's done, `--save-snapshot` Refresh `clone-kit/UPSTREAM_SNAPSHOT.json` Baseline.
1. **Take the difference.**：Upstream, newest. tag/commit，and MANIFEST A snapshot. commit Contrast:
   `git -C <Upstream cloning> log --oneline <A snapshot.commit>..HEAD -- skills/`；
   List New / Delete / Modify the skills directory.
2. **Classification**：
   - Revision: skills by skills diff SKILL.md；Determining whether to influence the semantics of the instructions (semanmatic changes)→Rerun security self-check list; plain language→Direct synchronization;
   - Add: Press `CONTRIBUTING.md` (b) A self-checking list of good faith and a decision on whether or not to develop a mirror;
   - Delete: Remove from mirror and TRANSPARENCY_LOG Records"Upstream Remove"。
3. **Security Scan**：New/Change of content to the platform or CI Scanning;**I can't get past it.**，Press TRANSPARENCY_LOG Processes are publicly recorded.
4. **Update List**：Refresh MANIFEST The date of the snapshot and the date of the version Fields;README Synchronizes the badges if they contain a count.
5. **Queue submission**：commit message Fixed Prefix `sync(aris): <A snapshot.commitShort Hashi.> -> <New Hashi.>`，
   body List New/Delete/Semantic changes to the list of three categories.
6. **Announcement**：Discussions Send one. sync Bulletin (templates can be reused) skill-request the structure of the).)

## Principles of communication (why not all automatic mirrors)

- This warehouse is...**Policy version**：Keep subsets and Chinese guides useful to beginners, without upstream integrity fork；
- Default for additional skills upstream**I'm not coming in.**Mirrors, menstruation. Discussion Entry after needs or maintenance assessment (demand-driven);
- Any additional paragraphs to the upstream text (e.g."Mirror description"）It must be clearly marked and do not change the semantics of the instructions;
- The chain of permits is continuous:NOTICE and LICENSE The upstream copyright line is always retained in the appendix.

## Not ARIS Source skills Community contribution or self-research skills entry `skills/` Hour:frontmatter Source indicated (original)/Upper URL），
Permission must be granted. MIT compatibility; in MANIFEST Middle by `source: community|original` Tags, with `source: aris-mirror` Distinguishing.
