import copy
import json
from pathlib import Path
import unittest
from readiness import evaluate, main, PROFILES

BASE = json.loads((Path(__file__).parent / 'examples/pension-w26.json').read_text())

class EvidenceTests(unittest.TestCase):
    def setUp(self): self.pack = copy.deepcopy(BASE)
    def test_complete_pack(self): self.assertEqual(evaluate(self.pack)['state'], 'READY_FOR_REVIEW')
    def test_missing_mandatory_gate(self):
        self.pack['gates'].pop()
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_failed_gate(self):
        self.pack['gates'][0]['status'] = 'fail'
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_blank_evidence(self):
        self.pack['gates'][0]['evidence'] = '  '
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_missing_reviewer(self):
        self.pack['gates'][0]['reviewer'] = ''
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_missing_owner(self):
        self.pack['gates'][0]['owner'] = ''
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_stale_review(self):
        self.pack['gates'][0]['reviewed_week'] = 23
        self.assertEqual(evaluate(self.pack)['state'], 'NO_GO')
    def test_age_boundary(self):
        self.pack['gates'][0]['reviewed_week'] = 24
        self.assertEqual(evaluate(self.pack)['state'], 'READY_FOR_REVIEW')
    def test_future_review_invalid(self):
        self.pack['gates'][0]['reviewed_week'] = 27
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_duplicate_invalid(self):
        self.pack['gates'].append(self.pack['gates'][0])
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_unknown_gate_invalid(self):
        self.pack['gates'][0]['id'] = 'unknown'
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_booleans_not_weeks(self):
        self.pack['as_of_week'] = True
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_unknown_profile(self):
        self.pack['profile'] = 'other'
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_bad_status(self):
        self.pack['gates'][0]['status'] = 'green'
        with self.assertRaises(ValueError): evaluate(self.pack)
    def test_design_profile(self):
        self.pack['profile'] = 'design'
        for row,id in zip(self.pack['gates'],PROFILES['design']): row['id'] = id
        self.assertEqual(evaluate(self.pack)['state'], 'READY_FOR_REVIEW')
    def test_w24_example_blocks(self):
        p=json.loads((Path(__file__).parent/'examples/pension-w24.json').read_text())
        r=evaluate(p)
        self.assertEqual(r['state'],'NO_GO')
        self.assertFalse(next(x for x in r['gates'] if x['gate']=='data')['ready'])
    def test_cli_complete(self):
        self.assertEqual(main([str(Path(__file__).parent/'examples/pension-w26.json')]),0)
    def test_cli_blocked(self):
        self.assertEqual(main([str(Path(__file__).parent/'examples/pension-w24.json')]),1)
    def test_cli_file_error(self): self.assertEqual(main(['/missing-example.json']),2)

if __name__ == '__main__': unittest.main()
