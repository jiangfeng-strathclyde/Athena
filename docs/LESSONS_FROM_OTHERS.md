# LESSONS_FROM_OTHERS · Research and lessons learned on a case-by-case basis for similar projects

> Snapshot:2026-11-09。Scope of the study: locally collected treaties 45 The project is based on the main scientific framework, the skills base and related platforms.
> Read it one by one. README With key architecture files (arrangement portals, skills)/prompt Format, Validation Section).
> Principles:**Research mechanisms only, no copying**——All on this page"Absorptable"All refer to practices and thinking;
> Any Text/The code has to be introduced first. [`skills/NOTICE.md`](../skills/NOTICE.md) The permit door.
> Position unchanged: we don't make one key out paper（See [`POSITIONING.md`](POSITIONING.md)）。

## I. Five cross-cutting conclusions (most valuable to us)

### 1. Turn honesty into a mechanism, not a slogan. We have red lines in the best projects."Enforceable"corresponding to:

- **ScienceClaw**（MIT）：Zero hallucination is the toughest word.——"Each reference must be returned from the tools of the current dialogue; the database cannot be cited without returning; the results are reported as missing if not available.**No backsliding to training.**"；And there is."Agreement against premature conclusion"：
  Minimum number of tool calls by mission type (%)quick=5 / survey=30 / review=60），We have to get past it before it's over. 7 Item checklist。
- **AutoResearchClaw**（MIT）：VerifiedRegistry——Each number in the paper must correspond to the real experimental product and the number has not been verified as being compulsorily laundered;4 Layer Reference Verification (Purpose)arXiv→CrossRef→S2→LLM (Relevance), hallucination references are automatically deleted.
- **codex-autoresearch**（MIT）：Verify/Guard Double door.——Verify Check if the indicators are improving.Guard Check to see if the other one is broken.guard It's a document that can't be changed. It's a document that can't be changed."The values are good, but the mechanisms are not right."Fake success.
- **OpenScholar**（Apache-2.0）：Answers with sentence-by-line references, cross-references; from feedback loop (generated)→Self-assessment lack of evidence→Orientation Retrieval→(d) Revisions).

**Orientation of Absorption**：Search/General skills plus"Minimum search source + End of story. checklist"；"If you can't find it, report the results."
text in red-line documents; evaluation class extension"Rating formula is fully visible, parameters can be custom-made"（PaperClaw A positive example.

### 2. Classification of human confirmation points (conservative to beginner default)

- AutoResearchClaw：Staple Lines 3 Individual work approval gate，Refusal to roll back;
- codex-autoresearch：Before startup Wizard 1–5 Reconfirm the target./Indicators/verify Commands;
- EvoScientist（Apache-2.0）：shell Command default manual approval + White list before command + Session Level"This full approval"；
- oh-my-claudecode（MIT）：Skills frontmatter Add `level: 1-4` Mark autonomy.

**Orientation of Absorption**：Ours."Give me a list of the costs, wait for the list of points before you do it."It's already the same practice; it could be further developed
ROUTING_TABLE , the assembly rules indicate the default approval level at the operating cost, and high-cost operations impose low autonomy.

### 3. Newcomer steering layer: a better place than we did.

- **claude-howto**（MIT）：LEARNING-ROADMAP Tier by Horizontal + "Find Your Level" The entrance. + Single Page QUICK_REFERENCE；
- **research-skills**（None LICENSE，Only practices can be used:README Top"Skills/Description/Trigger Word"List III, newcomers do not have to count in the catalogue;
- **academic-ai-prompt**（MIT）：Fill-in-the-Type Templates (Type Templates)[Grade][Teacher's orientation.][The way you're trying to avoid it.]），It's very friendly for students who can't write codes.
- **DeepTutor**（Apache-2.0）：Wrong Question(s)Question Notebook）、Read the self-censorship three questions, lasting. TutorBot——The audience fully coincides with us;
- **autoresearch**（Karpathy Prototype: Fixed 5 Minute budget + A single comparable indicator + "Just one file."，
  It's for undergraduates to understand."Fair comparison,diff Admissible"The smallest textbook.

**Orientation of Absorption**：START_HERE Already in the same direction; reparable"Info Collection Fillup Template"The path chart prefixes, adds to the documentation skills."Read the self-censorship three questions."The link.

### 4. Engineering practices in skills organization and state management

- **codex-autoresearch**：SKILL.md + `references/` Load as required (in mode only the required fascicles, control) token）；
- **AI-Research-SKILLs / Orchestra**（MIT）：frontmatter Add `tags`/`dependencies` fields;programming skills maintenance `research-state.yaml` + `findings.md` Inter-session status;`to_human/` A catalogue of regularly produced human-readable progress reports;
- **DrClaw**（README Name MIT，None LICENSE Documents:MEMORY.md（(Long-term memory rewriteable) and
  HISTORY.md（append-only Audit log) separation; tool-type sub-agent in a state + Hard overlap cap + It must be reciprocated;
