# Scoring rubric

Ten criteria, each scored 1 to 5 against the anchors below, each tagged with an
evidence grade. The script turns these into a raw total, an evidence-adjusted total, and
gate flags. Ideas rank on the adjusted total, with gated ideas below all ungated ones.

## Why the design looks like this

A plain weighted sum lets a strong market score paper over "nobody will pay" or "needs a
licence you cannot get". So three criteria are gates: a 1 on any of them flags the idea
as blocked and drops it below every unblocked idea, whatever its total.

A 4 backed by a 2,000-respondent survey and a 4 backed by a vendor's homepage are not
the same fact. Each score therefore carries an evidence grade, and the adjusted score
shrinks weakly evidenced scores towards the neutral midpoint of 3. That rewards
research, not optimism, and stops a confident guess from winning the ranking.

Weights depend on who is building. A side-project bootstrapper needs revenue in months
from something that ships in weeks; a venture-scale founder needs a large market and a
durable edge. Pick a weight profile that matches the founder rather than pretending one
set of weights fits everyone.

## Criteria and weights

| Key | Criterion | Gate | bootstrap-side | bootstrap-full-time | venture |
|---|---|---|---|---|---|
| `problem_severity` | Problem severity | yes | 12 | 12 | 12 |
| `market_size` | Market size and growth | | 8 | 12 | 18 |
| `competition` | How well served the customer is today | | 12 | 12 | 10 |
| `differentiation` | The entrant's durable edge | | 8 | 10 | 14 |
| `monetisation` | Willingness to pay and unit economics | yes | 14 | 14 | 10 |
| `retention` | Frequency of need and expected retention | | 10 | 10 | 8 |
| `feasibility` | Time and risk to a sellable first version | yes | 12 | 8 | 4 |
| `distribution` | Reaching the first hundred customers | | 12 | 10 | 8 |
| `founder_fit` | Founder fit and motivation | | 6 | 6 | 8 |
| `timing_and_risk` | Why now, and external risk | yes | 6 | 6 | 8 |

Each column sums to 100. `bootstrap-side` is the default: a solo founder building
around a job, no outside money. `bootstrap-full-time` is a founder who can work on it
full time for six to twelve months. `venture` is a founder who intends to raise and
needs a large outcome.

Total = sum(score x weight) / 5, out of 100.

## Evidence grades

Tag every score with the strength of the evidence behind it:

| Grade | Meaning | Adjustment |
|---|---|---|
| `strong` | Primary or reputable quantitative sources: vendor pricing pages, surveys with stated samples, filings, app-store review counts, funding announcements | none |
| `moderate` | Secondary sources that agree, or a primary source for part of the claim: comparison sites corroborated by two snippets, analyst reports, reasoned bottom-up estimates with stated inputs | score pulled 25% of the way towards 3 |
| `weak` | Inference, vendor marketing, a single listicle, or the researcher's own guess | score pulled 50% of the way towards 3 |

Adjusted score = 3 + (score - 3) x factor, where factor is 1.0, 0.75 or 0.5. A weakly
evidenced 5 becomes a 4; a weakly evidenced 1 becomes a 2. Grades matter most at the
extremes, which is the point: extreme scores need to earn it.

## Gates

A score of 1 on `problem_severity`, `monetisation`, `feasibility` or `timing_and_risk`
flags the idea as gated. Gated ideas still get a total, but rank below every ungated
idea, and the report must say what would need to change to lift the gate.

## Anchors

Use the anchors literally. They exist so two ideas scored by two different people land
on the same scale. When a score sits between anchors, round towards the one with better
evidence. Each anchor block ends with what evidence would justify a 4 or 5, so a high
score without that evidence should be graded `weak`.

### problem_severity (gate)
Frequency x intensity x what people already spend to cope.
- **1** Nobody is looking for a solution. No searches, forums, or spend on workarounds.
- **2** Mild annoyance. Some complaints exist but people live with it.
- **3** Real problem with visible workarounds (spreadsheets, manual processes, half-fit tools).
- **4** Frequent, costly problem. People already pay for partial solutions or pay someone to handle it.
- **5** Urgent, expensive, recurring. Evidence of budgets, job titles, or regulation dedicated to it.

Evidence for 4 or 5: surveys with sample sizes, paid substitutes with prices, hourly
rates for people hired to do it, regulation naming the problem.

### market_size
Serviceable market for this idea's segment, not the parent category. State the parent
category figure separately if it is the only thing that exists.
- **1** A few hundred potential buyers, or a hobby market with no spend.
- **2** Serviceable market under roughly $10M a year; a good outcome is a lifestyle business.
- **3** $10M to $100M a year; several small players can each reach low single-digit millions.
- **4** $100M to $1B a year and growing; established players report meaningful revenue.
- **5** Over $1B a year or growing over 20% a year, with public evidence (funding rounds, analyst sizing, category leaders at scale).

Evidence for 4 or 5: analyst sizing from a named report, funding rounds and revenue of
category players, a bottom-up estimate with stated buyer counts and spend. A number
pulled from a report mill with no method is `weak`.

