# CarSales Tracker Pro — content engine

The traffic strategy: rank for what car salespeople search, funnel them to the
free web tracker (→ paid subs) and the iOS app, and cross-link the BenchCalcs
auto-loan calculator. The **commission calculator is the hub**; blog posts are
spokes that link into it.

SEO is a 3–6 month compounding game. The same posts double as **social fuel**
(see angles below) for faster traffic via TikTok/YouTube/Reddit.

---

## Live now (updated 2026-08-02)

**Hub tools**
- `/tools/car-salesman-commission-calculator/` — interactive, ranks + converts
- `/tools/pay-plan-comparison-calculator/`

**Blog (14 posts, 3 pillars)** — ✅ = indexed by Google as of 2026-08-02
- Money: `how-car-salesman-commission-works`, `what-is-a-mini-deal`,
  `how-much-do-car-salesmen-make`, `car-salesman-pay-plan-explained`,
  ✅`front-end-vs-back-end-gross`, ✅`average-commission-per-car`,
  ✅`car-sales-draw-explained`, ✅`how-to-read-your-commission-statement`,
  ✅`car-sales-spiffs-bonuses-pvr`
- Skills/Career: `how-to-follow-up-with-car-leads`, `how-to-sell-more-cars`,
  `first-30-days-in-car-sales`, `i-want-to-think-about-it-objection`
- Dealership life: `day-in-the-life-car-salesman`

**Plumbing**: `/blog/` index, `/tools/` index, `sitemap.xml` (26 URLs, status
Success), `robots.txt`, shared `/assets/site.css`, Article/Breadcrumb schema on
every page.

### ⚠️ Indexing status (read before adding posts)

As of 2026-08-02: **9 URLs indexed, 13 "Discovered – currently not indexed."**
Every un-indexed blog post is from the original June batch; every July post is
indexed and earning impressions. Google is choosing not to index the older set.

Practical consequence for the engine: **volume is not the constraint right
now — indexation is.** Prefer deepening/consolidating existing posts and
strengthening internal links to un-indexed URLs over shipping a brand-new post
into a queue Google is already declining to crawl. Re-check this section each
month; if indexed count is still flat, pause net-new publishing.

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
7. **Point at least one "Keep reading" card at an un-indexed post.** Crawl
   paths only help if they start from a page Google actually visits. Audit
   2026-08-02 found the entire skills/career cluster
   (`how-to-sell-more-cars`, `first-30-days-in-car-sales`,
   `day-in-the-life-car-salesman`, `how-to-follow-up-with-car-leads`,
   `i-want-to-think-about-it-objection`) was reachable only from other
   un-indexed pages — a closed loop. Fixed by adding a card from each indexed
   money post. Don't let it re-form.

To add a post: copy any existing `/blog/<slug>/index.html`, swap the title,
description, canonical, schema, and body. No build step.

---

## Backlog — re-prioritized 2026-08-02 from Search Console

Ordering is now driven by real GSC data (3 months to 2026-07-31: 964
impressions, 7 clicks, avg position 21). Items at the top are queries the site
**already earns impressions for but has no dedicated page**.

**Tier 1 — proven demand, no page yet**

1. **Tracking a car deal / "commission system" for salespeople**
   Queries: `track sales` (10 impr), `dealership commission system` (5),
   `private sale tracking` (3). ~18 impressions of tool-intent traffic landing
   on nothing dedicated. This is also the closest query cluster to the paid
   product. → tracker + calculator.
2. **Chargebacks: commission that can be taken back**
   Query: `carsales what commissions can be taken back` (3 impr). Partly
   covered by the new §7 in `how-car-salesman-commission-works` (added
   2026-08-02) — promote to a standalone post only if that section starts
   earning impressions. → calc.
3. **How many cars does the average salesperson sell per month?**
   Query: `how many cars does the average salesman sell per month` (3 impr).
   Volume benchmark; pairs naturally with `average-commission-per-car`, which
   is the site's #2 page by impressions. → calc + tracker.

**Tier 2 — from the original backlog, still unwritten**

4. How to hit 20 cars a month (volume systems) → tracker
5. Spreadsheet vs app: tracking your car deals → app
6. Best CRM/apps for car salespeople (we're on the list) → app
7. Surviving month-end in car sales (the push, the board, the bonus)
8. Is car sales a good career in 2026? (honest pros & cons)

**Done** — pay plan (06-18), follow-up (06-18), commission statement,
spiffs/PVR/bonuses, front vs back-end gross, draw explained, "I want to think
about it" objection.

### CTR opportunities (fix before writing anything new)

Two indexed pages carry 70% of all impressions and convert almost none of it —
retitling is cheaper than a new post:

| Page | Impr | Clicks | CTR |
|---|---|---|---|
| `front-end-vs-back-end-gross` | 398 | 2 | 0.5% |
| `average-commission-per-car` | 278 | 0 | 0% |
| `car-sales-draw-explained` | 126 | 0 | 0% |

Avg position is 21 (page 2–3), so some of this is rank, not title. But the
title/meta pair is the free lever.

### Query noise to ignore

`how much does front end work cost` (3 impr) is auto-*repair* intent
(suspension work), not car-sales front-end gross. Don't write for it — it will
pull the wrong audience into a commission page.

---

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
