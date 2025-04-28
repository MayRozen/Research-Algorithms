import subprocess, sys, time

# subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy"], stdout=subprocess.DEVNULL)
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, cvxpy, numpy as np

np.float_ = np.float64


def mincover(graph: nx.Graph) -> set:
    """
    Return a minimum-cardinality vertex cover in the given graph.

    >>> len(mincover(nx.Graph([(1,2),(2,3)])))
    1
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,1)])))
    2
    >>> len(mincover(nx.Graph([(1,2),(2,3),(3,4),(4,1)])))
    2
    >>> len(mincover(nx.Graph([])))
    0
    """
    nodes = list(graph.nodes)
    n = len(nodes)
    if n == 0:
        return set()

    node_to_index = {node: i for i, node in enumerate(nodes)}
    x = cvxpy.Variable(n, boolean=True)

    constraints = []
    for u, v in graph.edges:
        i, j = node_to_index[u], node_to_index[v]
        constraints.append(x[i] + x[j] >= 1)

    objective = cvxpy.Minimize(cvxpy.sum(x))
    problem = cvxpy.Problem(objective, constraints)

    # Start timing
    start_time = time.time()

    # Try faster solver if available
    for solver in ["CBC", "GLPK_MI"]:
        if solver in cvxpy.installed_solvers():
            try:
                problem.solve(solver=solver, verbose=False, time_limit=1.0)
                break
            except:
                continue
    else:
        problem.solve()  # fallback to default

    # Timeout check
    if time.time() - start_time > 1.0:
        raise TimeoutError("Solving took too long!")

    # Verifying the result
    selected_nodes = {nodes[i] for i in range(n) if x.value[i] >= 0.5}

    # Verify that the selected nodes indeed form a vertex cover
    for u, v in graph.edges:
        if not (u in selected_nodes or v in selected_nodes):
            print(f"Error: Edge ({u}, {v}) is not covered by the selected vertex cover.")

    return selected_nodes


def test_mincover():
    def check(edges, expected_size):
        g = nx.Graph(edges)
        result = mincover(g)
        assert nx.is_vertex_cover(g, result), f"Result is not a valid vertex cover for {edges}"
        assert len(result) == expected_size, f"Expected size {expected_size}, got {len(result)}"

    check([(1, 2), (2, 3)], 1)
    check([(1, 2), (2, 3), (3, 1)], 2)
    check([(1, 2), (2, 3), (3, 4), (4, 1)], 2)
    check([], 0)
    print("All tests passed.")


if __name__ == '__main__':
    edges = eval(input())
    graph = nx.Graph(edges)
    print(len(mincover(graph)))

