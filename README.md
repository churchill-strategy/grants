# grants.json

Live data for the **Edmonton Ethnocultural Grants Finder** at
https://www.churchillstrategy.ca/edmonton-grants-finder (unlisted page).

The Squarespace code block on that page loads
`https://raw.githubusercontent.com/churchill-strategy/grants.json/main/grants.json`
every time someone opens it. If the file can't be loaded, the page falls back to the copy built into the code block. Statuses and countdowns ("Closes in 7 days") are worked out in the visitor's browser from today's date, so they're always current.

A weekly scheduled task re-checks every program and searches for new ones. It updates this file only after `python3 validate.py` passes.

## File format

```json
{ "verified": "YYYY-MM-DD", "count": 78, "programs": [ ... ] }
```

Each program:

| key | meaning |
| --- | --- |
| `n` | Program name (no em dashes; use a colon) |
| `f` | Funder |
| `c` | Optional city: `"Edmonton"` puts it in the Edmonton-local view; other cities (e.g. `"Calgary"`) are hidden from the Edmonton view |
| `lv` | `Federal`, `Provincial`, `Municipal`, `Foundation` or `Corporate` |
| `r` | `Canada` for national, otherwise a province code (`AB`, `BC`, ...) |
| `fo` | Focus tags, e.g. `Events & festivals`, `Operating`, `Projects`, `Anti-racism`, `Capital`, `Arts & heritage`, `Youth`, `Seniors`, `Capacity building`, `Community grants`, `Sponsorship & donations`, `Staffing` |
| `max` | Largest amount as a number, or `null` (used for sorting) |
| `amt` | Amount as shown to visitors |
| `w` | Intake windows `[[opens, closes], ...]`; `opens` is a date, `null` (deadline only) or `"rolling"`; `closes` is a date (`"2099-12-31"` for open-ended rolling programs) |
| `next` | Text shown when no window is open, e.g. "Next intake expected fall 2027" |
| `d` | Description |
| `el` | Who can apply |
| `warn` | Optional warning line |
| `u` | Official program page (https) |

## Rules

- Only facts confirmed on the funder's own page, or a reliable source when the funder's page is down. Unconfirmed future dates go in `next` as "expected", never in `w`.
- Canadian spelling, no em dashes, no prices for Churchill Strategy services.
- Never delete the list wholesale: the validator refuses fewer than 30 programs.
