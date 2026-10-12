# Data migration and reconciliation

Establish record and value integrity before transition.

**Reusable illustrative template.** Bracketed fields are completed for a real project; this is not an employer record.

| Control | Owner | Evidence | Approval |
| --- | --- | --- | --- |
| Mapping and rule version | Data Lead | Approved source-to-target map | Business / Finance |
| Profiling and exceptions | Data Lead | Duplicates, invalid keys, quarantines | Business |
| Count reconciliation | Data Lead | Source = accepted + quarantined | Reviewer |
| Value reconciliation | Finance | Control totals and unexplained variance | Finance |
| Access and retention | Security | Approved controls and test data handling | Security |
| Restore and replay | Operations | Rehearsal and live-write handling | Operations |

Do not delete exceptions to force totals to agree. Preserve lineage, quarantine dispositions and independent review. In a real project, identify applicable privacy, retention and policy obligations with responsible specialists.
