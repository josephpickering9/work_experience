# Business idea comparison: {{batch title}}

**Date:** {{YYYY-MM-DD}}
**Ideas evaluated:** {{n}}
**Founder context:** {{one line: from founder-profile.md, or the default solo-developer assumption}}
**Weight profile:** {{bootstrap-side | bootstrap-full-time | venture, and why}}

## Executive summary

{{Name the winner and the runner-up. Two or three sentences on why the winner leads,
grounded in the strongest evidence found. One sentence on what new information would
change the ranking. State the top-two margin and whether a single one-point change or a
different weight profile would swap them. If the winner is low confidence, say the
ranking is provisional. Name any gated ideas and what would lift the gate.}}

## Ranking

{{paste comparison.md here, including the weakest-criterion, per-profile and
sensitivity sections}}

## Idea deep-dives

{{One section per idea, in rank order. Repeat the block below.}}

### {{rank}}. {{Idea name}} ({{total}}/100, {{confidence}} confidence)

**One-liner:** {{one_liner}}
**Target customer:** {{target_customer}}

#### What already exists

| Product | Type | Pricing | Positioning | Where it falls short |
|---|---|---|---|---|
{{one row per existing product}}

{{One short paragraph: how well served the target customer is today and where the gap is.}}

#### Demand, frequency and market

{{Demand signals as a short bulleted list. How often the need recurs and what
comparables show about retention. Then the market size estimate for this idea's
segment, how it was derived, whether it is the agent's own estimate, and the growth
direction.}}

#### Monetisation

{{Payer, model, defensible price point, comparable pricing, what makes customers
expensive to acquire or serve.}}

#### Build and go-to-market

{{MVP scope in a sentence or two. Effort estimate. Dependencies with their access risk.
Distribution channels a newcomer could use.}}

#### Scorecard

| Criterion | Score | Evidence | Rationale |
|---|---|---|---|
{{one row per criterion, in rubric order}}

{{If calibration_notes is non-empty, list the adjustments here so the reader can see
where the raw research score was changed and why.}}

#### Why now

{{One short paragraph from the research's why_now field. "Nothing has changed" is a
legitimate and important answer.}}

#### Kill risks

{{Bulleted, specific, checkable. Include recent moves by large players. If the idea is
gated, the first bullet says which criterion gated it and what would lift it.}}

#### What would need to be true

{{Two or three assumptions the idea depends on, phrased so each can be tested.}}

#### Sources

{{Markdown links, one per line, with what each was used for. Include every source a
claim in this deep-dive rests on; if the research file has many more, say how many and
point to it rather than pasting them all.}}

## Cross-cutting observations

{{Patterns across the batch: shared risks, a criterion where every idea is weak, an
idea that is really a feature of another, markets that are converging. Keep it to what
would change a decision.}}

## Recommended next steps

{{For the top one or two ideas: cheap validation experiments with a success threshold
and rough cost in time or money. For example: "Post a landing page with pricing to
r/smallbusiness and two Facebook groups; proceed if 30 of the first 300 visitors leave
an email." Not "build an MVP".}}

## Method

Each idea was researched independently by an agent following a fixed brief (at least
eight web searches, competitor pricing verified on the vendor's own site where
possible). All ideas were then scored together, one criterion at a time, on ten
criteria with 1 to 5 anchors and an evidence grade per score. Weakly evidenced scores
are pulled towards the midpoint before weighting; a 1 on problem severity, monetisation,
feasibility or timing gates an idea below all ungated ideas. Weight profile
`{{profile}}`: {{weights}}. Confidence describes evidence quality, not idea quality. Raw
research, including all sources and every score change, is in `research/` next to this
report.
