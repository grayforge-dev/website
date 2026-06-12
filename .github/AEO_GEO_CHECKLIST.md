# AEO / GEO Maintenance Checklist

Last reviewed: 2026-06-12

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

## Recurring Checks

- [ ] After product or pricing changes, update visible copy, JSON-LD, FAQ answers, and guide comparison tables together.
- [ ] Keep `dateModified` and sitemap `lastmod` accurate after meaningful content changes.
- [ ] Verify App Store and Google Play descriptions use the same core claims as the website.
- [ ] Check Search Console indexing for `/`, `/dashlog/`, `/noisyno/`, and `/ko/offline-no-account-apps/`.
- [ ] Search for inaccurate claims such as `no analytics`, `no data collection`, and `lifetime` before every deployment.
- [ ] Validate JSON-LD and mobile layout after structural edits.

## External Authority Gaps

- [ ] Earn independent product mentions or reviews that link to the official product pages.
- [ ] Encourage real App Store and Google Play reviews without scripting review language.
- [ ] Publish useful, evidence-backed guides only when they answer a distinct user question.
- [ ] Recheck whether AI search engines cite GrayForge after the pages are indexed.

## Claim Boundaries

- NoisyNo and DashLog are currently free and require no subscription. They are not lifetime-purchase products.
- NoisyNo processes user audio and video files on-device, but limited Firebase analytics and diagnostics may be used.
- DashLog stores personal drive records locally and does not upload the drive archive to a DashLog server, but limited Firebase analytics and diagnostics may be used.
