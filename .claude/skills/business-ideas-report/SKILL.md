---
name: business-ideas-report
description: Research, score and compare a list of business or product ideas, producing a ranked markdown report backed by web research into existing products, competitors, pricing, market size and risks. Use this whenever the user gives you two or more ideas and wants them evaluated, compared, ranked, scored, validated, or wants a "report" / "analysis" / "which should I build" answer about them, even if they don't say "business idea" explicitly (side project ideas, SaaS ideas, app ideas, startup ideas all count). Also use it for a single idea when the user wants a researched viability assessment.
---

# Business ideas report

Turn a list of ideas into one ranked comparison report. Each idea gets the same
research treatment and the same scoring rubric so the ranking reflects the ideas,
not which one happened to get the most attention.

The user's ideas are usually rough one-liners. The value you add is
(1) finding out what already exists and how it is priced, (2) sizing the demand honestly,
and (3) being blunt about the reasons an idea would fail. A report that scores everything
3.5 out of 5 is useless; differentiate.

## Inputs

Ideas arrive one of three ways. Take the first that applies:

1. Inline arguments: `/business-ideas-report idea one; idea two; idea three`
   (split on `;` or newlines).
2. A file path argument: a markdown or text file with one idea per bullet, numbered line
   or plain line. Blank lines and headings are ignored. A bullet may carry a short
   description after a `-` or `:`; keep it, it is useful context.
3. No argument: read `docs/business-ideas/ideas.md` if it exists, otherwise ask the user
   for the ideas.

Also read `docs/business-ideas/founder-profile.md` if it exists and has been filled in
(not just the template placeholders). It feeds the founder-fit criterion. Without it,
score founder fit as a solo technical founder building evenings and weekends, and say so
in the report.

## Workflow

### 1. Set up the run directory

```
docs/business-ideas/<YYYY-MM-DD>-<short-slug>/
  research/      one JSON file per idea, written by the research agents
  scores.json    produced by the scoring script
  comparison.md  produced by the scoring script
  report.md      the deliverable
```

The slug is two or three words describing the batch (`saas-tools`, `fitness-apps`).
Give each idea a stable kebab-case id (`ai-invoice-chaser`); it names the research
file and is used throughout.

### 2. Research every idea in parallel

Spawn one `general-purpose` agent per idea, all in the same message so they run
concurrently. Five or more ideas: send them in batches of four so the searches don't
starve each other.

Each agent's prompt is the template in `references/research-brief.md` with the idea,
the id, the output path, and the founder context filled in. The brief tells the agent
what to look for, the minimum number of searches, and the exact JSON shape
(`assets/idea-research.schema.json`) to write. Fill in `{{skill-dir}}` with the absolute path of this skill. Don't paraphrase the brief; the
consistency of the report depends on every agent getting the same instructions.

Agents research independently and therefore score independently. That is fine for
evidence gathering but means their scores are not yet comparable; step 4 fixes that.

### 3. Score and validate

```
python3 .claude/skills/business-ideas-report/scripts/score_ideas.py <run-dir>
```

The script validates every research file against the schema (missing fields, scores
outside 1 to 5, fewer than the required sources), computes weighted totals from the
rubric weights, ranks the ideas and writes `scores.json` and `comparison.md`.

If it reports validation errors, re-run the affected agent with the error message
appended to its prompt rather than patching the JSON by hand; a hand-patched file
usually hides a research gap.

### 4. Calibrate across ideas

Read all the research files together and check that equal scores mean equal things.
Common drift: one agent gives a 4 for "competition" to a market with fifteen funded
incumbents because it found a niche, another gives a 2 to a market with three small
players. Use the anchors in `references/scoring-rubric.md` as the tie-breaker and adjust
the `score` values in the research JSON directly, recording every change in that file's
`calibration_notes` array with the reason. Re-run the script after adjusting.

Also sanity-check the evidence. An agent that claims a market size should cite where the
number came from; a competitor list with no pricing usually means the agent stopped at
the first listicle. Send it back for a second pass if the gaps would change the score.

### 5. Write the report

Fill in `assets/report-template.md` and save it as `report.md` in the run directory.
The template's structure is fixed so reports are comparable across runs; the content
should be specific and opinionated. Rules that keep it useful:

- The executive summary names a winner, says why in two or three sentences, and states
  what new information would change the ranking.
- Every existing-product table has pricing. "Freemium" alone is not pricing; give the
  paid tier's price.
- Every score in a scorecard has a one-line rationale that points at evidence.
- Kill risks are concrete ("Apple ships this natively in iOS 27", "requires FCA
  authorisation") not generic ("competition is high").
- Next steps are cheap validation experiments for the top one or two ideas, each with
  a success threshold, not "build an MVP".
- Sources are listed per idea as markdown links. Every factual claim in the deep-dive
  should be traceable to one.

Numbers belong in tables, not prose. Keep each deep-dive to roughly a page.

### 6. Deliver

Tell the user the report path, the ranking with totals, and the single most important
caveat about the research quality (for example, a market where pricing is hidden behind
"contact sales" so unit economics are a guess). Offer to publish the report as a shareable
Artifact page in one line; do so only if they want it.

Commit the run directory when the user asks for a commit; the research JSON is part of
the record and should be committed alongside the report.

## Reference files

- `references/scoring-rubric.md`: the eight criteria, their weights and the 1 to 5
  anchors. Read it before calibrating.
- `references/research-brief.md`: the prompt template for the research agents.
- `assets/idea-research.schema.json`: the JSON shape every research file must follow.
- `assets/report-template.md`: the report structure.
- `scripts/score_ideas.py`: validation, weighting, ranking. Run with `--help` for options.
