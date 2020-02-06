"""
Tests for `complexitygraph` module.
"""
import pytest
import math
from complexitygraph import time_complexity, fit_curves, score_report
import random

def test_complexities():
    def complexity_should_be(what, fn, ns):
        ts = time_complexity(fn, ns, reps=10, number=10)
        score_dict = fit_curves(ns, ts)
        print(score_dict)
        assert list(score_dict.keys())[0] == what

    ns = range(1, 1000, 50)

    def constant(n):
        return 1

    def linear(n):
        return [1 for i in range(n)]

    def quadratic(n):
        return [1 for i in range(n) for j in range(n)]

    def cubic(n):
        return [1 for i in range(n) for j in range(n) for k in range(n)]
        
    def exp(n):
        return [1 for i in range(2**n)]

    def factorial(n):
        x = [random.random() for i in range(n)]
        while not x == sorted(x):
            random.shuffle(x)

    def nlogn(n):
        x = [random.random() for i in range(n)]
        return sorted(x)
        
    complexity_should_be("constant", constant, ns)
    complexity_should_be("linear", linear, ns)
    complexity_should_be("quadratic", quadratic, range(1, 200, 20))
    complexity_should_be("nlogn", nlogn, range(1, 2000, 20))
    complexity_should_be("cubic", cubic, range(1, 50, 5))
    complexity_should_be("exp", exp, range(1, 16))
    complexity_should_be("factorial", factorial, range(1, 8))


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

