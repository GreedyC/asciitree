"""Run this repo's plain test functions without a Python-2-incompatible pytest."""

import importlib
import inspect
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.getcwd())

# Compare output types and existing byte-decoding failures with untouched source.
comparison = r'''
import json
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle
results = []
for label in ('label', u'caf\xe9', 'caf\xc3\xa9'):
    style = BoxStyle()
    for name in ('child_head', 'child_tail', 'last_child_head', 'last_child_tail'):
        try:
            output = getattr(style, name)(label)
            results.append((name, type(output).__name__, repr(output)))
        except UnicodeDecodeError:
            results.append((name, 'UnicodeDecodeError'))
    try:
        output = LeftAligned()({label: {label: {}}})
        results.append(('tree', type(output).__name__, repr(output)))
    except UnicodeDecodeError:
        results.append(('tree', 'UnicodeDecodeError'))
print(json.dumps(results))
'''
baseline = subprocess.check_output([sys.executable, '-c', comparison], cwd='baseline')
feature = subprocess.check_output([sys.executable, '-c', comparison], cwd='.')
assert baseline == feature, (baseline, feature)
print('Baseline/feature Python 2 outputs, types and decoding failures are identical.')

suite = unittest.TestSuite()
for name in ('test_backwards_compat', 'test_unicode', 'test_layout_space'):
    module = importlib.import_module('tests.' + name)
    for function_name, function in inspect.getmembers(module, inspect.isfunction):
        if function_name.startswith('test_'):
            suite.addTest(unittest.FunctionTestCase(function))
assert suite.countTestCases() == 10, suite.countTestCases()
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
