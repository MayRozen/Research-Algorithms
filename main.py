
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root
import time


def solve_with_root(a: np.ndarray, b: np.ndarray):
    def func(x):
        return a @ x - b

    x0 = np.zeros_like(b)
    sol = root(func, x0)
    return sol.x


def test_solve_with_root():
    print("Running tests for solve_with_root...")
    for i in range(10):
        n = np.random.randint(2, 10)
        a = np.random.rand(n, n)
        while np.linalg.matrix_rank(a) < n:
            a = np.random.rand(n, n)
        b = np.random.rand(n)
        x1 = np.linalg.solve(a, b)
        x2 = solve_with_root(a, b)
        assert np.allclose(x1, x2, atol=1e-6), f"Mismatch in test {i}: {x1} vs {x2}"
        print(f"Test {i + 1}/10 passed.")
    print("All tests passed!\n")


def compare_solution_methods():
    print("Comparing solution methods...")
    sizes = np.linspace(1, 1000, 20, dtype=int)
    solve_times = []
    root_times = []

    for n in sizes:
        print(f"Testing size {n}...")
        a = np.random.rand(n, n)
        while np.linalg.matrix_rank(a) < n:
            a = np.random.rand(n, n)
        b = np.random.rand(n)

        t0 = time.time()
        np.linalg.solve(a, b)
        t1 = time.time()
        solve_times.append(t1 - t0)

        t0 = time.time()
        solve_with_root(a, b)
        t1 = time.time()
        root_times.append(t1 - t0)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, solve_times, label='numpy.linalg.solve', marker='o')
    plt.plot(sizes, root_times, label='scipy.optimize.root', marker='x')
    plt.xlabel('Matrix size (n)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Performance Comparison: numpy.linalg.solve vs scipy.optimize.root')
    plt.legend()
    plt.grid(True)
    plt.savefig("comparison.png")  # after you plot the graphs, save them to a file and upload it separately.
    plt.show()                       # this should show the plot on your screen


if __name__ == '__main__':
    test_solve_with_root()
    compare_solution_methods()
