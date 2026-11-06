---
name: analyze-results
description: Analyze ML experiment results, compute statistics, generate comparison tables and insights. Use when user says "analyze results", "compare", or needs to interpret experimental data.
argument-hint: "[results-path-or-description]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# Analyze Experiment Results

Analyze: $ARGUMENTS

## Workflow

### Step 1: Locate Results
Find all relevant JSON/CSV result files:
- Check `figures/`, `results/`, or project-specific output directories
- Parse JSON results into structured data

### Step 2: Build Comparison Table
Organize results by:
- **Independent variables**: model type, hyperparameters, data config
- **Dependent variables**: primary metric (e.g., perplexity, accuracy, loss), secondary metrics
- **Delta vs baseline**: always compute relative improvement

### Step 3: Statistical Analysis
- If multiple seeds: report mean +/- std, check reproducibility
- If sweeping a parameter: identify trends (monotonic, U-shaped, plateau)
- Flag outliers or suspicious results

### Step 4: Generate Insights
For each finding, structure as:
1. **Observation**: what the data shows (with numbers)
2. **Interpretation**: why this might be happening
3. **Implication**: what this means for the research question
4. **Next step**: what experiment would test the interpretation

### Step 5: Update Documentation
If findings are significant:
- Propose updates to project notes or experiment reports
- Draft a concise finding statement (1-2 sentences)

## Output Format
Always include:
1. Raw data table
2. Key findings (numbered, concise)
3. Suggested next experiments (if any)

## 环境适配（QoderWake 安装时追加）
- 本 Skill 的原文与支持文件（scripts/、references/、以及同级 ../shared-references/）源目录为：D:\skills\Auto-claude-code-research-in-sleep-main\Auto-claude-code-research-in-sleep-main\skills\analyze-results\n- 执行脚本或读取参考文件时，请以该源目录解析相对路径；SkillStore 中仅保存本 SKILL.md 正文。
