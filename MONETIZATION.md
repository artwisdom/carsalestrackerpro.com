# Monetization — Phase 1: Website ads (AdSense)

The iOS app earns through **AdMob** (`ca-app-pub-…`). The website earns through
**AdSense** (`ca-pub-…`). Same Google account, same publisher number
(9525656057819245), two different consoles. Everything on the site side is
already wired — the steps below are the account side.

## Already live on the site (no action)

- `/ads.txt` → `google.com, pub-9525656057819245, DIRECT, f08c47fec0942fa0`
- Site-verification meta tag (`google-adsense-account`) in `<head>`
- Two responsive ad containers + the AdSense loader in `index.html`,
  shown **only to free-tier users** — Premium/Advanced stay ad-free,
  same ad model as the iOS app

## Your steps (~15 minutes of clicking, then waiting)

1. **Sign in** at [adsense.google.com](https://adsense.google.com) with
   **dube508@gmail.com** (the account running your AdMob).
2. **Add the site**: Sites → *Add site* → `carsalestrackerpro.com`.
3. **Verify ownership**: AdSense will detect the meta tag or the ads.txt —
   both are already live. Click *Verify* → *Request review*.
4. **Payments setup** (money cannot flow without this): Payments →
   *Payments info* → confirm name/address, submit **W-9** tax info,
   add your bank account.
5. **Wait for site review** — typically a few days, up to ~2 weeks.
   You'll get an email when the site is "Ready".
6. **Create two ad units**: Ads → *By ad unit* → **Display ad**:
   - `CSTP Web Top` (responsive)
   - `CSTP Web Bottom` (responsive)

   Each unit gives you a 10-digit `data-ad-slot` number.
7. **Paste the two slot IDs** into the `CONFIG` block at the top of
   `index.html`'s script:

   ```js
   AD_SLOTS:{top:'1234567890',bottom:'0987654321'},
   ```

   Commit and push — ads start serving to free users on the next deploy.

## Rules that protect the account

- **Leave Auto ads OFF** for this site — auto ads would inject ads into the
  tracker UI for *paying* users too. The manual slots already target only
  free users.
- **Never click your own ads**, and don't ask anyone to. Invalid traffic is
  the #1 reason new accounts get banned.
- Payout threshold is **$100**, paid monthly around the 21st.

## Phase 2 (later, optional)

- Stripe Payment Links pasted into `CONFIG.PAYMENT_LINKS` → direct web
  subscriptions without the App Store cut
- Redeem codes (`CONFIG.UPGRADE_CODE_HASHES`) for cross-selling web unlocks
  to iOS subscribers
