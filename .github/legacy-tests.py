"""Run this repo's plain test functions without a Python-2-incompatible pytest."""

import importlib
import inspect
import os
import sys
import unittest

sys.path.insert(0, os.getcwd())
suite = unittest.TestSuite()
for name in ('test_backwards_compat', 'test_unicode', 'test_layout_space'):
    module = importlib.import_module('tests.' + name)
    for function_name, function in inspect.getmembers(module, inspect.isfunction):
        if function_name.startswith('test_'):
            suite.addTest(unittest.FunctionTestCase(function))
assert suite.countTestCases() == 10, suite.countTestCases()
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
