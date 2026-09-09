# Comparative scoring pass

Research agents score their own idea in isolation, and isolated scorers drift: one
gives a 4 to a market with fifteen funded incumbents because it found a niche, another
gives a 2 to a market with three small players. The fix is to score all ideas together,
one criterion at a time, and to order before assigning.

Do this pass after every research file validates and before writing the report. It is
the main agent's job (or a single dedicated agent's), never split across agents.

## Procedure

1. Read every research file in full. Have `references/scoring-rubric.md` open.
2. For each criterion in rubric order:
   1. List the ideas from weakest to strongest on that criterion, using only the
      evidence in the research files. Write one line per idea saying why it sits
      where it does.
   2. Assign anchor scores to the ordered list. Ties are fine when the evidence is
      genuinely similar; gaps of two or more need a reason. Two ideas should never
      have the same score if you just ranked one clearly above the other.
   3. Grade the evidence for each score (`strong`, `moderate`, `weak`) by what the
      research file actually cites, not by how confident the rationale sounds. A score
      that rests on the researcher's own estimate is `weak`; on a report mill or a
      single listicle, `weak`; on two independent snippets or a vendor page, `moderate`
      or `strong` depending on whether the page was read or quoted.
   4. Compare with the researcher's proposed score. Where you differ by one, keep
      yours. Where you differ by two or more, re-read the evidence: either the
      researcher missed the anchors or you missed something in the file.
3. Write the final `score`, `evidence` and `rationale` into each research file's
   `scores` block. For every change from the researcher's score, append a line to that
   file's `calibration_notes`: criterion, old and new score, and the reason in one
   sentence.
4. Re-run `scripts/score_ideas.py`. Read the sensitivity section it prints: if the
   top two are within a single one-point change of swapping, the report must say so.

## Things that go wrong

- **Scoring the market instead of the idea.** `market_size` is the serviceable segment
  for this idea, not the parent category the researcher found a number for.
- **Letting whitespace and differentiation move together.** They measure different
  things: how well served the customer is today, and whether this entrant has a
  persistent edge. A saturated market with a structural wedge is 2 and 4, not 2 and 2.
- **Rewarding confident prose.** A rationale that reads well is not evidence. Check
  what the sources list actually contains before grading `strong`.
- **Softening gates.** If the honest score on a gate criterion is 1, give it a 1. The
  report explains what would lift the gate; the score does not pretend.
- **Forgetting the founder profile.** `founder_fit` and the weight profile come from
  the profile file. If it is unfilled, score fit 3, grade `weak`, use `bootstrap-side`,
  and say so in the report.
