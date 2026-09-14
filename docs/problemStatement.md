# Weekly App Review Pulse — Groww Platform

## Overview

Turn raw Google Play Store feedback into a **weekly pulse** your team can scan in minutes: what users care about, what they actually said, and what to do next. Reviews are already public; the job is to **aggregate, theme, summarize, and deliver** that insight through familiar surfaces — **Google Docs** for the written pulse and **Gmail** for a draft you can send yourself — without handling credentials or REST wiring yourself.

> **Target App:** [Groww — Stocks, Mutual Fund, IPO](https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN)

---

## End-to-End Flow (What "Done" Looks Like)

1. **Pull recent reviews** — Google Play Store reviews for the product (within the constraints below).
2. **Cluster into themes** — Group them into a small set of themes and distill a one-page weekly note.
3. **Publish to Google Docs** — Put that note where stakeholders can read it.
4. **Draft email via Gmail** — Create a draft email to yourself (or an alias) that contains or links to that pulse.

---

## Deliverables

The weekly one-page pulse must include:

| Section | Details |
|---|---|
| **Top Themes** | What people are talking about most |
| **Real User Quotes** | Verbatim snippets from reviews — no invented wording |
| **Action Ideas** | 3 concrete next steps grounded in the themes |
| **Draft Email** | Send yourself a draft email containing the weekly note (or a clear pointer to it) |

---

## Who This Helps

| Audience | Why |
|---|---|
| **Product / Growth** | Prioritize fixes and improvements from real signals |
| **Support** | Align messaging with what users are actually saying |
| **Leadership** | One-page health check without drowning in raw reviews |

---

## What You Must Build

1. **Import Reviews** — From roughly the last **8–12 weeks** (fields such as rating, title, text, date — whatever the export provides).
2. **Group into Themes** — At most **5 themes** (examples: onboarding, KYC, payments, statements, withdrawals — pick what fits the product).
3. **Generate Weekly Note** with:
   - Top **3 themes** (subset of the 5 as appropriate)
   - **3 user quotes**
   - **3 action ideas**
4. **Draft an Email** — With the note to yourself or an alias.

---

## Integrations: Google Docs & Gmail via MCP

> [!IMPORTANT]
> Use **MCP (Model Context Protocol) servers** for Google Docs and Gmail — for example, creating or updating the pulse document and creating the draft message — **rather than integrating Google APIs directly** (no bespoke OAuth client + REST client code as the primary integration path).

MCP servers expose tools your agent or app can call; lean on that pattern so Docs and Gmail stay consistent with the course tooling and avoid duplicating auth and HTTP plumbing.

Choose MCP servers or connectors your environment provides for Docs and Gmail; the requirement is **MCP-first**, not "call Google APIs manually."

---

## Key Constraints

| Constraint | Rule |
|---|---|
| **Reviews** | Use public review exports only — no scraping behind store logins or ToS-violating automation |
| **Themes** | Maximum **5 themes** for clustering; the written pulse highlights the **top 3** |
| **Length** | Keep the note scannable and **≤ 250 words** where applicable |
| **Privacy** | Do **not** include PII — no usernames, emails, device IDs, or other identifiable reviewer data in any artifact (quotes should be anonymous / stripped as needed) |
