# MIT License
#
# Copyright (C) IBM Corporation 2018
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

import numpy as np

from art.defences.variance_minimization import TotalVarMin
from art.utils import master_seed

logger = logging.getLogger('testLogger')


class TestTotalVarMin(unittest.TestCase):
    def setUp(self):
        # Set master seed
        master_seed(1234)

    def test_one_channel(self):
        clip_values = (0, 1)
        x = np.random.rand(2, 28, 28, 1)
        preprocess = TotalVarMin(clip_values=(0, 1))
        x_preprocessed, _ = preprocess(x)
        self.assertEqual(x_preprocessed.shape, x.shape)
        self.assertTrue((x_preprocessed >= clip_values[0]).all())
        self.assertTrue((x_preprocessed <= clip_values[1]).all())
        self.assertFalse((x_preprocessed == x).all())

    def test_three_channels(self):
        clip_values = (0, 1)
        x = np.random.rand(2, 32, 32, 3)
        preprocess = TotalVarMin(clip_values=clip_values)
        x_preprocessed, _ = preprocess(x)
        self.assertEqual(x_preprocessed.shape, x.shape)
        self.assertTrue((x_preprocessed >= clip_values[0]).all())
        self.assertTrue((x_preprocessed <= clip_values[1]).all())
        self.assertFalse((x_preprocessed == x).all())

    def test_failure_feature_vectors(self):
        x = np.random.rand(10, 3)
        preprocess = TotalVarMin()

        # Assert that value error is raised for feature vectors
        with self.assertRaises(ValueError) as context:
            preprocess(x)

        self.assertIn('Feature vectors detected.', str(context.exception))


if __name__ == '__main__':
    unittest.main()
