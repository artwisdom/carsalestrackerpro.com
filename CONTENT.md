# CarSales Tracker Pro — content engine

The traffic strategy: rank for what car salespeople search, funnel them to the
free web tracker (→ paid subs) and the iOS app, and cross-link the BenchCalcs
auto-loan calculator. The **commission calculator is the hub**; blog posts are
spokes that link into it.

SEO is a 3–6 month compounding game. The same posts double as **social fuel**
(see angles below) for faster traffic via TikTok/YouTube/Reddit.

---

## Live now (reviewed 2026-09-16)

**Hub tools**
- `/tools/car-salesman-commission-calculator/` — interactive, ranks + converts
- `/tools/pay-plan-comparison-calculator/` — compares two complete plans
- `/tracker/` — local-first deal and commission tracker

**Blog (16 posts, 3 pillars)**
- Money: `car-salesman-pay-plan-explained`, `how-car-salesman-commission-works`,
  `what-is-a-mini-deal`, `how-much-do-car-salesmen-make`,
  `how-to-read-your-commission-statement`, `car-sales-spiffs-bonuses-pvr`,
  `front-end-vs-back-end-gross`, `car-sales-draw-explained`,
  `average-commission-per-car`
- Skills/Career: `how-to-follow-up-with-car-leads`, `how-to-sell-more-cars`,
  `first-30-days-in-car-sales`, `i-want-to-think-about-it-objection`,
  `spreadsheet-vs-app-car-sales-tracking`
- Dealership life: `day-in-the-life-car-salesman`,
  `is-car-sales-a-good-career`

**Plumbing**: `/blog/` index, `/tools/` index, `sitemap.xml` (29 URLs),
`robots.txt`, RSS, IndexNow, shared `/assets/site.css`, structured data,
publisher profile, editorial policy, privacy, terms, contact, and disclaimer.

### Current search baseline

Search Console, last three months through 2026-09-14:

- **41 clicks / 7,470 impressions / 0.5% CTR / average position 11.4**
- Top pages: `front-end-vs-back-end-gross` (2,560 impressions), commission
  calculator (2,025), `average-commission-per-car` (1,566), and
  `car-sales-draw-explained` (755)
- Coverage report last updated 2026-09-13: 10 indexed, 17 discovered but not
  indexed, and 3 malformed 404 discoveries. Some URLs already show impressions
  even while the slower coverage report still groups them as not indexed.

**Operating decision:** do not increase publishing volume yet. Deepen pages
already earning impressions, improve crawl paths into the older skills/career
cluster, and let the current indexing validation finish. One excellent update
is worth more than several new pages waiting to be crawled.

`NET_NEW_STATUS: PAUSED_FOR_INDEXING`

The automated content routine must treat that status as a hard gate: no new
blog URL may be created while it is present. At most once every 28 days, the
routine may make one substantive improvement to an existing page listed under
"Current optimization targets"; otherwise it should finish without changing
the site. Remove the status only after Search Console shows that the indexing
queue has materially cleared or a verified query opportunity justifies a new
page.

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
7. At least one high-impression money page should link to each skills/career
   article until that article is crawled. Do not let an unindexed cluster form
   a closed loop again.

To add a post: copy any existing `/blog/<slug>/index.html`, swap the title,
description, canonical, schema, and body. No build step.

---

## Backlog (ordered by current leverage)

Do not publish these until the September indexing queue improves or Search
Console shows a query opportunity strong enough to justify a dedicated page.

1. Tracking a car deal or commission system for salespeople — strongest product
   intent; consider expanding the tracker page before creating another URL.
2. Chargebacks: commission that can be taken back — now covered substantially
   inside `how-car-salesman-commission-works`; make standalone only if it earns
   impressions.
3. How many cars does the average salesperson sell per month?
4. How to hit 20 cars a month (volume systems) → tracker.
5. Best CRM/apps for car salespeople → tracker/app.
6. Surviving month-end in car sales.

### Current optimization targets

- `average-commission-per-car`: query alignment updated 2026-09-16 after 1,566
  impressions, 1 click, and average position 19.3.
- `front-end-vs-back-end-gross`: protect its rankings and use it to pass crawl
  authority into the objection/skills cluster.
- `/tracker/`: expanded with static, useful documentation on 2026-09-16 because
  it is the best product-intent URL and remained discovered but not indexed.

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
