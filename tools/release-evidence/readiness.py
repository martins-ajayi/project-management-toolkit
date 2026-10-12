#!/usr/bin/env python3
"""Screen a versioned gate pack for complete, current mandatory evidence."""
import argparse
import json
from pathlib import Path
import sys

PROFILES = {
    'implementation': ('uat', 'data', 'security', 'training', 'operations', 'sponsor'),
    'design': ('research', 'critical_findings', 'accessibility', 'feasibility', 'product_acceptance', 'handoff'),
}

def whole(value, field, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{field} must be an integer >= {minimum}')
    return value

def evaluate(pack):
    if not isinstance(pack, dict):
        raise ValueError('Input must be a JSON object')
    profile = pack.get('profile')
    if not isinstance(profile, str) or profile not in PROFILES:
        raise ValueError('profile must be implementation or design')
    week = whole(pack.get('as_of_week'), 'as_of_week', 1)
    age = whole(pack.get('max_age_weeks'), 'max_age_weeks')
    gates = pack.get('gates')
    if not isinstance(gates, list):
        raise ValueError('gates must be an array')
    records = {}
    for gate in gates:
        if not isinstance(gate, dict):
            raise ValueError('Each gate must be an object')
        id = gate.get('id')
        if not isinstance(id, str) or id not in PROFILES[profile]:
            raise ValueError(f'Unknown gate ID for {profile}: {id!r}')
        if id in records:
            raise ValueError(f'Duplicate gate ID: {id}')
        status = gate.get('status')
        if status not in ('pass', 'fail', 'pending'):
            raise ValueError(f'{id}: status must be pass, fail or pending')
        reviewed = gate.get('reviewed_week')
        if reviewed is not None:
            whole(reviewed, f'{id}.reviewed_week', 1)
            if reviewed > week:
                raise ValueError(f'{id}: reviewed_week cannot be in the future')
        for field in ('owner', 'reviewer', 'evidence'):
            if not isinstance(gate.get(field), str):
                raise ValueError(f'{id}.{field} must be text')
        records[id] = gate
    results = []
    for id in PROFILES[profile]:
        g = records.get(id)
        reasons = []
        if g is None:
            reasons.append('Mandatory gate missing')
        else:
            if g['status'] != 'pass':
                reasons.append(f"Status {g['status']}")
            for field in ('owner', 'reviewer', 'evidence'):
                if not g[field].strip():
                    reasons.append(f'Missing {field}')
            if g.get('reviewed_week') is None:
                reasons.append('Review week missing')
            elif week - g['reviewed_week'] > age:
                reasons.append('Review evidence stale')
        results.append({'gate': id, 'ready': not reasons, 'reasons': reasons,
                        'evidence': g['evidence'] if g else None})
    ready = all(r['ready'] for r in results)
    return {'profile': profile, 'as_of_week': week,
            'state': 'READY_FOR_REVIEW' if ready else 'NO_GO', 'gates': results}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--json', action='store_true', dest='json_output')
    args = parser.parse_args(argv)
    try:
        report = evaluate(json.loads(args.file.read_text(encoding='utf-8')))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        if args.json_output:
            print(json.dumps({'state': 'INVALID_INPUT', 'error': str(exc)}))
        else:
            print(f'INVALID_INPUT: {exc}', file=sys.stderr)
        return 2
    if args.json_output:
        print(json.dumps(report, indent=2))
    else:
        print(report['state'])
        for row in report['gates']:
            print(f"{row['gate']}: " + ('Current evidence recorded' if row['ready'] else '; '.join(row['reasons'])))
    return 0 if report['state'] == 'READY_FOR_REVIEW' else 1

if __name__ == '__main__':
    sys.exit(main())
