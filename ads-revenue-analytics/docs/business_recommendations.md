# Business recommendations

**Period:** July 2024 – December 2025 · **Revenue:** $566.3M · **Blended ROAS:** 3.30x

Every figure below is produced by `sql/02_analysis.sql` and reproducible with
`python analysis/run_analysis.py`. The query behind each claim is named so it
can be checked.

---

## The headline is hiding two problems

Revenue grew 9.9% half-over-half — $184.0M in the first six months to $202.2M
in the last six. On that number alone the business looks healthy.

It is not the whole picture:

| | First month | Last month | Change |
|---|---|---|---|
| Active advertisers | 199 | 138 | **−31%** |
| Revenue per advertiser | $144,681 | $278,565 | **+93%** |

*(Q1 — executive summary)*

**All of the growth is coming from existing accounts spending more, on a base
that is contracting by roughly a third.** ARPA nearly doubling is not a
success story on its own; it is what revenue concentration looks like while it
is happening. The top revenue decile — 31 advertisers — now carries 66.8% of
revenue, and the top two deciles carry 83.2% *(Q6)*.

That is the single most important thing on this page. Two specific problems
sit underneath it.

---

## 1. Gaming is in structural decline, and it is being masked

**Finding.** Comparing the most recent three months against the prior three,
total revenue rose $17.2M. Within that, declining segments removed $4.9M, and
the largest single drag is Southeast Asia Gaming: −$1.21M, −33.7%, taking 7.0
percentage points off the total change on its own *(Q3)*.

Gaming declines are not confined to one market:

| Segment | Change | % change |
|---|---|---|
| Southeast Asia · Gaming | −$1,205,536 | −33.7% |
| North America · Gaming | −$685,522 | −31.7% |
| Australia & NZ · Gaming | −$444,877 | −65.4% |
| Japan & Korea · Gaming | −$180,646 | −14.5% |

Four of the five regions show Gaming contracting. Only Europe grew *(+47.1%)*.

**This is independently corroborated by a different query.** The churn
watchlist *(Q12)*, built with no knowledge of the segment analysis, returns 10
at-risk accounts carrying $2.84M — and 6 of the 10 are Gaming advertisers, 5 of
them in Southeast Asia. Two unrelated cuts of the data land on the same root
cause, which is a much stronger signal than either alone.

**Recommendation.**
1. Treat the Gaming book as a retention problem, not a performance problem —
   Gaming ROAS is 2.68x, below the 2.95x vertical average, so advertisers are
   getting weaker returns and responding rationally.
2. Commission a competitive review specifically for SEA Gaming before the next
   quarter's targets are set. A −34% segment trend that continues will remove
   roughly $2.4M annualised.
3. Do not set next quarter's regional targets from the blended growth rate.
   It is currently averaging a growing E-commerce book against a shrinking
   Gaming one, and will over-target the markets where Gaming concentrates.

---

## 2. The account base is shrinking because SMB retention is broken

**Finding.** Churn is severe and heavily tiered *(Q5)*:

| Tier | Advertisers | % of revenue | Churn rate | Revenue per advertiser |
|---|---|---|---|---|
| Enterprise | 42 | 72.5% | 16.3% | $9,770,015 |
| Mid-Market | 103 | 24.2% | 44.4% | $1,329,444 |
| SMB | 162 | 3.4% | **82.5%** | $117,601 |

SMB is 48% of the account base and 3.4% of revenue, churning at 82.5%.

**Recommendation — and a caution.** The obvious read is "fix SMB retention."
The number that matters is the second column: SMB is 3.4% of revenue. A
retention programme that halves SMB churn is worth about $1.7M annually in the
best case, and would consume disproportionate service capacity to deliver.

The better use of the same finding is coverage design. SMB accounts should move
to a pooled or self-serve model rather than named coverage, freeing named reps
for the Mid-Market tier — where churn is still 44.4% but each account is worth
11x more. **Mid-Market is where retention spend earns its return.**

---

## 3. Rep book sizes are set too high, and it is measurably costing retention

**Finding.** Churn on a rep's book rises with the size of that book *(Q9)*:

| Book size | Reps | Avg book | Book churn | SMB-only churn |
|---|---|---|---|---|
| 1–8 accounts | 14 | 5.1 | 42.8% | 65.0% |
| 9–16 accounts | 8 | 11.5 | 56.1% | 75.0% |
| 17+ accounts | 5 | 30.6 | **71.3%** | **93.8%** |

