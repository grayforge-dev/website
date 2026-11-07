# AEO / GEO Maintenance Checklist

Last reviewed: 2026-10-30

## Completed

- [x] Canonical URLs use `https://grayforge.app/`.
- [x] Sitemap and robots.txt are published.
- [x] OAI-SearchBot is explicitly allowed.
- [x] IndexNow submits primary pages after deployment.
- [x] GrayForge, DashLog, and NoisyNo use connected JSON-LD entity IDs.
- [x] Product pages include visible FAQ content matching FAQPage JSON-LD.
- [x] Korean intent guide answers offline, no-account, and no-subscription queries.
- [x] Privacy claims distinguish core user data from limited Firebase diagnostics.
- [x] Product and guide pages link to privacy policies and store listings.
- [x] Home Organization JSON-LD has `logo` (`/assets/grayforge-logo-512.png`) and `sameAs` for the Google Play developer page. The App Store developer page is under a personal name and is left out on purpose.
- [x] BlogPosting `author`/`publisher` are inline Organization nodes; deprecated HowTo markup is removed from all guides.
- [x] BreadcrumbList on app pages, all DashLog FAQ locales, `/products/` and `/blog/`.
- [x] Home, `/blog/` and `/products/` share `/assets/og-grayforge.png` (1200×630) with `summary_large_image` cards.
- [x] Custom `404.html` (noindex) links back to home, apps and the Journal.
- [x] Inter loads with `display=optional` so the font swap no longer shifts layout; Fraunces stays `display=swap`.

## Recurring Checks

- [ ] After product or pricing changes, update visible copy, JSON-LD, FAQ answers, and guide comparison tables together.
- [ ] Keep `dateModified` and sitemap `lastmod` accurate after meaningful content changes.
- [ ] Verify App Store and Google Play descriptions use the same core claims as the website.
- [ ] Check Search Console indexing for `/`, `/dashlog/`, `/noisyno/`, and `/vocalout/`. (`/ko/offline-no-account-apps/` no longer exists and was removed from the IndexNow list.)
- [ ] When a new app or page is added, update `sitemap.xml`, `llms.txt`, the IndexNow URL list in `.github/workflows/indexnow.yml`, and the home page JSON-LD in the same commit.
- [ ] Search for inaccurate claims such as `no analytics`, `no data collection`, and `lifetime` before every deployment.
- [ ] Validate JSON-LD and mobile layout after structural edits.
- [ ] When a guide gets a translation, add the language link to the metabar of every language version, and point the matching localized product page at the localized guide.
- [ ] Keep `<title>` within about 60 characters (CJK characters count double) and meta descriptions within about 155 characters.
- [x] ZapBlur iOS launch (App Store id6824579189, released 2026-10-31): App Store links on the home card, `/products/`, `zapblur/` and `ko/zapblur/`; `sameAs` in the home and product-page JSON-LD; privacy policy added to `sitemap.xml`; `llms.txt` updated.
- [ ] ZapBlur Android launch: it is still listed as *Android coming soon* (home card and aside note, `/products/` card, the status line of `zapblur/` and `ko/zapblur/`, `llms.txt`, and `operatingSystem: ["iOS"]` in the JSON-LD). At launch add the Google Play link everywhere, add Android to `operatingSystem` and the Play URL to `sameAs`, and re-read the pages for claims that were true only before the Android release.

## External Authority Gaps

- [ ] Earn independent product mentions or reviews that link to the official product pages.
- [ ] Encourage real App Store and Google Play reviews without scripting review language.
- [ ] Publish useful, evidence-backed guides only when they answer a distinct user question.
- [ ] Recheck whether AI search engines cite GrayForge after the pages are indexed.

## Claim Boundaries

- NoisyNo and DashLog are currently free and require no subscription. They are not lifetime-purchase products.
- NoisyNo processes user audio and video files on-device, but limited Firebase analytics and diagnostics may be used.
- ZapBlur is on the App Store for iPhone and free to download; the Android version is not released, so do not describe it as available on Google Play or Android. Photos are processed on-device and never leave it; Firebase usage and crash data are sent only after the user allows it; on Android, Google ML Kit may send device and performance information regardless of that choice.
- DashLog stores personal drive records locally and does not upload the drive archive to a DashLog server, but limited Firebase analytics and diagnostics may be used.
- DashLog is a drive logbook, not a tax-ready mileage log: drives export as CSV or GPX, with no tax formats or business/personal categories. Do not pitch it for work mileage, taxes or reimbursement (in German, avoid "Fahrtenbuch").