- **ResearchClaw**（Apache-2.0）：claim/evidence Figure——Every theory is evidence (thesis)/Notes/Experiment/Quoted; Gap automatically generates remediation tasks;README Quite frankly."still incomplete + List of maximum gaps"；
- **MedgeClaw**（README Name MIT，None LICENSE Documents:state.json + Single HTML Zero reliance on progress dashboards for rounding;
- **PaperClaw**（README Name MIT，None LICENSE Documents:"The meta-skill generation area Agent"——An interview collection of knowledge in the field, and a scaffolding belt. 5 Profiling and tracking of papers on time-bound tasks Agent；To re-index. + The status file design of the file lock.

**Orientation of Absorption**：109 Skillable skills can be broken down. `references/` Load as required; agree a unified status document for long-chain skills;
"Rewrite memory vs Only add logs"The separation is written into the collaboration agreement.

### 5. Licensing health and expectation management (reverse materials are equally useful)

- Multiple items (DrClaw / PaperClaw / MedgeClaw / Auto-Resubmit / autoresearch / research-skills /
  Memento-Skills）**README Claim MIT But it's not in the warehouse. LICENSE Documentation**——Legally, the retention-of-title interest is implied, and we do not copy the text, but we do. MANIFEST Hold on."The mirror must have a clear release."Reasons;
- CitationClaw Yes. CC BY-NC 4.0（Non-commercial);ipaperview It's a custom clause.——The same is true of research;
- Auto-Resubmit puts likely failure modes and required fixes in the most visible part of its README; DrClaw states its limitations just as directly.
  "I can't get you a doctorate."——A model of how to expect to manage writing, with us."Borders (4 Lines)"Same family.

## II. Project-by-project quick-view forms✅=Yes. LICENSE Documentation　⚠️=README Claimed but not documented　❌=No declaration.
"Introduction"All Rows**Yes**：This page projects are only research and non-recording.
[`TRANSPARENCY_LOG.md`](TRANSPARENCY_LOG.md) §5）。

### Autonomous scientific framework

| Item | One word. | Permissions | One of the most interesting things to learn from. |
|---|---|---|---|
| AutoResearchClaw | 23 Phase"Thesis."Full Auto-Tip | ✅ MIT | VerifiedRegistry：The numbers have to be traced back to the experimental product. |
| ScienceClaw | 285 Skills + 629 Okay. SCIENCE.md Agreement | ✅ MIT | Minimum number of tool calls + Countering premature conclusions checklist |
| codex-autoresearch | Target-driven unmanned loops | ✅ MIT | Verify/Guard Double Door Authentication |
| autoresearch | Karpathy It's an extremely simple night experiment prototype. | ⚠️ | Fixed budget + A single comparable indicator |
| EvoScientist | LangChain DeepAgents Self-evolving scientists | ✅ Apache-2.0 | Tier approval + Command White List |
| ResearchClaw | Local-first "Research OS" | ✅ Apache-2.0 | claim/evidence Figure |
| ClawPhD | Papers→Charts/Posters/Review Agent | ✅ MIT | Calibration of evaluation tips using real history |
| DrClaw | Micronucleic Multi-intelligent"Lobster lab." | ⚠️ | MEMORY/HISTORY Bilingual separation |
| dr-claw (OpenLAIR) | TS All-Bureau Research Station (not the same as the previous line) | ✅ GPL/AGPL | Dialogue pipeline planner + Fixed Product Directory |
| PaperClaw | Retrieval of papers in meta-skills generation Agent | ⚠️ | Rating formula is fully visible, parameters can be custom-made |
| MedgeClaw | IM→Docker A letter analysis assistant. | ⚠️ | state.json + Single HTML Zero Reliance dashboard |
| CitationClaw | Reference painting engine | ✅ CC BY-NC | 3-stage cost model (three-stage cost model)Basic/Advanced/Full）Choose and run. |
| Auto-Resubmit | Pure rules LaTeX Template Migration | ❌ | content_audit.json + The border of failure is written in the most visible place. |

### Skills bank / Prompt Collection