The relationship survives the obvious objection. Reps carrying more accounts
might simply hold more SMB accounts, which churn more for unrelated reasons —
but the SMB-only column controls for exactly that, and the effect is *stronger*
within SMB alone (65% → 93.8%) than across all accounts. Book size is doing
the work, not tier mix.

Reps with 17+ accounts hold 38% of total revenue, so this is not a marginal
group.

**Recommendation.** Cap named-coverage books at roughly 16 accounts. The five
reps above that line are carrying an average of 30.6 accounts and losing 71% of
their book. Rebalancing them requires either redistributing accounts to reps
below the line or moving their SMB tail to pooled coverage — which is the same
action recommended in §2, and doing both together is what makes either
affordable.

---

## 4. Beauty & Personal Care is under-invested

**Finding.** *(Q11)* Beauty & Personal Care returns **4.75x ROAS** — the
highest of any vertical, against a 2.95x average — on only **10.7% of spend**,
across 29 advertisers generating $60.4M.

For comparison, E-commerce & Retail takes 40.8% of spend at 3.50x.

**Recommendation.** Advertisers earning 4.75x have headroom to spend more; that
return is well above the point where most performance advertisers would
increase budget. Two concrete actions:
1. Set an upsell target on the existing 29 Beauty accounts before pursuing new
   logos — expanding a book that already returns 4.75x is cheaper than
   acquiring into it.
2. Prioritise Beauty in acquisition for the next two quarters, particularly in
   Europe, where the vertical grew 21.1% and is not yet saturated.

**Caveat.** ROAS here is attributed, not incremental. High attributed ROAS can
partly reflect purchases that would have happened anyway, and beauty is a
category where that risk is real. The upsell recommendation is safe; a large
acquisition bet should be validated with an incrementality test first.

---

## 5. New reps take five months to ramp — plan hiring accordingly

**Finding.** *(Q8)* Reps hired inside the observation window reach:

| Months since hire | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| % of tenured productivity | 25% | 49% | 54% | 76% | **91%** | 93% |

15 of 38 reps were hired during the window, so this is measured on a
substantial group rather than a handful.

**Recommendation.** Hiring decisions need a five-month lead time against
revenue targets — a rep hired to cover a Q1 gap contributes about a quarter of
a tenured rep's revenue in their first month and does not reach 90% until
month 4. Two implications:
1. Headcount to support a Q4 peak must be hired by Q2, not Q3.
2. Ramping reps should not be allocated at-risk or high-value accounts. Given
   §3, the accounts freed by capping book sizes should go to *tenured* reps,
   not to new hires.

---

## Summary of recommended actions

| # | Action | Evidence | Expected impact |
|---|---|---|---|
| 1 | Competitive review of SEA Gaming before next targets are set | Q3, Q12 | Protects ~$2.4M annualised |
| 2 | Move SMB to pooled/self-serve coverage | Q5, Q9 | Frees capacity; SMB is 3.4% of revenue |
| 3 | Cap named books at ~16 accounts | Q9 | Addresses 38% of revenue held by over-loaded reps |
| 4 | Upsell the 29 existing Beauty accounts | Q11 | Highest-ROAS vertical, 10.7% of spend |
| 5 | Hire five months ahead of target periods | Q8 | Removes the ramp gap from capacity planning |
| 6 | Report growth by segment, not blended | Q1, Q3 | Blended growth is currently masking a −34% segment |

---

## What this analysis cannot tell you

Stated plainly, because a recommendation is only as good as its limits:

- **The data is synthetic.** It is generated by `data/generate_data.py` to
  exhibit realistic business dynamics, and it demonstrates method rather than
  describing a real market. No conclusion here is a claim about any actual
  company.
- **ROAS is attributed, not incremental.** Every return figure inherits
  whatever attribution model produced it. Incrementality requires a holdout
  test, not a query.
- **The declines are described, not explained.** The analysis establishes
  *that* SEA Gaming contracted and *how much* it cost. Whether the cause is
  competitive, regulatory, or seasonal is not answerable from spend data alone
  — which is why recommendation 1 is a review, not a fix.
- **Churn is defined as an account closing.** Advertisers who cut spend by 90%
  but stay open are counted as retained. Q12 exists to partly cover that gap,
  but the tier churn rates in §2 read the strict definition.
