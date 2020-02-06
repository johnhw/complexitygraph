from complexitygraph import complexity_graph
import matplotlib.pyplot as plt

def quadratic_time(n):
    s = 0
    for i in range(n):
        for j in range(n):
            s = s + 1

complexity_graph(quadratic_time, range(1, 500, 20), reps=12, number=6)
plt.savefig("quadratic.png")
