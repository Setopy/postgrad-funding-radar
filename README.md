# Postgrad Funding Radar

Verified funding for students already enrolled in a Master's or PhD (research stays, conference travel, fieldwork, thesis completion), with priority for students from developing countries. Part of Scholarship Radar.

## How it fits together

| Part | Where | Notes |
| --- | --- | --- |
| Website | `site/` → Cloudflare Pages | Static. No build tools needed. |
| Listings (source of truth) | `site/data/opportunities.json` | Edited by the daily pipeline via commits. One record per programme. |
| Weekly QA numbers | `site/data/qa.json` | Written by the Monday pipeline run. |
| Waitlist and problem reports | Supabase tables `waitlist`, `reports` | Public key can only insert. Read them in the Supabase dashboard. |
| Quality gate | `scripts/validate.py` | Cloudflare runs it before each deploy. A broken listing fails the build and the last good version stays live. |
| Pipeline prompts | `pipeline_prompts.md` | Used by the daily scheduled task. |

## Cloudflare Pages settings

- Framework preset: None
- Build command: `python3 scripts/validate.py`
- Build output directory: `site`
- Production branch: `main`

## Supabase setup

1. New project (choose a region close to most users, e.g. Europe West for Africa).
2. SQL Editor → paste `supabase/schema.sql` → Run.
3. Project Settings → API → copy the Project URL and the publishable key into `site/config.js` (already done for project `zikclaxuyzdwhmvcnghq`, Europe).

## Local tasks

- Check listings: `python3 scripts/validate.py`
- Export a spreadsheet for hand-checks: `python3 scripts/export_xlsx.py` (needs `openpyxl`)

## Listing rules (short version)

Only funding for already-enrolled MSc/PhD students. Every fact comes from the funder's own page. Unknown = "not stated". `verification: official` only when the deadline or window was confirmed on the official page. Full rules in `pipeline_prompts.md`.
