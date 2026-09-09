# Business idea comparison: {{batch title}}

**Date:** {{YYYY-MM-DD}}
**Ideas evaluated:** {{n}}
**Founder context:** {{one line: from founder-profile.md, or the default solo-developer assumption}}

## Executive summary

{{Name the winner and the runner-up. Two or three sentences on why the winner leads,
grounded in the strongest evidence found. One sentence on what new information would
change the ranking. If the winner is low confidence, say the ranking is provisional.}}

## Ranking

{{paste comparison.md here}}

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

#### Demand and market

{{Demand signals as a short bulleted list. Then the market size estimate, how it was
derived, whether it is the agent's own estimate, and the growth direction.}}

#### Monetisation

{{Payer, model, defensible price point, comparable pricing, what makes customers
expensive to acquire or serve.}}

#### Build and go-to-market

{{MVP scope in a sentence or two. Effort estimate. Dependencies with their access risk.
Distribution channels a newcomer could use.}}

#### Scorecard

| Criterion | Score | Rationale |
|---|---|---|
{{one row per criterion, in rubric order}}

{{If calibration_notes is non-empty, list the adjustments here so the reader can see
where the raw research score was changed and why.}}

#### Kill risks

{{Bulleted, specific, checkable. Include recent moves by large players.}}

#### What would need to be true

{{Two or three assumptions the idea depends on, phrased so each can be tested.}}

#### Sources

{{Markdown links, one per line, with what each was used for.}}

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
possible), scored 1 to 5 on eight weighted criteria, then calibrated across ideas so
equal scores mean equal things. Confidence describes evidence quality, not idea
quality. Weights: {{weights}}. Raw research, including all sources, is in `research/`
next to this report.
