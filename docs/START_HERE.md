# Start a research project

This quickstart creates a local Athena project, records one completed step with
an artifact, exports a private Research Release draft, and verifies it offline.
It uses the repository's synthetic CSV, so no API key, GPU, or network service
is required after cloning.

> Athena Alpha is a control plane. The CLI stores state and enforces release
> gates; it does not run a model. For real work, your compatible local agent
> reads the action returned by `resume` and creates the artifact.

## 1. Clone Athena

Requirements: Git and Python 3.10 or newer.

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
cd Athena
python -m athena --version
```

Run the remaining commands from this checkout.

## 2. Create a local project

```bash
python -m athena init athena-demo --name "My first Research Release"
```

Athena creates `athena-demo/.athena/`. Nothing is uploaded.

## 3. Create a source-backed artifact

```bash
python docs/demo_assets/verify_demo.py > athena-demo/demo-verification.txt
```

Open `athena-demo/demo-verification.txt`. It should end with `PASS` and show
the per-seed differences plus `1.17 +/- 1.84`. This artifact verifies the
fixture's arithmetic only; it is not an end-to-end model audit.

## 4. Plan one bounded task

```bash
python -m athena plan --project athena-demo "Verify the supplied result and document its limits" --source docs/demo_assets/demo_results.csv --skill research-integrity-pipeline --json
```

Copy the printed `task_id`. This explicit route has one step,
`01-research-integrity-pipeline`.

Inspect the stable next action:

```bash
python -m athena resume --project athena-demo --json
```

For this narrow fixture, the verification output from step 3 is the artifact.
For your own paper or dataset, complete the returned instruction in your local
agent and save its real output before continuing.

For an automated host, the JSON action includes an absolute
`result_contract.artifact_path`. Write the completed result to that exact path,
then execute `checkpoint_argv` as an argument array without a shell (preferred),
or run the self-contained `checkpoint_command`. Do not replace placeholders or
append arguments; both returned forms are already complete.

## 5. Checkpoint completed work

Replace `<task-id>` with the value printed by `plan`:

```bash
python -m athena checkpoint --project athena-demo --task <task-id> --step 01-research-integrity-pipeline --artifact athena-demo/demo-verification.txt --note "Offline arithmetic check; no model execution or external source verification."
```

Athena copies the artifact into local project state and records its SHA-256.
Do not checkpoint planned, partial, or failed work.

Confirm that the task is `complete`, not `planned` or `in_progress`:

```bash
python -m athena status --project athena-demo --task <task-id> --json
```

## 6. Export only after the gate passes

Export is allowed only when:

- every planned step has status `complete`;
- at least one artifact is registered; and
- every registered artifact still exists and matches its recorded size and
  SHA-256.

With those conditions met:

```bash
python -m athena export --project athena-demo --task <task-id> --release-version 0.1.0 --title "Verified paired-result fixture" --json
```

The command creates an immutable draft under
`athena-demo/.athena/releases/`. Its default visibility is
`private-local-draft`; export does not publish or upload it.

## 7. Verify the release offline

Replace `<release-directory>` with the directory printed by `export`:

```bash
python -m athena verify <release-directory> --json
```

A successful verification checks the manifest and bundled files. You now have
a source-linked, versioned Research Release draft.

## Use your own question, paper, or dataset

Create a separate project and repeat the loop:

```bash
python -m athena init my-study --name "My study"
python -m athena plan --project my-study "Audit the central claims and identify unsupported conclusions" --source https://example.org/paper.pdf
python -m athena resume --project my-study --json
```

`--source` accepts a local file or an HTTP(S) reference and can be repeated.
Local files are fingerprinted; URL references are recorded but not fetched by
the Alpha CLI. Replace the example URL with a real paper URL, or use a local
path that already exists. Routing can select a bounded subset for the goal;
the canonical order across all three core stages is `citation-tracing` →
`research-integrity-pipeline` → `explorable-paper` → Research Release.
Actual browsing, model calls, code execution, and credentials belong to the
local agent and tools you choose.

Continue with `resume → execute locally → save artifact → checkpoint` until
status is `complete`; only then run `export`.

## Next

- [Research Bot Alpha contract](RESEARCH_BOT_ALPHA.md)
- [Install skills for a compatible agent](INSTALL_ONCE.md)
- [Open the synthetic damped-oscillator release](examples/damped-oscillator.html)
- [Understand current validation boundaries](VALIDATION.md)
