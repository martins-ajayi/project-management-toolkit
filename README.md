# Project Management Toolkit

Original practical templates and a release evidence checker complement Martins Ajayi’s case studies. Templates are illustrative delivery methods, not historical project records. Tailor the controls to scope and risk; a prototype handoff needs different gates from a data migration.

## Toolkit
| Phase | Template |
| --- | --- |
| 01 | [Project charter](templates/01-project-charter.md) |
| 02 | [Business case and benefits](templates/02-business-case-and-benefits.md) |
| 03 | [Scope work breakdown and schedule](templates/03-scope-wbs-and-schedule.md) |
| 04 | [Stakeholder RACI and communication plan](templates/04-stakeholders-raci-and-comms.md) |
| 05 | [Budget and resource control](templates/05-budget-and-resource-control.md) |
| 06 | [RAID and escalation register](templates/06-raid-and-escalation.md) |
| 07 | [Requirements and acceptance traceability](templates/07-requirements-traceability.md) |
| 08 | [Change and decision record](templates/08-change-and-decision-record.md) |
| 09 | [Executive status and steering minutes](templates/09-executive-status-and-minutes.md) |
| 10 | [UAT and quality plan](templates/10-uat-and-quality-plan.md) |
| 11 | [Data migration and reconciliation](templates/11-data-migration-and-controls.md) |
| 12 | [Release cutover and hypercare](templates/12-release-cutover-and-hypercare.md) |
| 13 | [Design research and implementation handoff](templates/13-design-research-and-handoff.md) |
| 14 | [Commercial and fit gap controls](templates/14-commercial-and-fit-gap.md) |
| 15 | [Closure benefits and lessons](templates/15-closure-and-lessons.md) |

## Working project
[Release evidence checker](tools/release-evidence/README.md) reads a JSON gate pack, rejects incomplete or stale mandatory evidence, and produces a traceable report. It uses the Python standard library and has tests for missing controls, invalid inputs, stale reviews and failed gates. Fictional pension examples reproduce W24 NO-GO and W26 ready-for-review results.

The checker reports evidence readiness. Authorized reviewers retain the release decision; the tool does not independently verify supplied evidence or confer approval.
