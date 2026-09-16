# CarSales Tracker Pro — content engine

The traffic strategy: rank for what car salespeople search, funnel them to the
free web tracker (→ paid subs) and the iOS app, and cross-link the BenchCalcs
auto-loan calculator. The **commission calculator is the hub**; blog posts are
spokes that link into it.

SEO is a 3–6 month compounding game. The same posts double as **social fuel**
(see angles below) for faster traffic via TikTok/YouTube/Reddit.

---

## Live now (updated 2026-09-16)

**Hub tools**
- `/tools/car-salesman-commission-calculator/` — interactive, ranks + converts
- `/tools/pay-plan-comparison-calculator/`

**Blog (14 posts, 3 pillars)**
- Money: `how-car-salesman-commission-works`, `car-salesman-pay-plan-explained`,
  `what-is-a-mini-deal`, `how-much-do-car-salesmen-make`,
  `how-to-read-your-commission-statement`, `car-sales-spiffs-bonuses-pvr`,
  `front-end-vs-back-end-gross`, `car-sales-draw-explained`,
  `average-commission-per-car`
- Skills/Career: `how-to-follow-up-with-car-leads`, `how-to-sell-more-cars`,
  `first-30-days-in-car-sales`, `i-want-to-think-about-it-objection`
- Dealership life: `day-in-the-life-car-salesman`

**Plumbing**: `/blog/` index, `/tools/` index, `sitemap.xml` (27 URLs, Success),
`robots.txt`, `feed.xml`, shared `/assets/site.css`, Article/FAQ/Breadcrumb
schema on every page, trust pages (`about`, `contact`, `editorial-policy`,
`authors/michael-dube`, `privacy`, `terms`, `disclaimer`).

**Indexing reality (GSC, 2026-09-16)**: 10 indexed / 20 not indexed. 17 URLs sit
at "Discovered – currently not indexed", including 8 blog posts. See the
CTR/indexing note at the end of the backlog before commissioning new work.

---

## Internal-linking map (keep this intact when adding posts)

```
                 ┌─────────────────────────────┐
   every post ─► │  Commission Calculator (hub) │ ─► Free web tracker (/)
                 └─────────────────────────────┘ ─► BenchCalcs auto-loan calc
        ▲  ▲  ▲                 ▲
        │  │  │                 │
  how-commission ── what-is-a-mini ── how-much-make   (money cluster, interlinked)
        │
  how-to-sell-more ── first-30-days ── day-in-the-life (skills/life, interlinked)
```

Rules of thumb for each new post:
1. Link **to the calculator** at least once (the conversion bridge).
2. Link **to the free tracker** (`/`) in a CTA box.
3. Link to **2–3 sibling posts** in the "Keep reading" cards.
4. Where payments come up, link the **BenchCalcs auto-loan calculator**
   (`https://benchcalcs.com/calculators/auto-loan-calculator`).
5. Add the new URL to `sitemap.xml`.
6. Reciprocate: add a link **back** from the relevant BenchCalcs page to the
   commission calculator when convenient (two of our own topical sites
   reinforcing each other).

To add a post: copy any existing `/blog/<slug>/index.html`, swap the title,
description, canonical, schema, and body. No build step.

---

## Backlog — re-prioritized 2026-09-16 from Search Console

Ordered by **real impressions with no dedicated page**, from the 3-month GSC
window (7.12K impressions / 209 queries / avg position 11.6). Impression counts
are the 3-month totals for the query cluster named.

**Tier 1 — proven demand, no page yet**

1. **How much does a car salesman make per car?** (~40 impr: "how much do car
   salesmen make per car" 4 @ pos 14, "car salesman commission per car" 3 @ 22,
   "how much commission does a car salesman make per car" 4 @ 23, plus
   "$10,000 car" / "$40,000 car" long-tails). *Intent: informational, high
   commercial adjacency.* → commission calculator. Partly answered by the new
   "What one car actually pays you" section in `how-car-salesman-commission-works`;
   a dedicated page should own the head term.
2. **How many cars does the average salesman sell per month?** (~8 impr across
   "how many cars does the average salesman sell per month" 3 @ 44, "average car
   sales per month" 2 @ 33, "how many cars does a car salesman sell per month"
   2 @ 37). *Intent: informational benchmark.* → tracker (you can't beat an
   average you don't measure).
3. **What is back-end gross / F&I products?** (~10 impr: "back end products"
   2 @ 28, "back end profit meaning" 1 @ 12, "back end sales" 1 @ 21,
   "f&i gross profit definition" 4 @ 26). *Intent: definitional.* → calculator.
   `front-end-vs-back-end-gross` ranks for the front-end half of this; the
   back-end half has its own query set and deserves its own page.
4. **What percentage commission do car salesmen make?** (~15 impr across
   "what percent commission do car salesmen make", "car salesman commission
   percentage" 4 @ 23, "average car salesman commission percentage", etc.)
   *Intent: informational, head-term adjacent.* → calculator.

**Tier 2 — carried over from the original backlog, still unwritten**

5. How to hit 20 cars a month (volume systems) → tracker
6. Best CRM/apps for car salespeople (we're on the list) → app
7. Spreadsheet vs app: tracking your car deals → app
8. Is car sales a good career in 2026? (honest pros & cons)
9. Surviving month-end in car sales (the push, the board, the bonus)

**Written (do not re-commission)**

`car-salesman-pay-plan-explained`, `how-to-follow-up-with-car-leads`,
`how-to-read-your-commission-statement`, `car-sales-spiffs-bonuses-pvr`,
`front-end-vs-back-end-gross`, `car-sales-draw-explained`,
`i-want-to-think-about-it-objection`, `average-commission-per-car`.

---

## Priority ahead of any new post: fix CTR, not volume

The site earns impressions and does not convert them. Site-wide CTR is **0.6%
at average position 11.6**; three pages hold 5,847 impressions between them and
return 24 clicks. Ranking is not the bottleneck — the SERP snippet is.

| Page | Impr | Clicks | CTR | Note |
|---|---|---|---|---|
| `average-commission-per-car` | 1,492 | 1 | **0.07%** | worst on the site |
| `car-salesman-commission-calculator` | 1,902 | 9 | 0.47% | |
| `front-end-vs-back-end-gross` | 2,453 | 14 | 0.57% | "front end gross" = 117 impr @ pos 14.4, 0 clicks |

Rewriting titles and meta descriptions on those three is worth more than the
next four posts combined. Do that before commissioning Tier 1.

Second constraint: **8 of 14 posts are "Discovered – currently not indexed."**
New posts compete for crawl budget the existing ones are not getting. Volume is
not the lever right now.

## Social repurposing (per post → faster traffic)

Car-sales content performs on TikTok/YouTube Shorts and in r/CarSalesProfessionals,
r/askcarsales, and dealer Facebook groups. Each post = several clips/threads:

- **How commission works** → "Why your $3,000 deal only paid you $550" (pack reveal)
- **Mini deal** → "Should you take a mini? The answer that gets reps fired up"
- **How much they make** → "Car sales income: green pea vs top dog" (the table)
- **Sell more cars** → "The 9:30am hour that separates 9-car reps from 18-car reps"
- **First 30 days** → "Day 1 in car sales: what nobody tells the green pea"
- **Day in the life** → "POV: it's 8:30pm and the last up just walked in"

Hook with the surprising number or the relatable moment; CTA to the calculator
or the free tracker in the caption/bio.

---

## Measurement
- Google Search Console: submit `sitemap.xml`, watch impressions/clicks per page.
- The calculator and money posts should index and gather impressions first.
- Conversion signal: paywall opens / web subs from `utm`-free organic sessions.