### competition
How well served the target customer is today. This is about the customer's current
options, not about the entrant. A high score means the customer is poorly served.
- **1** Well-funded incumbents with strong distribution serve the target customer well; complaints are minor.
- **2** Several established players; only a narrow segment is visibly underserved.
- **3** Crowded but fragmented; incumbents have clear, repeatedly cited weaknesses the customer cares about.
- **4** A handful of small or neglected competitors; obvious unmet needs with evidence customers notice them.
- **5** No direct competitor; nearest substitutes are manual processes or general-purpose tools, and customers complain about them.

Beware of a 4 or 5 because nothing exists: sometimes nothing exists because there is no
demand. Cross-check against `problem_severity`. Evidence for 4 or 5: review-site
complaint themes, "alternative to X" search demand, customers building their own tools.

### differentiation
The entrant's advantage, and whether it persists. This is about the proposed product,
not the market. A crowded market can still have a 4 here if the wedge is structural.
- **1** Feature-level difference an incumbent could copy in a sprint, or no stated difference.
- **2** Positioning or UX difference; copyable but takes effort.
- **3** A distinct wedge (segment, workflow, integration, price point) incumbents are unlikely to prioritise.
- **4** Structural advantage: proprietary data, a network effect, a distribution channel, or a regulatory moat that builds over time.
- **5** Multiple compounding advantages that get stronger with each customer.

Evidence for 4 or 5: a specific asset the founder controls, or a mechanism by which
the advantage grows with usage. "We will execute better" is a 1.

### monetisation (gate)
- **1** No plausible payer, or price would need to be near zero.
- **2** Willingness to pay is unproven and comparables are free or ad-supported.
- **3** Clear payer and comparable pricing exists, but margins or acquisition cost are uncertain.
- **4** Comparables show sustained paid demand at a price that supports the likely acquisition cost.
- **5** High-value, recurring, low-churn revenue with evidence of expansion within accounts.

Evidence for 4 or 5: comparable products' published prices and revenue or subscriber
figures, gross-margin logic that accounts for serving cost and platform fees.

### retention
How often the need recurs and how long a customer plausibly stays. Distinct from
monetisation: this is about the shape of usage, not the price.
- **1** One-off need; the customer has no reason to return after the first use.
- **2** Episodic need (a few times a year) with no reason to stay subscribed in between.
- **3** Regular need (monthly) or a product that becomes part of a routine for some users.
- **4** Weekly or daily use with switching costs (data, integrations, habit, team adoption).
- **5** Embedded in a workflow or system of record; leaving is painful and comparables show multi-year retention.

Evidence for 4 or 5: comparable products' retention or churn figures, the nature of the
data the product accumulates, integration depth.

### feasibility (gate)
For the founder described in the profile, not a generic team.
- **1** Requires hardware, deep research, or a regulated licence or partner consent before anything can be sold.
- **2** Many months of work, or a critical dependency on an API or partner that could refuse access.
- **3** A few months; standard stack; some integration risk.
- **4** Weeks to a sellable MVP using well-documented services.
- **5** Days to a sellable MVP; the hard part is entirely distribution.

Evidence: a listed MVP scope and dependency table with access risks. A high score with
an unlisted high-risk dependency is wrong, not weakly evidenced.

### distribution
- **1** No identifiable channel; buyers are dispersed and unreachable without a sales team.
- **2** Channels exist but are expensive or saturated relative to the price point.
- **3** Reachable communities, marketplaces, or search terms with moderate competition.
- **4** A concentrated, accessible channel where a newcomer can get noticed, and the price point supports the likely acquisition cost.
- **5** Built-in distribution: a partner, an existing audience, virality, or a marketplace with obvious demand and weak supply.

Evidence for 4 or 5: named channels with a reason to believe they are open (search
results showing few competitors, community size, a partner conversation, an audience
the founder actually has).

### founder_fit
Read from the founder profile. Without a filled-in profile, score 3 and grade `weak`.
- **1** The founder lacks the skills to build it and the domain knowledge to sell it.
- **2** Can build it but has no domain knowledge, network, or stated interest in the space.
- **3** Adequate: can build it, some interest, no particular advantage.
- **4** Relevant experience, network, or domain knowledge; the founder would be credible to customers.
- **5** The founder has lived the problem, has an audience or network of buyers, and wants to work on it for years.

### timing_and_risk (gate)
Why now, and what outside the founder's control could end it.
- **1** A regulatory, legal, or platform barrier makes it unsellable, or the window has clearly closed.
- **2** A meaningful external risk (pending regulation, platform dependence, an incumbent that has announced this) with no mitigation.
- **3** No strong reason it is now rather than three years ago; risks are manageable.
- **4** A clear enabling shift (new technology, regulation, behaviour change) within the last two years and no serious external risk.
- **5** A shift that makes this newly possible and newly demanded, with incumbents structurally unable to follow quickly.

Evidence for 4 or 5: a dated event (regulation, platform change, API launch, cost
curve) and a reason incumbents cannot simply respond.

## Confidence

Each idea also carries an overall confidence label describing the research, separate
from the per-criterion grades:

- **high**: most criteria graded `strong`; pricing, traction and sizing found from primary or reputable secondary sources.
- **medium**: mixed grades; at least one important number is an estimate.
- **low**: mostly `moderate` and `weak`; pricing hidden, sizing guessed, or page access blocked.

Low-confidence ideas should not rank first without the report saying the ranking is
provisional and naming the research that would firm it up.
