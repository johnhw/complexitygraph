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
    return np.sum(np.exp((x * fn(ns) - ts) ** 2))


def time_complexity(
    fn, ns, reps=20, number=1000, shuffle=True, setup="pass", extra_globals={}
):
    """Time the runtime of a function, running it repeatedly using timeit and return the runtimes.

    Parameters:
        fn: function to run. Must take one argument `n`, which specifies the "size" of the probelm
        ns: The values for n to use. Usually something like range(1, 1000, 100)
        number: number of times to run each function inside the timeit loop
        reps: number of repetitions of the entire timeit run to do. This is important to reduce
            variance in the estimates
        shuffle: If True, the order of ns is shuffled before each `rep`. This helps reduce
            correlated variations in the results and can result in lower noise
        setup: string, representing code to be executed at the start of each
                invocation of the fn loop (i.e. once per `number` loops).
                Defaults to "pass".
        extra_globals: any extra variables to be available to fn or setup
            during execution, as a dictionary.
        
    Returns:
        ts: the times, as an (ns, reps) shape NumPy array, for each n in order.            
            Times are normalised so that they are proportional
            to the median of the value of the first n given.
            i.e., median(ts[0,:])==1
    """
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
    """Fit different functional forms of curves to the times.

    Parameters:
        ns:     the value of n for each invocation
        ts:     the measured run time, as a (len(ns), reps) shape array
    Returns:
        scores:  normalised scores for each function
        coeffs:  coefficients for each function
        names:   names of each function
        fns:     the callable for each function in turn.
    """
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
    """Return just the score dictionary for the curve fits.
    Parameters:
        ns:     the value of n for each invocation
        ts:     the measured run time, as a (len(ns), reps) shape array
    Returns:
        score_dict: Dictionary mapping complexity function names to their scores. Scores sum to 1.0
    """
    (scores, coeffs, names, fns) = _fit_curves(ns, ts)

    ord_score = np.argsort(-scores)
    score_dict = {}
    for ix in ord_score:
        score_dict[names[ix]] = scores[ix]
    return score_dict


def score_report(score_dict):
    """Print out a simple tabular report on the complexities.
    Parameters:
        score_dict: A dictionary mapping complexity function names to scores, as
                    returned by fit_curves(ns, ts).
    """

    for name, score in score_dict.items():
        print(f"  {name.ljust(12)} {score*100.0:4.1f}%")


def plot_complexity(ns, ts, reference_curves=True):
    """Generate a plot of the time complexity, including 
    reference curves.
    Parameters:
        ns:     the value of n for each invocation
        ts:     the measured run time, as a (len(ns), reps) shape array    
    """
    # fit the curves
    scores, coeffs, names, fns = _fit_curves(ns, ts)
    # get median and IQR
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

    # show curves for the complexity functions, to 
    # help visually indicate best match
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
    """Wrapper to call time_complexity, then score_report and plot_complexity,
    all in one go.

    Parameters:
        fn: function to run. Must take one argument `n`, which specifies the "size" of the probelm
        ns: The values for n to use. Usually something like range(1, 1000, 100)
        number: number of times to run each function inside the timeit loop
        reps: number of repetitions of the entire timeit run to do. This is important to reduce
            variance in the estimates
        shuffle: If True, the order of ns is shuffled before each `rep`. This helps reduce
            correlated variations in the results and can result in lower noise
        setup: string, representing code to be executed at the start of each
                invocation of the fn loop (i.e. once per `number` loops).
                Defaults to "pass".
        extra_globals: any extra variables to be available to fn or setup
            during execution, as a dictionary.
            
    """
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
    import math
    def logn(n):
        s = 0
        for i in range(int(math.log(n))):
            s = s + 1
    #complexity_graph(quadratic_time, range(1, 500, 20), reps=12, number=6)
    complexity_graph(logn, range(1, 50000, 1000), reps=12, number=6)
    #plt.show()
