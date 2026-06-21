# CarSales Tracker Pro — content engine

The traffic strategy: rank for what car salespeople search, funnel them to the
free web tracker (→ paid subs) and the iOS app, and cross-link the BenchCalcs
auto-loan calculator. The **commission calculator is the hub**; blog posts are
spokes that link into it.

SEO is a 3–6 month compounding game. The same posts double as **social fuel**
(see angles below) for faster traffic via TikTok/YouTube/Reddit.

---

## Live now (2026-06-14)

**Hub tool**
- `/tools/car-salesman-commission-calculator/` — interactive, ranks + converts

**Blog (7 posts, 3 pillars)**
- Money: `car-salesman-pay-plan-explained` (1st auto-engine post, 2026-06-18), `how-car-salesman-commission-works`, `what-is-a-mini-deal`, `how-much-do-car-salesmen-make`
- Skills/Career: `how-to-sell-more-cars`, `first-30-days-in-car-sales`
- Dealership life: `day-in-the-life-car-salesman`

**Plumbing**: `/blog/` index, `/tools/` index, `sitemap.xml`, `robots.txt`,
shared `/assets/site.css`, Article/FAQ/Breadcrumb schema on every page.

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

## 12-topic backlog (ordered by leverage)

**Money (highest intent — best product fit)**
1. ✅ DONE 2026-06-18 — Car salesman pay plan explained (`car-salesman-pay-plan-explained`)
2. How to read your car sales pay plan / commission statement → calc
3. Spiffs, bonuses & PVR: the extras that pad your check
4. Front-end vs back-end gross: what counts toward your commission → calc
5. Car sales draw explained (recoverable vs non-recoverable)

**Skills / career**
6. How to follow up with car leads (cadence + scripts)
7. Overcoming "I want to think about it" (and 4 other objections)
8. How to hit 20 cars a month (volume systems)
9. Best CRM/apps for car salespeople (we're on the list) → app
10. Spreadsheet vs app: tracking your car deals → app

**Dealership life / culture**
11. Is car sales a good career in 2026? (honest pros & cons)
12. Surviving month-end in car sales (the push, the board, the bonus)

Each maps cleanly to a search query car salespeople actually type, and each
funnels to the calculator and the tracker.

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
