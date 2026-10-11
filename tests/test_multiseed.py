"""Functional tests for the v1.1 delta: `python -m unittest discover -s tests`."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/silicon-sample-design/scripts/multiseed_sensitivity.py'
SPEC=importlib.util.spec_from_file_location('multiseed_sensitivity',SCRIPT)
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
BASE=ROOT/'skills/silicon-sample-design/assets/example-simulation-config.json'
DESIGN=ROOT/'skills/silicon-sample-design/assets/example-multi-scenario-config.json'

class MultiSeed(unittest.TestCase):
    def test_same_seed_and_parameters_are_reproducible(self):
        cfg=json.loads(BASE.read_text())
        a,p=M.generate(cfg,12345,{'loading_scale':1})
        b,q=M.generate(cfg,12345,{'loading_scale':1})
        self.assertEqual(a,b)
        self.assertEqual(p,q)
        c,_=M.generate(cfg,12346,{'loading_scale':1})
        self.assertNotEqual(a,c)
        self.assertIn('sample_group',a[0])

    def test_scenario_changes_loading_before_respondents(self):
        cfg=json.loads(BASE.read_text())
        _,medium=M.generate(cfg,12345,{'loading_scale':1})
        _,noise=M.generate(cfg,12345,{'loading_scale':.86})
        _,high=M.generate(cfg,12345,{'loading_scale':1.08})
        v=lambda d:d['item_parameters']['I01']['loading']
        self.assertLess(v(noise),v(medium))
        self.assertLess(v(medium),v(high))

    def test_no_recalculate_complete_cases_after_deletion(self):
        cfg=json.loads(BASE.read_text())
        rows,_=M.generate(cfg,12345,{'loading_scale':1})
        whole=M.analyse(rows,cfg,['D1','D2','D3'],set(),5,12345)
        short=M.analyse(rows,cfg,['D1','D2','D3'],{'I12'},5,12345)
        self.assertEqual(whole['eligible_n'],short['eligible_n'])
        self.assertEqual(whole['efa_n'],short['efa_n'])
        self.assertEqual(whole['validation_n'],short['validation_n'])
        self.assertEqual(whole['status'],'ok')

    def test_exactly_16_seeds_predeclared(self):
        design=json.loads(DESIGN.read_text())
        self.assertEqual([len(design['seeds'][k]) for k in ['medium','noise','high']],[12,2,2])
        self.assertEqual(len(set(sum([design['seeds'][k] for k in ['medium','noise','high']],[]))),16)

if __name__=='__main__':unittest.main()
