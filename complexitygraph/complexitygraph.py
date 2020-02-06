# JHW 2019

import timeit
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import scipy.special
import time


complexities = {
    "linear": lambda n: n,
    "constant": lambda n: 1 + n * 0,
    "quadratic": lambda n: n ** 2,
    "cubic": lambda n: n ** 3,
    "log": lambda n: np.log(n),
    "nlogn": lambda n: n * np.log(n),
    "exp": lambda n: 2 ** n,
    "factorial": lambda n: scipy.special.gamma(n),
}


def complexity_fit(x, fn, ns, ts):
    return np.sum((x * fn(ns) - ts) ** 2)


def time_complexity(
    fn, ns, reps=20, number=1000, shuffle=True, setup="pass", extra_globals={}
):
    ts = []
    ns = np.array(ns)
    for rep in range(reps):
        times = []
        # shuffle to remove correlation between successive samples
        if shuffle:
            test_ns = np.random.choice(ns, replace=False, size=len(ns))
        else:
            test_ns = ns
        for n in test_ns:
            times.append(
                (
                    n,
                    timeit.timeit(
                        "fn(n)",
                        setup=setup,
                        globals={**globals(), "fn": fn, "n": n, **extra_globals},
                        number=number,
                    ),
                )
            )

            time.sleep(0.0005)  # important for getting timings reliably!
        print(".", end="", flush=True)
        # restore original order
        times = [t[1] for t in sorted(times)]
        time.sleep(0.01)
        ts.append(times)
    ts = np.array(ts).T
    ts = ts / np.median(ts[0])
    return ts


def _fit_curves(ns, ts):
    """Fit different curves to the times, and return a
    dictionary of fits"""
    # compute stats
    med_times = np.median(ts, axis=1)
    # fit and score complexities
    scores = []
    coeffs = []
    names = []
    fns = []
    ns = np.array(ns)
    ts = np.array(med_times)
    for c_name, c_fn in complexities.items():
        res = scipy.optimize.minimize_scalar(
            complexity_fit, bracket=[1e-5, 1e5], args=(c_fn, ns, ts)
        )
        scores.append(res.fun)
        coeffs.append(res.x)
        names.append(c_name)
        fns.append(c_fn)

    scores = 1.0 / np.sqrt(np.array(scores))
    tot_score = np.sum(scores)
    scores = scores / tot_score

    return scores, coeffs, names, fns


def fit_curves(ns, ts):
    """Return just the score dictionary for the curve fits"""
    (scores, coeffs, names, fns) = _fit_curves(ns, ts)

    ord_score = np.argsort(-scores)
    score_dict = {}
    for ix in ord_score:
        score_dict[names[ix]] = scores[ix]
    return score_dict


def score_report(score_dict):
    """Print out a simple tabular report on the complexities"""

    for name, score in score_dict.items():
        print(f"  {name.ljust(12)} {score*100.0:4.1f}%")


def plot_complexity(ns, ts, reference_curves=True):
    """Generate a plot of the time complexity, including 
    reference curves"""
    scores, coeffs, names, fns = _fit_curves(ns, ts)
    ord_times = np.percentile(ts, q=[25, 50, 75], axis=1)

    ns = np.array(ns)
    # plot complexity curve
    fig, ax = plt.subplots(1, 1, figsize=(9, 4))
    ax.plot(ns, ord_times[1, :], "k--", zorder=10)
    ax.plot(ns, ord_times[1, :], "k.", zorder=11)
    ax.fill_between(ns, ord_times[0, :], ord_times[2, :], alpha=0.1)
    ax.set_xlabel("N")
    ax.set_ylabel("Time (relative)")
    ax.set_title("Linear scale complexity")
    ax.set_frame_on(False)

    if reference_curves:
        for score, coeff, fn, name in zip(scores, coeffs, fns, names):
            ax.plot(
                ns,
                fn(ns) * coeff,
                alpha=min(1.0, score + 0.1),
                label=name,
                lw=1 + score * 5,
            )  #

        ax.legend()

    ax.set_ylim(0.0, np.max(ord_times[0, :]) * 1.1)


def complexity_graph(
    fn, ns, reps=20, number=1000, shuffle=True, setup="pass", extra_globals={}
):
    ts = time_complexity(fn, ns, reps, number, shuffle, setup, extra_globals)
    score_dict = fit_curves(ns, ts)
    print()
    print(f"Scores for {fn.__name__}")
    score_report(score_dict)
    plot_complexity(ns, ts, reference_curves=True)
    return score_dict


if __name__ == "__main__":
    import random
    
    def quadratic_time(n):
        s = 0
        for i in range(n):
            for j in range(n):
                s = s + 1

    complexity_graph(quadratic_time, range(1, 500, 20), reps=12, number=6)
    plt.show()
