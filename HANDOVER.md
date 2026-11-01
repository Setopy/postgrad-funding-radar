# Handover – Postgrad Funding Radar (as of 1 Nov 2026)

Read this first, then `pipeline_prompts.md` (the rules for the daily pipeline).

## What this project is
- A verified funding listing for students already enrolled in a Master's or PhD: research stays, conference travel, fieldwork, thesis completion and small grants. Priority goes to developing-country students. Part of the Scholarship Radar brand.
- Live site: https://postgrad-funding-radar.pages.dev (Cloudflare Pages, builds from `site/` on every push to `main`).
- The build runs `python3 scripts/validate.py`. It must print OK, or Cloudflare keeps the last good version live.

## Data files (source of truth = this repo)
- `site/data/opportunities.json`: `meta`, `opportunities` (43 listings), `excluded`, `discovery_feeds`. Write it pretty-printed with indent=1 and ensure_ascii=False.
- `site/data/featured.json`: the "Featured today" card (date, id, who, funding, deadline_note).
- `site/data/qa.json`: weekly QA numbers. The first QA run is due Monday 2 Nov 2026.
- `site/data/scholarships.json`: the Scholarship Radar page. It is fed by a separate Mon/Wed/Sat post task.
- Problem reports and the waitlist live in Supabase (the `reports` table), which Setopy reviews by hand.

## State right now
- Registry: 43 listings (34 official, 6 secondary, 3 needs_check). Last daily update: 2026-11-01. Repo is in sync, with nothing unpushed.
- Featured on 1 Nov: `acm-w-scholarship` (deadline 15 Dec 2026).
- New on 1 Nov: ictp-tril, icgeb-short-term-phd, iubmb-wood-whelan, biochemsoc-lab-visit, biochemsoc-general-travel, aaai-27-student-scholar, ipsa-wc2027-travel, eps-member-travel.
- Visitor tracking: Cloudflare Web Analytics is live (beacon in `site/index.html` and `site/privacy.html`). The CSP in `site/_headers` allows static.cloudflareinsights.com and cloudflareinsights.com. Read the numbers in the Cloudflare dashboard under Analytics & Logs → Web Analytics, not on the Pages Metrics tab.

## Follow-ups for the next run
1. `wenner-gren-dfg`: its 1 Nov 2026 deadline has passed. Set status to upcoming and clear next_deadline (the next round closes 1 May).
2. `qcrypt-support`: the 2026 fund only covered caregiving and accessibility costs. Decide whether to move it to `excluded`.
3. These listings have no current call that could be confirmed on official pages: `google-conf-scholarships` (the page does not render without a browser), `ieee-photonics-travel`, `ssrc-nextgen-africa`, `codesria-small-grants`.
4. 9 listings are not yet official (secondary or needs_check). Upgrade each from its official page, or drop it.
5. Calls to watch for early 2027: ICASSP 2027 (IEEE SPS travel grants), ICGEB (opens Jan), AIS-Bocconi (opens Jan), APS-EPS-ICTP (Feb), IUBMB (15 Mar), DAAD GROW.
6. Monday 2 Nov: weekly QA. Sample 10 random listings plus every listing changed in the last 7 days, then write `qa.json`.

## Known problem: pushing from the scheduled task
- The cloud scheduled task got a 403 when pushing: "repository not in this session's authorized repository set". Add Setopy/postgrad-funding-radar to the task's sources (in its settings).
- A local Claude Code session that uses your own git credentials will not hit this.

## Ideas queued (using the cloud credit before 5 Nov)
1. Big discovery sweep (all seven weekday focuses), aiming for about 100 verified listings.
2. Full re-audit of every existing listing.
3. Track Apply clicks, for example with a small Supabase counter. Cloudflare Web Analytics does not record clicks.
4. A month of WhatsApp Channel posts and Status text for deadlines from Nov to Feb.
