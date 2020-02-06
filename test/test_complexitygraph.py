"""
Tests for `complexitygraph` module.
"""
import pytest
from complexitygraph import time_complexity, fit_curves, score_report


def test_complexities():
    time_complexity(lambda n: n, [1], reps=1, number=1, shuffle=True)


def test_fit_curves():
    ns = range(10)
    ts = time_complexity(lambda n: n, ns, reps=10, number=10, shuffle=True)
    score_dict = fit_curves(ns, ts)
    score_report(score_dict)


def test_time_complexity():
    time_complexity(lambda n: n, [1], reps=1, number=1, shuffle=True)
    time_complexity(lambda n: n, range(10), reps=1, number=1, shuffle=False)
    time_complexity(lambda n: n, range(0, 100, 10), reps=10, number=1, shuffle=False)
    time_complexity(lambda n: n, range(0, 100, 10), reps=10, number=10, shuffle=True)

