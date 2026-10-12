# Release evidence checker

A dependency-free Python project that screens a gate pack for complete, current evidence. It demonstrates practical project governance using fictional scenarios. Supplied evidence references are not independently verified and `READY_FOR_REVIEW` does not authorize release.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python readiness.py examples/pension-w24.json
python readiness.py examples/pension-w26.json --json
python -m unittest -v
```

The W24 example returns `NO_GO` and exit code 1. The W26 example returns `READY_FOR_REVIEW` and exit code 0. Invalid input/file errors return exit code 2. JSON output is written to stdout including invalid-input reports.

## Input

The JSON object includes `profile`, `as_of_week`, `max_age_weeks` and a `gates` array. Each gate has a unique `id`, `status` (`pass`, `fail`, `pending`), text `owner`, `reviewer`, `evidence` and integer/null `reviewed_week`. Weeks are relative scenario periods. IDs and statuses are case-sensitive.

| Profile | Required gates |
| --- | --- |
| implementation | uat, data, security, training, operations, sponsor |
| design | research, critical_findings, accessibility, feasibility, product_acceptance, handoff |

Every required gate must be present, pass, have nonblank owner/reviewer/evidence and have a review within the configured age. Missing or pending evidence blocks readiness. Duplicate/unknown IDs, future review weeks and invalid types are input errors. Evidence exactly at the maximum permitted age remains current.

Templates must still define substantive criteria. A text reference does not prove the underlying evidence passed review. The portfolio examples use `SIM` references to make their fictional status visible.

## Why this belongs in a PM portfolio

The code makes a control repeatable: missing mandatory gates cannot disappear from a checklist, and stale evidence cannot appear current. Test cases include failed data gates despite apparently healthy aggregate results, missing approvals and review-age boundaries. A real project needs authorized approval and authentic evidence outside this tool.