| Item | One word. | Permissions | One of the most interesting things to learn from. |
|---|---|---|---|
| AI-Research-SKILLs (Orchestra) | 91 A life-cycle pool of skills | ✅ MIT | frontmatter tags/dependencies + to_human/ Progress reporting |
| Awesome-Scientific-Skills | Index of skills development programmes + Quality assessor | ✅ MIT | 24 Quality of skills classified rubric（It can be built into a library. QC） |
| scientific-agent-skills (K-Dense) | 133 Skills + 100 Scientific database | ✅ MIT | scan_skills.py Repository-level skills validation CI |
| claude-scientific-writer | Writing tool to retrieve and write first | ✅ MIT | PV claim Validable Reference Checking Process |
| research-skills | 3 Skills mini-match. | ❌ | README"Skills/Description/Trigger Word"III List |
| Memento-Skills | Autoevolve agent Frame | ❌ | Skills utility score + Failed is modified |
| academic-ai-prompt | Chinese graduate students 89+ prompt Collection | ✅ MIT | Fill-in-the-Technology Acquisition Template |
| claude-howto | Claude Code Teaching library (in thousands of United States dollars)377 md） | ✅ MIT | Road map for grade learning + Single Page Quick Check |
| oh-my-claudecode | CC Heavy Enhanced Framework | ✅ MIT | level 1-4 Auto Fields + `<Use_When>` Counterfeit |
| oh-my-codex | Codex Working troposphere | ✅ MIT | missions/ Mission script as a first-class citizen. |
| system_prompts_leaks | Commercial product system tipbook leaks | ⚠️ | Structural reference only: identity→Tool Rule→Output Constraint→Red Line |

### Platform / Single Point Tool

| Item | One word. | Permissions | One of the most interesting things to learn from. |
|---|---|---|---|
| OpenScholar (AllenAI) | Retrieval for enhanced science questions and answers LM | ✅ Apache-2.0 | Quote Word by Quote + Retrieval Retrieval |
| DeepTutor (HKUDS) | Agent Native personalized tutoring platform | ✅ Apache-2.0 | Wrong title. + Read self-measured; distributed with warehouse SKILL.md |
| onyx (Original Danswer) | Enterprise level Agentic RAG Application Layer | ✅ MIT | Deep Research Planned→Multiple Retrievals→Summary reporting structure |
| OpenVitamin | Local Priority AI Platform | ✅ Apache-2.0 | Intent Rules + Skill Discovery It's a product-based process. |
| hermes-agent (Nous) | Self-improvement common Agent | ✅ MIT | Auto-settling skills after missions; alignment agentskills.io Standards |
| paperclip | More Agent"Zeros."Arranger | ✅ MIT | Budget/Cost dashboard echo"List of costs" |
| ppt-master | Document→Editable PPTX Skills | ✅ MIT | examples/ End to Sample + More Agent The entrance fits. |
| forgecode | Rust Terminal AI Encoding Environment | ✅ Apache-2.0 | Skills profile global/Item/Session Layer Overwrite |
| ipaperview | arXiv Browse+Visualize website | ❌ Custom | Templateted charts for literature measurement (trends)/United Nations Development Programme (UNDP) |
| LLM Wiki（Hashi Catalogue) | Persistence Markdown Knowledge-base philosophy | ❌ | Knowledge compilation is continuously updated, conflicting points mark |
| sherlock | Username OSINT Tools | ✅ MIT | Data file driver rules, code only for engines |
| gallery (Google) | Local cellular LLM Experience App | ✅ Apache-2.0 | Model White List/Allow filtering files |

### It's not about scientific research.

markitdown（Transfer of documents Markdown Capital)· timesfm（Time series model)· VibeVoice（Voice TTS）·
nvim-treesitter（Editor Plugin)· tdesktop（Telegram Client)· openscreen（Screen Recording)·
LiteRT-LM（Edge Logic Frame)· xiaohongshu_import（Internal language library, non-project).

## III. Clear non-absorption (position comparison)

| Practice | Who's using it? | Why don't we? |
|---|---|---|
| Automatically"Thesis." | AutoResearchClaw Wait. | Conflict with mission: beginners have to walk through the circle to grow; we keep it. gate But the default is on the ring. |
| Automatically write new skills when running and take effect immediately | ScienceClaw / Memento / hermes | Uncensored self-evolving skills undermine auditability; let's go."The monthly show. + PR + Self-examination of integrity"（CONTRIBUTING） |
| Business Hint Text Reuse | system_prompts_leaks | There's a problem with the authorized status. Just look at the structure and don't copy it. |
| None LICENSE The code for the project./Text | Top Table ⚠️/❌ Item | Legal acquiescence of retention-of-title interest; reference to public description only |

## IV. List of actions to be taken at this warehouse (in order of cost)

1. **Low cost (landed) 2026-11-09）**：13 Additional search-type skills"Minimum search source + End of story. checklist +
   Flank result visual report"Environmentally appropriate bands;START_HERE Day 4 Add"Read the self-censorship three questions."Links;
2. **Medium cost (landed) 2026-11-09）**：`scripts/check_skills_quality.py` Repository QC
   （frontmatter Hard Check + 8 Quality scoring reports) CI；ROUTING_TABLE Merger rules plus
   L0–L3 (a) Approval classification (by default at operating cost);
3. **High cost (suspension)**：claim/evidence Figure, skills utility score、references/ Loading modifications as required——
   This will be done when the scale of the skills bank and community feedback are in place; programmes and cost lists will be given as a rule before action is taken, and maintenance lists will be taken.
