# Research brief (agent prompt template)

Fill the placeholders and pass the whole thing to a `general-purpose` agent. One agent per
idea. Keep the wording otherwise identical between ideas.

---

You are researching a business idea so it can be scored and compared against other ideas
with a fixed rubric. Be sceptical: the useful output is an accurate picture of what
already exists and what could kill this idea, not a pitch for it.

**Idea id:** `{{id}}`
**Idea:** {{idea text as the user wrote it, including any description}}
**Founder context:** {{contents of founder-profile.md, or "Solo technical founder (full-stack web developer) building evenings and weekends, no existing audience, bootstrapping."}}
**Today's date:** {{date}}
**Skill directory:** `{{skill-dir}}`
**Write your output to:** `{{run-dir}}/research/{{id}}.json`

## What to find out

Use WebSearch and WebFetch. Run at least eight distinct searches, and open at least
four pages beyond the search results (competitor pricing pages, review sites, forum
threads, market reports). Listicles are a starting point, not evidence: follow them to
the product's own site to confirm pricing and positioning. If page fetches are blocked
in your environment, say so in `confidence_rationale`, run extra searches targeted at
pricing pages (`"<product> pricing"`, `site:` queries) to compensate, and cap your
confidence at `medium`.

1. **Existing products.** Find the five to eight closest products or services. For
   each: name, URL, pricing (actual numbers for the main paid tier; if pricing is hidden
   say so), positioning, main strengths, weaknesses users complain about (check reviews
   on G2, Capterra, app stores, Reddit, Product Hunt, Hacker News as relevant), and any
   traction signal (users, revenue, funding, app-store rank, review counts, launch date).
   Include indirect substitutes if people mostly solve this with spreadsheets, a
   general-purpose tool, or a manual process.
2. **Demand.** Evidence people actively want this: search volume indications, forum
   questions, job postings, "alternatives to X" articles, people building their own
   workarounds, complaints about incumbents.
3. **Market.** A sizing estimate with the source and the reasoning (top-down from a
   report, or bottom-up from number of buyers times plausible spend). Note the growth
   direction and what is driving it. Say clearly when a number is your estimate.
4. **Monetisation.** Who pays, the likely model (subscription, one-off, usage,
   marketplace fee), a defensible price point based on comparables, and anything that
   makes customers expensive to acquire or serve.
5. **Build.** What a sellable MVP would contain, a rough effort estimate for the
   founder described above, and the third-party dependencies (APIs, data sources,
   platform approvals) with their access risk.
6. **Distribution.** The concrete channels a newcomer could use to reach the first
   hundred customers and how contested they are.
7. **Risks.** Regulatory, platform, timing, and incumbent-response risks. Note any
   recent moves (last 12 months) by large players into this space.
8. **Differentiation.** Given all of the above, the angles that are actually open, and
   whether any of them compound over time.

## Scoring

Read `{{skill-dir}}/references/scoring-rubric.md` and score each criterion 1 to 5 with a
one or two sentence rationale that points at the evidence you found. Use the anchors
literally. Other agents are scoring other ideas with the same anchors, so a generous
score here makes the final comparison wrong.

## Output

Write a single JSON file to the output path above that validates against
`{{skill-dir}}/assets/idea-research.schema.json`. Read the schema before you start so you
collect everything it asks for. Do not add fields, do not omit fields, and do not wrap
the JSON in markdown fences. Before finishing, run

```
python3 {{skill-dir}}/scripts/score_ideas.py {{run-dir}}
```

and fix anything it reports for your file (ignore messages about other ideas' files).

Notes on the fields:

- `sources` needs at least six entries and every existing product must have its URL
  in `sources` too. `used_for` says which claim the source supports.
- `confidence` describes the evidence quality, not the idea quality. Use `low` if
  pricing was hidden or market sizing is guesswork.
- `kill_risks` should be specific enough that someone could go and check them.
- Leave `calibration_notes` as an empty array; it is filled in later.

Finish by replying with the idea id, the weighted total you expect, the confidence
label, and the two facts you found that most surprised you. Nothing else.
