# Scoring rubric

Eight criteria, each scored 1 to 5. Weights sum to 100, so the weighted total
(`sum(score * weight) / 5`) is out of 100. The weights favour demand, market and
money over build effort because a technical founder can usually build almost
anything; what they can't do is conjure customers.

| Key | Criterion | Weight | What it measures |
|---|---|---|---|
| `problem_severity` | Problem severity and demand evidence | 15 | Is this a real, painful, frequent problem that people already try to solve? |
| `market_size` | Market size and growth | 15 | How many buyers exist, what they spend, and which way that is trending |
| `competition` | Competitive whitespace | 15 | How crowded the space is and how well-served the target customer already is. A high score means there is room |
| `differentiation` | Differentiation and defensibility | 10 | Whether the idea has an angle incumbents can't or won't copy, and whether that angle compounds |
| `monetisation` | Monetisation and unit economics | 15 | Will people pay, how much, how often, and what does it cost to acquire and serve them |
| `feasibility` | Feasibility and time to MVP | 10 | Effort and risk to ship a sellable first version, including third-party dependencies |
| `distribution` | Go-to-market and distribution | 10 | Is there a clear, affordable way to reach the first hundred customers |
| `founder_fit_and_risk` | Founder fit and external risk | 10 | Does the founder's profile suit this, and what regulatory, platform, or timing risks sit outside their control |

## Anchors

Use the anchors literally. The anchors exist so that two ideas researched by two
different agents end up on the same scale; when a score sits between anchors, round
towards the more evidenced one.

### problem_severity
- **1** Nobody is looking for a solution. No searches, forums, or spend on workarounds.
- **2** Mild annoyance. Some complaints exist but people live with it.
- **3** Real problem with visible workarounds (spreadsheets, manual processes, half-fit tools).
- **4** Frequent, costly problem. People already pay for partial solutions or hire around it.
- **5** Urgent, expensive, recurring. Evidence of budgets, job titles, or regulation dedicated to it.

### market_size
- **1** A few hundred potential buyers, or a hobby market with no spend.
- **2** Small niche; a good outcome is a lifestyle business.
- **3** Mid-sized market able to support several million in revenue for a small player.
- **4** Large and growing; established players report meaningful revenue.
- **5** Very large or fast-growing with public evidence (funding rounds, analyst sizing, category leaders at scale).

### competition
- **1** Dominated by well-funded incumbents with strong distribution; the target customer is well served.
- **2** Several established players; only a narrow underserved segment is visible.
- **3** Crowded but fragmented; incumbents have clear, repeatedly cited weaknesses.
- **4** A handful of small or neglected competitors; obvious unmet needs.
- **5** No direct competitor; nearest substitutes are manual processes or general-purpose tools.

Beware of scoring a market 4 or 5 because nothing exists: sometimes nothing exists because
there is no demand. Cross-check against `problem_severity`.

### differentiation
- **1** Feature-level difference an incumbent could copy in a sprint.
- **2** Positioning or UX difference; copyable but takes effort.
- **3** A distinct wedge (segment, workflow, integration, price point) incumbents are unlikely to prioritise.
- **4** Structural advantage: proprietary data, a network effect, a distribution channel, or a regulatory moat that builds over time.
- **5** Multiple compounding advantages that get stronger with each customer.

### monetisation
- **1** No plausible payer, or price would need to be near zero.
- **2** Willingness to pay is unproven and comparables are free or ad-supported.
- **3** Clear payer and comparable pricing exists, but margins or churn are uncertain.
- **4** Comparables show sustained paid demand at a price that supports acquisition costs.
- **5** High-value, recurring, low-churn revenue with evidence of expansion within accounts.

### feasibility
- **1** Requires hardware, deep research, or a regulated licence before anything ships.
- **2** Many months of work or a critical dependency on an API or partner that could refuse access.
- **3** A few months for a solo developer; standard stack; some integration risk.
- **4** Weeks to a sellable MVP using well-documented services.
- **5** Days to a sellable MVP; the hard part is entirely distribution.

### distribution
- **1** No identifiable channel; buyers are dispersed and unreachable without a sales team.
- **2** Channels exist but are expensive or saturated (paid ads in a crowded category).
- **3** Reachable communities, marketplaces, or SEO terms with moderate competition.
- **4** A concentrated, accessible channel (a marketplace, an app store category, an active community) where a newcomer can get noticed.
- **5** Built-in distribution: a partner, an existing audience, virality, or a marketplace with obvious demand and weak supply.

### founder_fit_and_risk
- **1** Poor fit and a serious external risk (regulation, platform dependence, timing).
- **2** Either poor fit or a meaningful external risk.
- **3** Adequate fit; external risks are manageable.
- **4** Good fit; the founder has relevant experience, network, or domain knowledge.
- **5** Excellent fit with no notable external risk; the founder would be a credible operator in this space.

## Confidence

Every idea also gets a confidence label describing the quality of the evidence, not the
quality of the idea:

- **high**: pricing, competitor traction, and market sizing all found from primary or
  reputable secondary sources.
- **medium**: most facts found, but at least one important number is an estimate.
- **low**: pricing hidden, market size unknown, or the agent relied mostly on listicles
  and vendor marketing.

Low-confidence ideas should not rank first without the report saying that the ranking
is provisional.
